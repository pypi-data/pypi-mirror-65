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

"""Implements :class:`ExponentialCone`."""

import operator
from collections import namedtuple

from .. import glyphs
from ..apidoc import api_end, api_start
from ..constraints import ExpConeConstraint
from .data import convert_operands
from .exp_affine import AffineExpression
from .expression import refine_operands, validate_prediction
from .set import Set

_API_START = api_start(globals())
# -------------------------------


class ExponentialCone(Set):
    r"""The exponential cone.

    Represents the convex cone
    :math:`\operatorname{cl}\{(x,y,z): y \exp(\frac{z}{y}) \leq x, x,y > 0\}`.
    """

    def __init__(self):
        """Construct an exponential cone."""
        typeStr = "Exponential Cone"
        symbStr = glyphs.closure(glyphs.set(glyphs.sep(
            glyphs.col_vectorize("x", "y", "z"), ", ".join([
                glyphs.le(
                    glyphs.mul("y", glyphs.exp(glyphs.div("z", "y"))), "x"),
                glyphs.gt("x", 0),
                glyphs.gt("y", 0)
            ]))))

        Set.__init__(self, typeStr, symbStr)

    def _get_variables(self):
        return set()

    def _replace_variables(self):
        return self

    Subtype = namedtuple("Subtype", ())

    def _get_subtype(self):
        return self.Subtype()

    @classmethod
    def _predict(cls, subtype, relation, other):
        assert isinstance(subtype, cls.Subtype)

        if relation == operator.__rshift__:
            if issubclass(other.clstype, AffineExpression):
                if other.subtype.dim == 3:
                    return ExpConeConstraint.make_type()

        return NotImplemented

    @convert_operands()
    @validate_prediction
    @refine_operands()
    def __rshift__(self, element):
        if isinstance(element, AffineExpression):
            if len(element) != 3:
                raise TypeError("Elements of the exponential cone must be "
                    "three-dimensional.")

            return ExpConeConstraint(element)
        else:
            return NotImplemented


# --------------------------------------
__all__ = api_end(_API_START, globals())
