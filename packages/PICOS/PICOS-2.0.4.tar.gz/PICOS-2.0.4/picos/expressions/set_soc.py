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

"""Implements :class:`SecondOrderCone`."""

import operator
from collections import namedtuple

from .. import glyphs
from ..apidoc import api_end, api_start
from ..constraints import SOCConstraint
from .data import convert_operands
from .exp_affine import AffineExpression
from .expression import refine_operands, validate_prediction
from .set import Set

_API_START = api_start(globals())
# -------------------------------


class SecondOrderCone(Set):
    r"""The second order cone.

    .. _lorentz:

    Also known as the quadratic, :math:`2`-norm, Lorentz, or ice cream cone.

    For :math:`n \in \mathbb{Z}_{\geq 2}`, represents the convex cone

    .. math::

        \mathcal{Q}^n = \left\{
            x \in \mathbb{R}^n
        ~\middle|~
            x_1 \geq \sqrt{\sum_{i = 2}^n x_i^2}
        \right\}.

    :Dual cone:

    The second order cone as defined above is self-dual.
    """

    def __init__(self):
        """Construct a second order cone."""
        typeStr = "Second Order Cone"
        symbStr = glyphs.set(glyphs.sep(
            glyphs.col_vectorize("t", "x"), glyphs.le(glyphs.norm("x"), "t")))

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
                if other.subtype.dim >= 2:
                    return SOCConstraint.make_type(other.subtype.dim - 1)

        return NotImplemented

    @convert_operands()
    @validate_prediction
    @refine_operands()
    def __rshift__(self, element):
        if isinstance(element, AffineExpression):
            if len(element) < 2:
                raise TypeError("Elements of the second order cone must be "
                    "at least two-dimensional.")

            element = element.vec

            return SOCConstraint(element[1:], element[0])
        else:
            return NotImplemented


# --------------------------------------
__all__ = api_end(_API_START, globals())
