# coding: utf-8

# ------------------------------------------------------------------------------
# Copyright (C) 2018-2019 Maximilian Stahlberg
#
# This file is part of PICOS.
#
# PICOS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PICOS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

"""Implementation of :class:`SCIPSolver`."""

import cvxopt

from ..apidoc import api_end, api_start
from ..compat import assert_import_exists
from ..constraints import (AffineConstraint, ConvexQuadraticConstraint,
                           NonconvexQuadraticConstraint, RSOCConstraint,
                           SOCConstraint)
from ..expressions import AffineExpression, BinaryVariable, IntegerVariable
from ..modeling.footprint import Specification
from ..modeling.solution import (PS_FEASIBLE, PS_INFEASIBLE, PS_UNBOUNDED,
                                 PS_UNKNOWN, SS_INFEASIBLE, SS_OPTIMAL,
                                 SS_PREMATURE, SS_UNKNOWN)
from .solver import Solver

_API_START = api_start(globals())
# -------------------------------


class SCIPSolver(Solver):
    """Interface to the SCIP solver via the PySCIPOpt Python interface."""

    SUPPORTED = Specification.compile(
        directions=Specification.ALL,
        objectives=[
            AffineExpression],
        variables=Specification.ALL,
        constraints=[
            AffineConstraint,
            SOCConstraint,
            RSOCConstraint,
            ConvexQuadraticConstraint,
            NonconvexQuadraticConstraint])

    @classmethod
    def supports(cls, footprint):
        """Implement :meth:`~.solver.Solver.supports`."""
        if not Solver.supports(footprint):
            return False

        # HACK: SCIP does not produce dual values (except for LPs, where they
        #       are known to be sometimes incorrect). For now pretend SCIP does
        #       not support continuous problems at all (unless there are
        #       nonconvex quadratics where no other solver works).
        # TODO: Support all continuous problems when ``duals=False``.
        if footprint.continuous \
        and not ("con", NonconvexQuadraticConstraint) in footprint:
            return False

        return footprint << cls.SUPPORTED

    @classmethod
    def default_penalty(cls):
        """Implement :meth:`~.solver.Solver.default_penalty`."""
        return 1.0  # Stable free/open source solver.

    @classmethod
    def test_availability(cls):
        """Implement :meth:`~.solver.Solver.test_availability`."""
        assert_import_exists("pyscipopt")

    @classmethod
    def names(cls):
        """Implement :meth:`~.solver.Solver.names`."""
        return "scip", "SCIP", "SCIP Optimization Suite"

    def __init__(self, problem):
        """Initialize a SCIP solver interface.

        :param ~picos.Problem problem: The problem to be solved.
        """
        super(SCIPSolver, self).__init__(problem)

        self._scipVar = dict()
        """Maps PICOS variable indices to SCIP variables."""

        self._scipCons = dict()
        """
        Maps PICOS constraints to lists of SCIP constraints.

        For PICOS second order cone constraints, the first entry in the list is
        a SCIP quadratic constraint and the second entry is a SCIP linear
        auxiliary constraint.
        """

        self._scipQuadObjAuxVar = None
        """A SCIP auxiliary variable to support a PICOS quadratic objective."""

        self._scipQuadObjAuxCon = None
        """A SCIP auxiliary constraint to support a PICOS quadr. objective."""

    def reset_problem(self):
        """Implement :meth:`~.solver.Solver.reset_problem`."""
        self.int = None

        self._scipVar.clear()
        self._scipCons.clear()

        self._scipQuadObjAuxVar = None
        self._scipQuadObjAuxCon = None

    def _make_scip_var_names(self, picosVar, localIndex=None):
        """Make SCIP variable names.

        Converts a PICOS variable to a list of SCIP variable names, each
        corresponding to one scalar variable contained in the PICOS variable.
        If localIndex is given, then only the name of the SCIP variable
        representing the scalar variable with that offset is returned.
        The name format is "picosName[localIndex]".
        """
        # TODO: This function appears in multiple solvers, move it to the Solver
        #       base class as "_make_scalar_var_names".
        if localIndex is not None:
            return "{}[{}]".format(picosVar.name, localIndex)
        else:
            return [
                self._make_scip_var_names(picosVar, localIndex)
                for localIndex in range(len(picosVar))]

    def _import_variable(self, picosVar):
        from math import ceil, floor

        dim = picosVar.dim
        inf = self.int.infinity()

        # Retrieve type code.
        if isinstance(picosVar, (BinaryVariable, IntegerVariable)):
            scipVarType = "I"
        else:
            scipVarType = "C"

        # Retrieve bounds.
        lowerBounds = [-inf]*dim
        upperBounds = [inf]*dim
        lower, upper = picosVar.bound_dicts
        for i, b in lower.items():
            lowerBounds[i] = b
        for i, b in upper.items():
            upperBounds[i] = b

        # Refine bounds.
        if isinstance(picosVar, IntegerVariable):
            lowerBounds = [int(ceil(b)) for b in lowerBounds]
            upperBounds = [int(floor(b)) for b in upperBounds]

        # Give names.
        scipNames = self._make_scip_var_names(picosVar)

        # Import scalar variables.
        for i in range(dim):
            self._scipVar[picosVar.id_at(i)] = self.int.addVar(
                name=scipNames[i], vtype=scipVarType,
                lb=lowerBounds[i], ub=upperBounds[i])

    def _import_variable_values(self):
        # TODO: Import variable values with SCIP.
        raise NotImplementedError

    def _reset_variable_values(self):
        # TODO: Import variable values with SCIP.
        raise NotImplementedError

    def _affinexp_pic2scip(self, picosExpression):
        """Transform an affine expression from PICOS to SCIP.

        Multidimensional PICOS expressions are converted to a number of scalar
        SCIP expressions.

        :returns: A :class:`list` of :class:`SCIP expressions
            <pyscipopt.scip.Expr>`.
        """
        from pyscipopt.scip import Expr

        if picosExpression is None:
            yield Expr()
            return

        for scipVars, coefficients, constant in picosExpression.sparse_rows(
                None, indexFunction=lambda picosVar, localIndex:
                self._scipVar[picosVar.id_at(localIndex)]):
            scipExpression = Expr()
            for scipVar, coefficient in zip(scipVars, coefficients):
                scipExpression += coefficient * scipVar
            scipExpression += constant
            yield scipExpression

    def _scalar_affinexp_pic2scip(self, picosExpression):
        """Transform a PICOS scalar affine expression into a SCIP expression.

        :returns: A :class:`SCIP expression <pyscipopt.scip.Expr>`.
        """
        assert len(picosExpression) == 1
        return next(self._affinexp_pic2scip(picosExpression))

    def _quadexp_pic2scip(self, picosExpression):
        # Convert affine part.
        scipExpression = self._scalar_affinexp_pic2scip(picosExpression.aff)

        # Convert quadratic part.
        for (pVar1, pVar2), pCoefficients \
        in picosExpression.quadratic_forms.items():
            for sparseIndex in range(len(pCoefficients)):
                localVar1Index   = pCoefficients.I[sparseIndex]
                localVar2Index   = pCoefficients.J[sparseIndex]
                localCoefficient = pCoefficients.V[sparseIndex]
                scipVar1 = self._scipVar[pVar1.id_at(localVar1Index)]
                scipVar2 = self._scipVar[pVar2.id_at(localVar2Index)]
                scipExpression += localCoefficient * scipVar1 * scipVar2

        return scipExpression

    def _import_linear_constraint(self, picosConstraint):
        assert isinstance(picosConstraint, AffineConstraint)

        scipCons = []
        picosLHS = picosConstraint.lhs - picosConstraint.rhs
        for scipLHS in self._affinexp_pic2scip(picosLHS):
            if picosConstraint.is_increasing():
                scipCons.append(self.int.addCons(scipLHS <= 0.0))
            elif picosConstraint.is_decreasing():
                scipCons.append(self.int.addCons(scipLHS >= 0.0))
            elif picosConstraint.is_equality():
                scipCons.append(self.int.addCons(scipLHS == 0.0))
            else:
                assert False, "Unexpected constraint relation."

        return scipCons

    def _import_quad_constraint(self, picosConstraint):
        assert isinstance(picosConstraint,
            (ConvexQuadraticConstraint, NonconvexQuadraticConstraint))

        scipLHS  = self._quadexp_pic2scip(picosConstraint.le0)
        scipCons = [self.int.addCons(scipLHS <= 0.0)]

        return scipCons

    def _import_socone_constraint(self, picosConstraint):
        scipCons = []
        scipQuadLHS = self._quadexp_pic2scip(
            (picosConstraint.ne | picosConstraint.ne)
            - (picosConstraint.ub * picosConstraint.ub))
        scipCons.append(self.int.addCons(scipQuadLHS <= 0.0))

        scipAuxLHS = self._scalar_affinexp_pic2scip(picosConstraint.ub)
        if scipAuxLHS.degree() > 0:
            scipCons.append(self.int.addCons(scipAuxLHS >= 0.0))

        return scipCons

    def _import_rscone_constraint(self, picosConstraint):
        scipCons = []
        scipLHS = self._quadexp_pic2scip(
            (picosConstraint.ne | picosConstraint.ne)
            - (picosConstraint.ub1 * picosConstraint.ub2))
        scipCons.append(self.int.addCons(scipLHS <= 0.0))

        # Make sure that either the RHS is constant, or one of the two
        # expressions is non-negative.
        scipAuxLHS = self._scalar_affinexp_pic2scip(picosConstraint.ub1)
        if scipAuxLHS.degree() > 0:
            scipCons.append(self.int.addCons(scipAuxLHS >= 0.0))
        else:
            scipAuxLHS = self._scalar_affinexp_pic2scip(picosConstraint.ub2)
            if scipAuxLHS.degree() > 0:
                scipCons.append(self.int.addCons(scipAuxLHS >= 0.0))

        return scipCons

    def _import_constraint(self, picosConstraint):
        # Import constraint based on type.
        if isinstance(picosConstraint, AffineConstraint):
            scipCons = self._import_linear_constraint(picosConstraint)
        elif isinstance(picosConstraint,
                (ConvexQuadraticConstraint, NonconvexQuadraticConstraint)):
            scipCons = self._import_quad_constraint(picosConstraint)
        elif isinstance(picosConstraint, SOCConstraint):
            scipCons = self._import_socone_constraint(picosConstraint)
        elif isinstance(picosConstraint, RSOCConstraint):
            scipCons = self._import_rscone_constraint(picosConstraint)
        else:
            assert False, "Constraint type belongs to unsupported problem type."

        # Map PICOS constraints to lists of SCIP constraints.
        self._scipCons[picosConstraint] = scipCons

    def _import_objective(self):
        picosSense, picosObjective = self.ext.no

        # Retrieve objective sense.
        if picosSense == "min":
            scipSense = "minimize"
        else:
            assert picosSense == "max"
            scipSense = "maximize"

        # Import objective function.
        scipObjective = self._scalar_affinexp_pic2scip(picosObjective)

        # HACK: Remove a constant term from the objective as this is not allowed
        #       by SCIP under Python 2. (Not sure if the term is stored or
        #       dropped under Python 3, but no exception is thrown there.)
        from pyscipopt.scip import Term
        constantTerm = Term()
        if constantTerm in scipObjective.terms:
            scipObjective.terms.pop(constantTerm)

        self.int.setObjective(scipObjective, scipSense)

    def _import_problem(self):
        import pyscipopt as scip

        # Create a problem instance.
        self.int = scip.Model()

        # Import variables.
        for variable in self.ext.variables.values():
            self._import_variable(variable)

        # Import constraints.
        for constraint in self.ext.constraints.values():
            self._import_constraint(constraint)

        # Set objective.
        self._import_objective()

    def _update_problem(self):
        # TODO: Support all problem updates supported by SCIP.
        raise NotImplementedError

    def _solve(self):
        import pyscipopt as scip

        # TODO: Give Problem an interface for checks like this.
        isLP = isinstance(self.ext.no.function, AffineExpression) \
            and all(isinstance(constraint, AffineConstraint)
            for constraint in self.ext.constraints.values())

        # Reset options.
        self.int.resetParams()

        # verbosity
        picosVerbosity = self.verbosity()
        if picosVerbosity <= -1:
            scipVerbosity = 0
        elif picosVerbosity == 0:
            scipVerbosity = 2
        elif picosVerbosity == 1:
            scipVerbosity = 3
        elif picosVerbosity >= 2:
            scipVerbosity = 5
        self.int.setIntParam("display/verblevel", scipVerbosity)

        # abs_prim_fsb_tol
        if self.ext.options.abs_prim_fsb_tol is not None:
            self.int.setRealParam("numerics/lpfeastol",
                self.ext.options.abs_prim_fsb_tol)

        # abs_dual_fsb_tol
        if self.ext.options.abs_dual_fsb_tol is not None:
            self.int.setRealParam("numerics/dualfeastol",
                self.ext.options.abs_dual_fsb_tol)

        # rel_prim_fsb_tol, rel_dual_fsb_tol
        relFsbTols = [tol for tol in (self.ext.options.rel_prim_fsb_tol,
            self.ext.options.rel_dual_fsb_tol) if tol is not None]
        if relFsbTols:
            self.int.setRealParam("numerics/feastol", min(relFsbTols))

        # abs_ipm_opt_tol, abs_bnb_opt_tol
        absOptTols = [tol for tol in (self.ext.options.abs_ipm_opt_tol,
            self.ext.options.abs_bnb_opt_tol) if tol is not None]
        if absOptTols:
            self.int.setRealParam("limits/absgap", min(absOptTols))

        # rel_ipm_opt_tol, rel_bnb_opt_tol
        relOptTols = [tol for tol in (self.ext.options.rel_ipm_opt_tol,
            self.ext.options.rel_bnb_opt_tol) if tol is not None]
        if relOptTols:
            self.int.setRealParam("limits/gap", min(relOptTols))

        # timelimit
        if self.ext.options.timelimit is not None:
            self.int.setRealParam("limits/time", self.ext.options.timelimit)

        # treememory
        if self.ext.options.treememory is not None:
            self.int.setRealParam("limits/memory", self.ext.options.treememory)

        # max_fsb_nodes
        if self.ext.options.max_fsb_nodes is not None:
            self.int.setRealParam(
                "limits/solutions", float(self.ext.options.max_fsb_nodes))

        # Handle SCIP-specific options.
        for option, value in self.ext.options.scip_params.items():
            try:
                if isinstance(value, bool):
                    self.int.setBoolParam(option, value)
                elif isinstance(value, str):
                    if len(value) == 1:
                        try:
                            self.int.setCharParam(option, ord(value))
                        except LookupError:
                            self.int.setStringParam(option, value)
                    else:
                        self.int.setStringParam(option, value)
                elif isinstance(value, float):
                    self.int.setRealParam(option, value)
                elif isinstance(value, int):
                    try:
                        self.int.setIntParam(option, value)
                    except LookupError:
                        try:
                            self.int.setLongintParam(option, value)
                        except LookupError:
                            self.int.setRealParam(option, float(value))
            except KeyError:
                self._handle_bad_option_value("scip_params",
                    "SCIP option '{}' does not exist.".format(option))
            except ValueError:
                self._handle_bad_option_value("scip_params",
                    "Invalid value '{}' for SCIP option '{}'."
                    .format(value, option))
            except LookupError:
                self._handle_bad_option_value("scip_params",
                    "Failed to guess type of SCIP option '{}'.".format(option))

        # Handle unsupported options.
        self._handle_unsupported_options(
            "hotstart", "lp_node_method", "lp_root_method", "max_iterations")

        # In the case of a pure LP, disable presolve to get duals.
        if self.ext.options.duals is not False and isLP:
            self._debug("Disabling SCIP's presolve, heuristics, and propagation"
                " features to allow for LP duals.")

            self.int.setPresolve(scip.SCIP_PARAMSETTING.OFF)
            self.int.setHeuristics(scip.SCIP_PARAMSETTING.OFF)

            # Note that this is a helper to set options, so they get reset at
            # the beginning of the function instead of in the else-scope below.
            self.int.disablePropagation()
        else:
            self.int.setPresolve(scip.SCIP_PARAMSETTING.DEFAULT)
            self.int.setHeuristics(scip.SCIP_PARAMSETTING.DEFAULT)

        # Attempt to solve the problem.
        with self._header(), self._stopwatch():
            self.int.optimize()

        # Retrieve primals.
        primals = {}
        if self.ext.options.primals is not False:
            for picosVar in self.ext.variables.values():
                value = []
                for localIndex in range(picosVar.dim):
                    scipVar = self._scipVar[picosVar.id_at(localIndex)]
                    value.append(self.int.getVal(scipVar))

                primals[picosVar] = value

        # Retrieve duals for LPs.
        duals = {}
        if self.ext.options.duals is not False and isLP:
            for picosConstraint in self.ext.constraints.values():
                assert isinstance(picosConstraint, AffineConstraint)

                # Retrieve dual value for constraint.
                scipDuals = []
                for scipCon in self._scipCons[picosConstraint]:
                    scipDuals.append(self.int.getDualsolLinear(scipCon))
                picosDual = cvxopt.matrix(scipDuals, picosConstraint.size)

                # Flip sign based on constraint relation.
                if picosConstraint.is_decreasing():
                    picosDual = -picosDual

                # Flip sign based on objective sense.
                if picosDual and self.ext.no.direction == "min":
                    picosDual = -picosDual

                duals[picosConstraint] = picosDual

        # # Retrieve objective value.
        # objectiveValue = self.int.getObjVal()
        #
        # # HACK: Add back the constant objective term; see above.
        # picosObjective = self.ext.no.function
        # picosObjectiveAffinePart = picosObjective.aff \
        #     if isinstance(picosObjective, QuadExp) else picosObjective
        # if picosObjectiveAffinePart.constant:
        #     objectiveValue += picosObjectiveAffinePart.constant[0]

        status = self.int.getStatus()
        if   status == "optimal":
            primalStatus   = SS_OPTIMAL
            dualStatus     = SS_OPTIMAL
            problemStatus  = PS_FEASIBLE
        elif status == "timelimit":
            primalStatus   = SS_PREMATURE
            dualStatus     = SS_PREMATURE
            problemStatus  = PS_UNKNOWN
        elif status == "infeasible":
            primalStatus   = SS_INFEASIBLE
            dualStatus     = SS_UNKNOWN
            problemStatus  = PS_INFEASIBLE
        elif status == "unbounded":
            primalStatus   = SS_UNKNOWN
            dualStatus     = SS_INFEASIBLE
            problemStatus  = PS_UNBOUNDED
        else:
            primalStatus   = SS_UNKNOWN
            dualStatus     = SS_UNKNOWN
            problemStatus  = PS_UNKNOWN

        return self._make_solution(
            primals, duals, primalStatus, dualStatus, problemStatus)


# --------------------------------------
__all__ = api_end(_API_START, globals())
