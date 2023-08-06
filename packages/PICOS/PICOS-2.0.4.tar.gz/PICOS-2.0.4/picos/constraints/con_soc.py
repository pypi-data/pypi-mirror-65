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

"""Second order conce constraints."""

from collections import namedtuple

from .. import glyphs
from ..apidoc import api_end, api_start
from .constraint import Constraint

_API_START = api_start(globals())
# -------------------------------


class SOCConstraint(Constraint):
    """Second order (:math:`2`-norm, Lorentz) cone membership constraint."""

    def __init__(self, normedExpression, upperBound, customString=None):
        """Construct a :class:`SOCConstraint`.

        :param ~picos.expressions.AffineExpression normedExpression:
            Expression under the norm.
        :param ~picos.expressions.AffineExpression upperBound:
            Upper bound on the normed expression.
        :param str customString:
            Optional string description.
        """
        from ..expressions import AffineExpression

        assert isinstance(normedExpression, AffineExpression)
        assert isinstance(upperBound, AffineExpression)
        assert len(upperBound) == 1

        # NOTE: len(normedExpression) == 1 is allowed even though this should
        #       rather be represented as an AbsoluteValueConstraint.

        self.ne = normedExpression
        self.ub = upperBound

        super(SOCConstraint, self).__init__(
            self._get_type_term(), customString, printSize=True)

    def _get_type_term(self):
        return "SOC"

    Subtype = namedtuple("Subtype", ("argdim",))

    def _subtype(self):
        return self.Subtype(len(self.ne))

    @classmethod
    def _cost(cls, subtype):
        return subtype.argdim + 1

    def _expression_names(self):
        yield "ne"
        yield "ub"

    def _str(self):
        return glyphs.le(glyphs.norm(self.ne.string), self.ub.string)

    def _get_size(self):
        return (len(self.ne) + 1, 1)

    def _get_slack(self):
        return self.ub.value - abs(self.ne).value


# --------------------------------------
__all__ = api_end(_API_START, globals())
