# coding: utf-8

# ------------------------------------------------------------------------------
# Copyright (C) 2017 Maximilian Stahlberg
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

"""Implementation of :class:`SMCPSolver`."""

# ------------------------------------------------------------------------------
# This file is a skeleton implementation for the SMCP solver.
# Currently, the funcional implementation is found in CVXOPTSolver.
# ------------------------------------------------------------------------------

from ..apidoc import api_end, api_start
from ..compat import assert_import_exists
from ..constraints import AffineConstraint, LMIConstraint
from ..expressions import CONTINUOUS_VARTYPES, AffineExpression
from ..modeling.footprint import Specification
from .solver import Solver
from .solver_cvxopt import CVXOPTSolver

_API_START = api_start(globals())
# -------------------------------


class SMCPSolver(CVXOPTSolver):
    """Interface to the SMCP solver.

    Most of the logic is implemented in the
    :class:`CVXOPTSolver <picos.solvers.solver_cvxopt.CVXOPTSolver>` base class.
    """

    SUPPORTED = Specification.compile(
        directions=Specification.ALL,
        objectives=[
            AffineExpression],
        variables=CONTINUOUS_VARTYPES,
        constraints=[
            AffineConstraint,
            # TODO: See below.
            # SOCConstraint,
            # RSOCConstraint,
            LMIConstraint])

    @classmethod
    def supports(cls, footprint):
        """Implement :meth:`~.solver.Solver.supports`."""
        if not Solver.supports(footprint):
            return False

        # TODO: SMCP formally supports problems that are not SDPs, but it is
        #       known to perform poorly for them, sometimes even returning
        #       incorrect solutions. For now, only support SDPs.
        if not ("con", LMIConstraint) in footprint:
            return False

        return footprint << cls.SUPPORTED

    @classmethod
    def default_penalty(cls):
        """Implement :meth:`~.solver.Solver.default_penalty`."""
        return 2.0  # Experimental free/open source solver.

    @classmethod
    def test_availability(cls):
        """Implement :meth:`~.solver.Solver.test_availability`."""
        assert_import_exists("smcp")

    @classmethod
    def names(cls):
        """Implement :meth:`~.solver.Solver.names`."""
        return "smcp", "SMCP", "Sparse Matrix Cone Program Solver"

    @property
    def is_smcp(self):
        """Whether to implement SMCP instead of CVXOPT."""
        return True


# --------------------------------------
__all__ = api_end(_API_START, globals())
