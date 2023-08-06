"""A wrapper for the GibbeEnergyPredictor in component-contribution."""
# The MIT License (MIT)
#
# Copyright (c) 2013 Weizmann Institute of Science
# Copyright (c) 2018 Institute for Molecular Systems Biology,
# ETH Zurich
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from typing import Dict, List, Tuple

import numpy as np
from component_contribution.predict import GibbsEnergyPredictor, Preprocessor
from equilibrator_cache import Compound, CompoundMicrospecies

from . import (
    FARADAY,
    Q_,
    R,
    ccache,
    default_I,
    default_pH,
    default_pMg,
    default_rmse_inf,
    default_T,
    ureg,
)
from .phased_reaction import PhasedReaction


def find_most_abundance_ms(
    cpd: Compound, p_h: Q_, ionic_strength: Q_, temperature: Q_
) -> CompoundMicrospecies:
    """Find the most abundant microspecies based on transformed energies.

    Ignore microspecies with Magnesium, as we assume they never traverse
    the membrane. Therefore, the value of p_mg is not necessary.
    """
    p_mg = default_pMg
    ddg_over_rts = [
        (ms.transform(p_h, ionic_strength, temperature, p_mg).magnitude, ms)
        for ms in cpd.microspecies
        if ms.number_magnesiums == 0
    ]
    min_ddg, min_ms = min(ddg_over_rts, key=lambda x: x[0])
    return min_ms


def predict_protons_and_charge(
    rxn: PhasedReaction, p_h: Q_, ionic_strength: Q_, temperature: Q_
) -> Tuple[float, float]:
    """Find the #protons and charge of a transport half-reaction."""
    n_h = 0
    z = 0
    for cpd, coeff in rxn.items():
        if ccache.is_proton(cpd):
            n_h += coeff
            z += coeff
        else:
            ms = find_most_abundance_ms(cpd, p_h, ionic_strength, temperature)
            n_h += coeff * ms.number_protons
            z += coeff * ms.charge
    return n_h, z


