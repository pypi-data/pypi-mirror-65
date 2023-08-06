# coding: utf-8

# ------------------------------------------------------------------------------
# Copyright (C) 2019 Maximilian Stahlberg
# Based on the original picos.expressions module by Guillaume Sagnol.
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

"""Mathematical expression types."""

from ..apidoc import api_end, api_start

_API_START = api_start(globals())
# -------------------------------


from .algebra import *  # noqa
from .exp_affine import (AffineExpression, ComplexAffineExpression,  # noqa
                         Constant)
from .exp_detrootn import DetRootN  # noqa
from .exp_entropy import Entropy, NegativeEntropy  # noqa
from .exp_geomean import GeometricMean  # noqa
from .exp_logarithm import Logarithm  # noqa
from .exp_logsumexp import LogSumExp  # noqa
from .exp_norm import Norm, SpectralNorm, NuclearNorm  # noqa
from .exp_powtrace import PowerTrace  # noqa
from .exp_quadratic import QuadraticExpression  # noqa
from .exp_sumexp import SumExponentials  # noqa
from .exp_sumxtr import SumExtremes  # noqa
from .expression import Expression, ExpressionType, NotValued  # noqa
from .variables import (BaseVariable, BinaryVariable, ComplexVariable,  # noqa
                        HermitianVariable, IntegerVariable,
                        LowerTriangularVariable, RealVariable,
                        SkewSymmetricVariable, SymmetricVariable,
                        UpperTriangularVariable, CONTINUOUS_VARTYPES)
from .set import Set, SetType  # noqa
from .set_ball import Ball  # noqa
from .set_expcone import ExponentialCone  # noqa
from .set_simplex import Simplex  # noqa
from .set_soc import SecondOrderCone  # noqa
from .set_rsoc import RotatedSecondOrderCone  # noqa


# --------------------------------------
__all__ = api_end(_API_START, globals())
