"""module for component-contribution predictions."""
# The MIT License (MIT)
#
# Copyright (c) 2013 The Weizmann Institute of Science.
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
# Copyright (c) 2018 Institute for Molecular Systems Biology,
# ETH Zurich, Switzerland.
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

import logging
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import quilt
from equilibrator_cache import (
    FARADAY,
    Q_,
    Compound,
    CompoundCache,
    R,
    Reaction,
    ureg,
)
from equilibrator_cache.thermodynamic_constants import default_pMg
from requests.exceptions import ConnectionError

from . import DEFAULT_QUILT_PKG, DEFAULT_QUILT_VERSION, CCModelParameters
from .linalg import LINALG


logger = logging.getLogger(__name__)


class Preprocessor(object):
    """A Component Contribution preprocessing class."""

    def __init__(self, parameters: CCModelParameters, mse_inf: float):
        """Create a GibbsEnergyPredictor object."""
        self._compound_ids = parameters.train_G.index.tolist()
        self.Nc = parameters.dimensions.at["Nc", "number"]

        # store the number of "real" groups, i.e. not including the "fake"
        # ones that are placeholders for non-decomposable compounds
        self.Ng = parameters.dimensions.at["Ng", "number"]

        # the total number of groups ("real" and "fake")
        self.Ng_full = parameters.dimensions.at["Ng_full", "number"]

        W = np.diag(parameters.train_w.ravel())

        self.S = parameters.train_S.values
        self.G = parameters.train_G.values

        _, P_col = LINALG.col_uniq(self.S)
        self.S_counter = np.sum(P_col, 0)

        self.MSE_rc = parameters.MSE.at["rc", "MSE"]
        self.MSE_gc = parameters.MSE.at["gc", "MSE"]
        self.MSE_inf = mse_inf

        self.v_r = parameters.dG0_cc
        self.v_g = parameters.dG0_gc

        # pre-processing matrices
        self.G1 = parameters.P_R_rc @ parameters.inv_S.T @ W @ P_col
        self.G2 = parameters.P_N_rc @ self.G @ parameters.inv_GS.T @ W @ P_col
        self.G3 = parameters.inv_GS.T @ W @ P_col
        self.C1 = (
            self.MSE_rc * parameters.V_rc
            + self.MSE_gc * parameters.V_gc
            + self.MSE_inf * parameters.V_inf
        )
        self.C2 = (
            self.MSE_gc * parameters.P_N_rc @ self.G @ parameters.inv_GSWGS
            + self.MSE_inf * self.G @ parameters.P_N_gc
        )
        self.C3 = (
            self.MSE_gc * parameters.inv_GSWGS
            + self.MSE_inf * parameters.P_N_gc
        )

    def get_compound(self, i: int) -> Union[Compound, None]:
        """Get a Compound that was in the original training data.

        Parameters
        ----------
        i : int
            the index of that Compound


        Returns
        -------
        Compound or None
            the Compound object or None if it is not found in the cache

        """
        return self.ccache.get_compound_by_internal_id(self._compound_ids[i])

    def get_compound_index(self, compound: Compound) -> int:
        """Get the index of a compound in the original training data.

        Parameters
        ----------
        compound : Compound
            a Compound object


        Returns
        -------
        int
            the index of that compound, or -1 if it was not in the
            training list

        """
        if compound.id in self._compound_ids:
            return self._compound_ids.index(compound.id)
        else:
            return -1

    def decompose_reaction(
        self, reaction: Reaction
    ) -> Tuple[np.ndarray, np.ndarray, Dict[Compound, float]]:
        """Decompose a reaction.

        Parameters
        ----------
        reaction : Reaction
            the input Reaction object


        Returns
        -------
        tuple
            a tuple (x, g, residual) of the stoichiometric vector and
            group incidence vector, and the residual reaction
            in sparse notation

        """
        x = np.zeros(self.Nc)  # stoichiomtric vector for the RC part
        g = np.zeros(self.Ng)  # group vector for the GC part
        residual = dict()

        for compound, coefficient in reaction.items(protons=False):
            i = self.get_compound_index(compound)
            if i >= 0:
                # This compound is in the training set so we can use reactant
                # contributions for it
                x[i] = coefficient
            elif not compound.group_vector:
                residual[compound] = coefficient
            else:
                g += coefficient * np.array(
                    compound.group_vector, ndmin=1, dtype=float
                )
        return x, g, residual

    def decompose_reactions(
        self, reactions: List[Reaction]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Decompose a list of reactions.

        Parameters
        ----------
        reactions: List[Reaction] :
            a list of Reaction objects


        Returns
        -------
        tuple
            a tuple (X, G, U) of the main stoichiometric matrix the
            group change matrix, and the residual stoichiometric matrix

        """
        Nr = len(reactions)
        X = np.zeros((self.Nc, Nr))
        G = np.zeros((self.Ng_full, Nr))

        residuals = []
        for i, reaction in enumerate(reactions):
            x, g, residual = self.decompose_reaction(reaction)
            X[:, i] = x
            G[: self.Ng, i] = g
            residuals.append(residual)

        # make an ordered list of the unknown-undecomposable compounds
        residual_compounds = set()
        for sparse in residuals:
            residual_compounds.update(sparse.keys())
        residual_compounds = sorted(residual_compounds)

        # construct the residual stoichiometric matrix U
        U = np.zeros((len(residual_compounds), Nr))
        for i, sparse in enumerate(residuals):
            for cpd, coeff in sparse.items():
                j = residual_compounds.index(cpd)
                U[j, i] = coeff

        return X, G, U

    def predict(
        self, X: np.ndarray, G: np.ndarray, U: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        r"""Calculate the chemical reaction energies for a list of reactions.

        Parameters
        ----------
        X : np.ndarray
            stoichiometric matrix of the reactions (RC part)
        G : np.ndarray
            group incidence matrix of the reactions (GC part)
        U : np.ndarray
            stoichiometric matrix of unknown-undecomposable compounds


        Returns
        -------
        standard_dg : np.ndarray
            a 1D array with the estimated values of the standard
            :math:`\Delta G`
        cov_dg : np.ndarray
            a 2D array with the error covariance matrix for the standard
            :math:`\Delta G` values

        """
        standard_dg = X.T @ self.v_r + G.T @ self.v_g
        cov_dg = (
            X.T @ self.C1 @ X
            + X.T @ self.C2 @ G
            + G.T @ self.C2.T @ X
            + G.T @ self.C3 @ G
            + self.MSE_inf * U.T @ U
        )
        return standard_dg, cov_dg

    @staticmethod
    def quilt_fetch(
        package: str = DEFAULT_QUILT_PKG,
        overwrite: bool = True,
        version: Optional[str] = DEFAULT_QUILT_VERSION,
        tag: Optional[str] = None,
    ) -> CCModelParameters:
        """Get the CC parameters from quilt.

        Parameters
        ----------
        package : str, optional
            quilt package name (Default value = DEFAULT_QUILT_PKG)
        overwrite : bool, optional
            Re-download the quilt data if a newer version exists
            (Default value = True).
        version : str, optional
            quilt version (Default value = DEFAULT_QUILT_VERSION)
        tag : str, optional
            quilt tab (Default value = None)

        Returns
        -------
        CCModelParameters
            a collection of Component Contribution parameters.

        """
        try:
            logger.info("Fetching Component-Contribution parameters...")
            quilt.install(package, version=version, tag=tag, force=overwrite)
        except ConnectionError:
            logger.error(
                "No internet connection available. Attempting to use "
                "the existing component contribution model."
            )
        except PermissionError:
            logger.error(
                "You do not have the necessary filesystem permissions to "
                "download an update to the quilt data. Attempting to use the "
                "existing component contribution model."
            )
        pkg = quilt.load(package)

        param_dict = {k: v() for k, v in pkg.parameters._children.items()}
        return CCModelParameters(**param_dict)


class GibbsEnergyPredictor(object):
    """A class that can be used to predict dGs of reactions using CC."""

    DEFAULT_QUILT_PARAMS: CCModelParameters = Preprocessor.quilt_fetch(
        package=DEFAULT_QUILT_PKG,
        version=DEFAULT_QUILT_VERSION,
        overwrite=True,
        tag=None,
    )

    def __init__(
        self,
        ccache: CompoundCache,
        rmse_inf: Q_,
        parameters: CCModelParameters = None,
    ):
        """Create a GibbsEnergyPredictor object.

        ccache : CompoundCache
            The compound cache used for looking up structures and pKas.
        parameters : CCModelParameters
            Optional CC parameters. If not provided, the parameters are
            automatically downloaded from quilt.
        mse_inf : another parameter determining the uncertainty we associate
            with reactions that are not covered at all (not by RC nor GC)
        """
        self.ccache = ccache

        self.params = parameters or GibbsEnergyPredictor.DEFAULT_QUILT_PARAMS

        assert rmse_inf.check(
            "[energy]/[substance]"
        ), "rmse_inf must be in kJ/mol or equivalent units"

        mse_inf = rmse_inf.m_as("kJ/mol") ** 2
        self.preprocess = Preprocessor(self.params, mse_inf)
        self.Nc = self.preprocess.Nc
        self.Ng = self.preprocess.Ng
        self.Ng_full = self.preprocess.Ng_full

    def standard_dgf(self, compound: Compound) -> ureg.Measurement:
        """Calculate the chemical formation energy of the major MS at pH 7.

        Parameters
        ----------
        compound: Compound :
            a compound object


        Returns
        -------
        Measurement
            a tuple of two arrays. the first is a 1D NumPy array
            containing the CC estimates for the reactions' untransformed dG0
            (i.e. using the major MS at pH 7 for each of the reactants).
            the second is a 2D numpy array containing the covariance matrix
            of the standard errors of the estimates. one can use the
            eigenvectors of the matrix to define a confidence high-dimensional
            space, or use U as the covariance of a Gaussian used for sampling
            (where dG0_cc is the mean of that Gaussian).

        """
        return self.standard_dg(Reaction({compound: 1}))

    @ureg.check(None, None, "", "[concentration]", "[temperature]", "")
    def standard_dgf_prime(
        self,
        compound: Compound,
        p_h: Q_,
        ionic_strength: Q_,
        temperature: Q_,
        p_mg: Q_ = default_pMg,
    ) -> ureg.Measurement:
        """Calculate the biocheimcal formation energy of the compound.

        Parameters
        ----------
        compound : Compound
            a compound object
        p_h : Quantity
            the pH
        ionic_strength : Quantity
            the ionic strength
        temperature : Quantity
            temperature in Kalvin
        p_mg : Quantity, optional
            the pMg (Default value = default_pMg)


        Returns
        -------
        type
            a tuple of two arrays. the first is a 1D NumPy array
            containing the CC estimates for the reactions' untransformed dG0
            (i.e. using the major MS at pH 7 for each of the reactants).
            the second is a 2D numpy array containing the covariance matrix
            of the standard errors of the estimates. one can use the
            eigenvectors of the matrix to define a confidence high-dimensional
            space, or use U as the covariance of a Gaussian used for sampling
            (where dG0_cc is the mean of that Gaussian).

        """
        return self.standard_dg_prime(
            Reaction({compound: 1}),
            p_h=p_h,
            ionic_strength=ionic_strength,
            temperature=temperature,
            p_mg=p_mg,
        )

    def dg_analysis(self, reaction: Reaction) -> List[Dict[str, object]]:
        r"""Analyse the weight of each observation to the :math:`\Delta G`.

        Parameters
        ----------
        reaction : Reaction
            the input Reaction object


        Returns
        -------
        list
            a list of reactions that contributed to the value of the
            :math:`\Delta G` estimation, with their weights and extra
            information

        """
        G1 = self.preprocess.G1
        G2 = self.preprocess.G2
        G3 = self.preprocess.G3
        S = self.preprocess.S
        S_counter = self.preprocess.S_counter

        x, g, residual = self.preprocess.decompose_reaction(reaction)
        if residual:
            return []

        # dG0_cc = (x*G1 + x*G2 + g*G3)*b
        weights_rc = (x @ G1).round(5)
        weights_gc = (x @ G2 + g @ G3[0 : self.Ng, :]).round(5)
        weights = abs(weights_rc) + abs(weights_gc)

        analysis = []
        for j in reversed(np.argsort(weights)):
            if abs(weights[j]) < 1e-5:
                continue
            r = {i: S[i, j] for i in range(S.shape[0]) if S[i, j] != 0}
            analysis.append(
                {
                    "index": j,
                    "w_rc": weights_rc[j],
                    "w_gc": weights_gc[j],
                    "reaction": r,
                    "count": int(S_counter[j]),
                }
            )

        return analysis

    def is_using_group_contribution(self, reaction: Reaction) -> bool:
        r"""Check if group contributions is needed for the :math:`\Delta G`.

        Parameters
        ----------
        reaction : Reaction
            the input Reaction object


        Returns
        -------
        bool
            True if the reaction require group contributions.

        """
        G2 = self.preprocess.G2
        G3 = self.preprocess.G3

        x, g, residual = self.preprocess.decompose_reaction(reaction)
        if residual:
            return False

        weights_gc = x @ G2 + g @ G3[: self.Ng, :]
        sum_w_gc = sum(abs(weights_gc).flat)
        logging.info("sum(w_gc) = %.2g" % sum_w_gc)
        return sum_w_gc > 1e-5

    def standard_dg_multi(
        self, reactions: List[Reaction]
    ) -> Tuple[np.ndarray, np.ndarray]:
        r"""Calculate the chemical reaction energies for a list of reactions.

        Using the major microspecies of each of the reactants.

        Parameters
        ----------
        reactions : List[Reaction]
            a list of Reaction objects


        Returns
        -------
        standard_dg : np.ndarray
            the array of Component Contribution estimates for the reactions'
            untransformed :math:`\Delta G` in kJ/mol,
            (i.e. using the major MS at pH 7 for each of the reactants).
        cov_dg : np.ndarray
            the covariance matrix of the standard errors of the estimates.
            one can use the eigenvectors of the matrix to define a confidence
            high-dimensional space, or use U as the covariance of a Gaussian
            used for sampling (where cov_dg is the mean of that Gaussian).

        """
        X, G, U = self.preprocess.decompose_reactions(reactions)

        standard_dg, cov_dg = self.preprocess.predict(X, G, U)

        standard_dg = Q_(standard_dg, "kJ/mol")
        cov_dg = Q_(cov_dg, "(kJ/mol)**2")
        return standard_dg, cov_dg

    @ureg.check(None, None, "", "[concentration]", "[temperature]", "")
    def standard_dg_prime_multi(
        self,
        reactions: List[Reaction],
        p_h: Q_,
        ionic_strength: Q_,
        temperature: Q_,
        p_mg: Q_ = default_pMg,
    ) -> Tuple[np.ndarray, np.ndarray]:
        r"""Calculate the transformed reaction energies of a list of reactions.

        Parameters
        ----------
        reactions : List[Reaction]
            a list of Reaction objects
        p_h : Quantity
            the pH
        ionic_strength : Quantity
            the ionic strength
        temperature : Quantity
            the temperature
        p_mg: Quantity, optional
             (Default value = default_pMg)

        Returns
        -------
        standard_dg_prime : np.ndarray
            the array of Component Contribution estimates for the reactions'
            :math:`\Delta G'` in kJ/mol
        cov_dg : np.ndarray
            the covariance matrix of the standard errors of the estimates.
            one can use the eigenvectors of the matrix to define a confidence
            high-dimensional space, or use U as the covariance of a Gaussian
            used for sampling (where cov_dg is the mean of that Gaussian).

        """
        standard_dg, cov_dg = self.standard_dg_multi(reactions)

        for i, r in enumerate(reactions):
            standard_dg[i] += (
                R
                * temperature
                * r.transform(
                    p_h=p_h,
                    ionic_strength=ionic_strength,
                    temperature=temperature,
                    p_mg=p_mg,
                )
            )

        return standard_dg, cov_dg

    def standard_dg(self, reaction: Reaction) -> ureg.Measurement:
        r"""Calculate the chemical reaction energy.

        Using the major microspecies of each of the reactants.

        Parameters
        ----------
        reaction: Reaction :
            the input Reaction object


        Returns
        -------
        Measurement
        standard_dg : Measurement
            the :math:`\Delta G` in kJ/mol and standard error. to
            calculate the 95% confidence interval, multiply the error by 1.96

        """
        standard_dg, cov_dg = self.standard_dg_multi([reaction])
        standard_dg = standard_dg[0].plus_minus(np.sqrt(cov_dg[0, 0]))
        return standard_dg

    @ureg.check(None, None, "", "[concentration]", "[temperature]", "")
    def standard_dg_prime(
        self,
        reaction: Reaction,
        p_h: Q_,
        ionic_strength: Q_,
        temperature: Q_,
        p_mg: Q_ = default_pMg,
    ) -> ureg.Measurement:
        r"""Calculate the transformed reaction energies of a reaction.

        Parameters
        ----------
        reaction : Reaction
            the input Reaction object
        p_h : Q_
            pH
        ionic_strength : Q_
            ionic strength
        temperature : Q_
            temperature
        p_mg: Q_ :
             (Default value = default_pMg)

        Returns
        -------
        standard_dg : Measurement
            the :math:`\Delta G'` in kJ/mol and standard error. to
            calculate the 95% confidence interval, multiply the error by 1.96

        """
        standard_dg, cov_dg = self.standard_dg_prime_multi(
            [reaction],
            p_h=p_h,
            ionic_strength=ionic_strength,
            temperature=temperature,
            p_mg=p_mg,
        )
        standard_dg = standard_dg[0].plus_minus(np.sqrt(cov_dg[0, 0]))
        return standard_dg

    @ureg.check(
        None,
        None,
        None,
        None,
        None,
        "",
        "",
        "[concentration]",
        "[concentration]",
        "[energy]/[current]/[time]",
        "[temperature]",
        "",
        "",
    )
    def multicompartmental_standard_dg_prime(
        self,
        reaction_1: Reaction,
        reaction_2: Reaction,
        transported_protons: float,
        transported_charge: float,
        p_h_1: Q_,
        p_h_2: Q_,
        ionic_strength_1: Q_,
        ionic_strength_2: Q_,
        delta_chi: Q_,
        temperature: Q_,
        p_mg_1: Q_ = default_pMg,
        p_mg_2: Q_ = default_pMg,
    ) -> ureg.Measurement:
        r"""Calculate the transformed energies of multi-compartmental reactions.

        Based on the equations from
        Harandsdottir et al. 2012 (https://doi.org/10.1016/j.bpj.2012.02.032)

        Parameters
        ----------
        reaction_1 : Reaction
            half-reaction associated to compartment 1
        reaction_2 : Reaction
            half-reaction associated to compartment 2
        transported_protons : float
            the total number of protons
            transported through the membrane
        transported_charge : float
            the total charge
            transported through the membrane
        p_h_1 : Quantity
            the pH in compartment 1
        p_h_2 : Quantity
            the pH in compartment 2
        ionic_strength_1 : Quantity
            the ionic strength in compartment 1
        ionic_strength_2 : Quantity
            the ionic strength in compartment 2
        delta_chi : Quantity
            electrostatic potential across the membrane
        temperature : Quantity
            temperature in Kalvin
        p_mg_1 : Quantity, optional
            the pMg in compartment 1 (Default value = 10)
        p_mg_2 : Quantity, optional
            the pMg in compartment 2 (Default value = 10)

        Returns
        -------
        standard_dg : Measurement
            the :math:`\Delta G'` in kJ/mol and standard error. to
            calculate the 95% confidence interval, multiply the error by 1.96

        """
        standard_dg, cov_dg = self.standard_dg_multi([reaction_1, reaction_2])

        # the contribution of the chemical reaction to the standard ΔG' is
        # the sum of the two half reactions and the variance is the sum
        # of all the values in cov_dg. For the uncertainty we take the square
        # root of the sum.

        uncertainty = np.sqrt(sum(cov_dg.flat))
        standard_dg = (standard_dg[0] + standard_dg[1]).plus_minus(uncertainty)

        # Here we calculate the transform (since the two reactions are in
        # different pH and I, we have to do it here):
        transform_dg_over_rt = 0.0
        for compound, coeff in reaction_1.items(protons=False):
            transform_dg_over_rt += coeff * compound.transform(
                p_h=p_h_1,
                ionic_strength=ionic_strength_1,
                temperature=temperature,
                p_mg=p_mg_1,
            )

        for compound, coeff in reaction_2.items(protons=False):
            transform_dg_over_rt += coeff * compound.transform(
                p_h=p_h_2,
                ionic_strength=ionic_strength_2,
                temperature=temperature,
                p_mg=p_mg_2,
            )

        transform_dg = (R * temperature * transform_dg_over_rt).to("kJ/mol")

        dg_protons = (
            transported_protons
            * R
            * temperature
            * np.log(10.0)
            * (p_h_2 - p_h_1)
        ).to("kJ/mol")

        dg_electrostatic = (FARADAY * transported_charge * delta_chi).to(
            "kJ/mol"
        )

        standard_dg += transform_dg - dg_protons - dg_electrostatic
        return standard_dg
