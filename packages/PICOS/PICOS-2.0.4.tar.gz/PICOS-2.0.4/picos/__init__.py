# coding: utf-8

# ------------------------------------------------------------------------------
# Copyright (C) 2012-2017 Guillaume Sagnol
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

"""A Python Interface to Conic Optimization Solvers.

The :mod:`picos` namespace gives you quick access to the most important classes
and functions for optimizing with PICOS, so that ``import picos`` is often
sufficient for implementing your model.
"""

import os

from .apidoc import api_start, api_end


_API_START = api_start(globals())
# -------------------------------


# Character set changes.
from .glyphs import ascii, latin1, unicode, default as default_charset  # noqa

# Model setup.
from .modeling import (find_assignment, maximize, minimize, Objective,  # noqa
                       Options, Problem, Solution)

# Constants.
from .expressions import Constant  # noqa

# Variables.
from .expressions.variables import (  # noqa
    BinaryVariable, ComplexVariable, HermitianVariable, IntegerVariable,
    LowerTriangularVariable, RealVariable, SkewSymmetricVariable,
    SymmetricVariable, UpperTriangularVariable)

# Sets.
from .expressions import (  # noqa
    Ball, ExponentialCone, SecondOrderCone, Simplex, RotatedSecondOrderCone)

# Algebraic function-like classes.
from .constraints import FlowConstraint  # noqa
from .expressions import (  # noqa
    DetRootN, Entropy, GeometricMean, Logarithm, LogSumExp,
    NegativeEntropy, Norm, SpectralNorm, NuclearNorm, PowerTrace,
    SumExtremes, SumExponentials)

# Algebraic functions, including legacy ones.
from .expressions.algebra import *  # noqa

# Utilities.
from .expressions.data import value  # noqa
from .solvers import available_solvers  # noqa

# Non-algebraic legacy imports.
from .modeling.file_in import import_cbf  # noqa

# Exceptions.
from .modeling import SolutionFailure  # noqa
from .expressions import NotValued  # noqa


_LOCATION = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
_VERSION_FILE = os.path.join(_LOCATION, ".version")


def _get_version_info():
    with open(_VERSION_FILE, "r") as versionFile:
        return tuple(versionFile.read().strip().split("."))


__version_info__ = _get_version_info()
__version__ = '.'.join(__version_info__)


# --------------------------------------
__all__ = api_end(_API_START, globals())