class ComponentContribution(object):
    """A wrapper class for GibbsEnergyPredictor.

    Also holds default conditions for compounds in the different phases.
    """

    @ureg.check(
        None,
        None,
        None,
        "[concentration]",
        "[temperature]",
        "[energy]/[substance]",
        None,
    )
    def __init__(
        self,
        p_h: Q_ = default_pH,
        p_mg: Q_ = default_pMg,
        ionic_strength: Q_ = default_I,
        temperature: Q_ = default_T,
        rmse_inf: Q_ = default_rmse_inf,
        **quilt_cc_kwargs,
    ) -> object:
        """Create a ComponentContribution object.

        :param p_h: Set the -log10 of the proton concentration [H+].
        :param p_mg: Set the -log10 of the magnesium ion concentration [Mg++].
        :param ionic_strength: Set the ionic strength.
        :param temperature: Set the temperature.
        :param rmse_inf: Set the factor by which to multiply the error
        covariance matrix for reactions outside the span of
        Component Contribution.
        """
        self.p_h = p_h
        self.ionic_strength = ionic_strength
        self.p_mg = p_mg
        self.temperature = temperature

        if quilt_cc_kwargs:
            parameters = Preprocessor.quilt_fetch(**quilt_cc_kwargs)
        else:
            parameters = None

        self.predictor = GibbsEnergyPredictor(
            ccache, rmse_inf=rmse_inf, parameters=parameters
        )

    @property
    def RT(self) -> Q_:
        """Get the value of RT."""
        return R * self.temperature

    def standard_dg(self, reaction: PhasedReaction) -> ureg.Measurement:
        """Calculate the chemical reaction energies of a reaction.

        :param reaction: the input Reaction object
        :return: a tuple of the dG0 in kJ/mol and standard error. to
        calculate the confidence interval, use the range -1.96 to 1.96 times
        this value
        """
        residual_reaction, stored_dg = reaction.separate_stored_dg()

        standard_dg = self.predictor.standard_dg(residual_reaction)

        return standard_dg + stored_dg

    def standard_dg_multi(
        self, reactions: List[PhasedReaction]
    ) -> Tuple[np.array, np.array]:
        """Calculate the chemical reaction energies of a list of reactions.

        Using the major microspecies of each of the reactants.

        :return: a tuple with the CC estimation of the major microspecies'
        standard formation energy, and the uncertainty matrix.
        """
        rxn_dg_pairs = map(lambda r: r.separate_stored_dg(), reactions)
        residual_reactions, stored_dg = zip(*rxn_dg_pairs)
        stored_dg = np.array(stored_dg)

        (standard_dg, dg_sigma) = self.predictor.standard_dg_multi(
            residual_reactions
        )
        return standard_dg + stored_dg, dg_sigma

    def standard_dg_prime(self, reaction: PhasedReaction) -> ureg.Measurement:
        """Calculate the transformed reaction energies of a reaction.

        :param reaction: the input Reaction object
        :return: a tuple of the dG0_prime in kJ/mol and standard error. to
        calculate the confidence interval, use the range -1.96 to 1.96 times
        this value
        """
        residual_reaction, stored_dg_prime = reaction.separate_stored_dg_prime(
            p_h=self.p_h,
            p_mg=self.p_mg,
            ionic_strength=self.ionic_strength,
            temperature=self.temperature,
        )

        standard_dg_prime = self.predictor.standard_dg_prime(
            residual_reaction,
            p_h=self.p_h,
            p_mg=self.p_mg,
            ionic_strength=self.ionic_strength,
            temperature=self.temperature,
        )

        return standard_dg_prime + stored_dg_prime

    def dg_prime(self, reaction: PhasedReaction) -> ureg.Measurement:
        """Calculate the dG'0 of a single reaction.

        :param reaction: an object of type Reaction
        :return: a tuple of (dG_r_prime, dG_uncertainty) where dG_r_prime is
        the estimated Gibbs free energy of reaction and dG_uncertainty is the
        standard deviation of estimation. Multiply it by 1.96 to get a 95%
        confidence interval (which is the value shown on eQuilibrator).
        """
        return (
            self.standard_dg_prime(reaction)
            + self.RT * reaction.dg_correction()
        )

    def standard_dg_prime_multi(
        self, reactions: List[PhasedReaction]
    ) -> Tuple[np.array, np.array]:
        """Calculate the transformed reaction energies of a list of reactions.

        :return: a tuple of two arrays. the first is a 1D NumPy array
        containing the CC estimates for the reactions' transformed dG0
        the second is a 2D numpy array containing the covariance matrix
        of the standard errors of the estimates. one can use the eigenvectors
        of the matrix to define a confidence high-dimensional space, or use
        U as the covariance of a Gaussian used for sampling
        (where dG0_cc is the mean of that Gaussian).
        """
        rxn_dg_pairs = map(
            lambda r: r.separate_stored_dg_prime(
                p_h=self.p_h,
                p_mg=self.p_mg,
                ionic_strength=self.ionic_strength,
                temperature=self.temperature,
            ),
            reactions,
        )
        residual_reactions, stored_dg_primes = zip(*rxn_dg_pairs)
        stored_dg_primes = np.array(stored_dg_primes)

        (standard_dg_prime, dg_sigma) = self.predictor.standard_dg_prime_multi(
            residual_reactions,
            p_h=self.p_h,
            p_mg=self.p_mg,
            ionic_strength=self.ionic_strength,
            temperature=self.temperature,
        )
        return standard_dg_prime + stored_dg_primes, dg_sigma

    def physiological_dg_prime(
        self, reaction: PhasedReaction
    ) -> ureg.Measurement:
        """Calculate the dG'm of a single reaction.

        Assume all aqueous reactants are at 1 mM, gas reactants at 1 mbar and
        the rest at their standard concentration.

        :param reaction: an object of type PhasedReaction
        :return: a tuple (dG_r_prime, dG_uncertainty) where dG_r_prime is
        the estimated Gibbs free energy of reaction and dG_uncertainty is the
        standard deviation of estimation. Multiply it by 1.96 to get a 95%
        confidence interval (which is the value shown on eQuilibrator).
        """
        return (
            self.standard_dg_prime(reaction)
            + self.RT * reaction.physiological_dg_correction()
        )

    def ln_reversibility_index(
        self, reaction: PhasedReaction
    ) -> ureg.Measurement:
        """Calculate the reversibility index (ln Gamma) of a single reaction.

        :return: ln_RI - The reversibility index (in natural log scale).
        """
        physiological_dg_prime = self.physiological_dg_prime(reaction)

        abs_sum_coeff = reaction._sum_absolute_coefficients()
        if abs_sum_coeff == 0:
            return np.inf
        ln_RI = (2.0 / abs_sum_coeff) * physiological_dg_prime / self.RT
        return ln_RI

    def standard_e_prime(self, reaction: PhasedReaction) -> ureg.Measurement:
        """Calculate the E'0 of a single half-reaction.

        :param reaction: a PhasedReaction object
        :return: a tuple (E0_prime, E0_uncertainty) where E0_prime is
        the estimated standard electrostatic potential of reaction and
        E0_uncertainty is the standard deviation of estimation. Multiply it
        by 1.96 to get a 95% confidence interval (which is the value shown on
        eQuilibrator).
        """
        n_e = reaction.check_half_reaction_balancing()
        if n_e is None:
            raise ValueError("reaction is not chemically balanced")
        if n_e == 0:
            raise ValueError(
                "this is not a half-reaction, " "electrons are balanced"
            )
        return -self.standard_dg_prime(reaction) / (n_e * FARADAY)

    def physiological_e_prime(
        self, reaction: PhasedReaction
    ) -> ureg.Measurement:
        """Calculate the E'0 of a single half-reaction.

        :param reaction: a PhasedReaction object
        :return: a tuple (E0_prime, E0_uncertainty) where E0_prime is
        the estimated standard electrostatic potential of reaction and
        E0_uncertainty is the standard deviation of estimation. Multiply it
        by 1.96 to get a 95% confidence interval (which is the value shown on
        eQuilibrator).
        """
        n_e = reaction.check_half_reaction_balancing()
        if n_e is None:
            raise ValueError("reaction is not chemically balanced")
        if n_e == 0:
            raise ValueError(
                "this is not a half-reaction, " "electrons are balanced"
            )
        return -self.physiological_dg_prime(reaction) / (n_e * FARADAY)

    def e_prime(self, reaction: PhasedReaction) -> ureg.Measurement:
        """Calculate the E'0 of a single half-reaction.

        :param reaction: a PhasedReaction object
        :return: a tuple (E0_prime, E0_uncertainty) where E0_prime is
        the estimated standard electrostatic potential of reaction and
        E0_uncertainty is the standard deviation of estimation. Multiply it
        by 1.96 to get a 95% confidence interval (which is the value shown on
        eQuilibrator).
        """
        n_e = reaction.check_half_reaction_balancing()
        if n_e is None:
            raise ValueError("reaction is not chemically balanced")
        if n_e == 0:
            raise ValueError(
                "this is not a half-reaction, " "electrons are balanced"
            )
        return -self.dg_prime(reaction) / (n_e * FARADAY)

    def dg_analysis(self, reaction: PhasedReaction) -> List[Dict[str, object]]:
        """Get the analysis of the component contribution estimation process.

        :param reaction: a PhasedReaction object.
        :return: the analysis results as a list of dictionaries
        """
        return self.predictor.get_dg_analysis(reaction)

    def is_using_group_contribution(self, reaction: PhasedReaction) -> bool:
        """Check whether group contribution is needed to get this reactions' dG.

        :param reaction: a PhasedReaction object.
        :return: true iff group contribution is needed
        """
        return self.predictor.is_using_group_contribution(reaction)

    def multicompartmental_standard_dg_prime(
        self,
        reaction_inner: PhasedReaction,
        reaction_outer: PhasedReaction,
        delta_chi: Q_,
        p_h_outer: Q_,
        ionic_strength_outer: Q_,
        p_mg_outer: Q_ = default_pMg,
    ) -> ureg.Measurement:
        """Calculate the transformed energies of a multi-compartmental reaction.

        Based on the equations from
        Harandsdottir et al. 2012 (https://doi.org/10.1016/j.bpj.2012.02.032)

        :param reaction_inner: the inner compartment half-reaction
        :param reaction_outer: the outer compartment half-reaction
        :param delta_phi: the difference in electro-static potential between
        the outer and inner compartments
        :param p_h_outer: the pH in the outside compartment
        :param ionic_strength_outer: the ionic strength outside
        :param p_mg_outer: the pMg in the outside compartment
        :return: the transport reaction Gibbs free energy change
        """
        n_h_inner, z_inner = predict_protons_and_charge(
            reaction_inner, self.p_h, self.ionic_strength, self.temperature
        )
        n_h_outer, z_outer = predict_protons_and_charge(
            reaction_outer, self.p_h, self.ionic_strength, self.temperature
        )
        if (n_h_inner != -n_h_outer) or (z_inner != -z_outer):
            raise ValueError(
                "inner and outer half-reactions don't balance each other: "
                f"n_h(inner) = {n_h_inner}, n_h(outer) = {n_h_outer}, "
                f"z(inner) = {z_inner}, z(outer) = {z_outer}, "
            )

        transported_protons = n_h_outer
        transported_charge = z_outer

        (
            residual_reaction_inner,
            stored_dg_prime_inner,
        ) = reaction_inner.separate_stored_dg_prime(
            p_h=self.p_h,
            p_mg=self.p_mg,
            ionic_strength=self.ionic_strength,
            temperature=self.temperature,
        )

        (
            residual_reaction_outer,
            stored_dg_prime_outer,
        ) = reaction_outer.separate_stored_dg_prime(
            p_h=p_h_outer,
            p_mg=p_mg_outer,
            ionic_strength=ionic_strength_outer,
            temperature=self.temperature,
        )

        (standard_dg) = self.predictor.multicompartmental_standard_dg_prime(
            residual_reaction_inner,
            residual_reaction_outer,
            transported_protons,
            transported_charge,
            self.p_h,
            p_h_outer,
            self.ionic_strength,
            ionic_strength_outer,
            delta_chi,
            self.temperature,
        )

        return standard_dg + stored_dg_prime_inner + stored_dg_prime_outer
