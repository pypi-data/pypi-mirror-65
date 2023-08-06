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

"""Backend for mathematical set type implementations."""

from .. import glyphs
from ..apidoc import api_end, api_start
from ..compat import ABC, abstractmethod
from .expression import ExpressionType

_API_START = api_start(globals())
# -------------------------------


class SetType(ExpressionType):
    """:class:`~picos.expressions.ExpressionType` for sets."""

    pass


class Set(ABC):
    """Abstract base class for mathematical set expressions."""

    def __init__(self, typeStr, symbStr):
        """Perform basic initialization for :class:`Set` instances.

        :param str typeStr: Short string denoting the set type.
        :param str symbStr: Algebraic string description of the set.
        """
        self._typeStr = typeStr
        self._symbStr = symbStr

    @property
    def string(self):
        """Symbolic string representation of the set."""
        return self._symbStr

    @property
    @abstractmethod
    def Subtype(self):
        """See :meth:`picos.expressions.Expression.Subtype`."""
        pass

    @property
    def type(self):
        """See :meth:`picos.expressions.Expression.type`."""
        return ExpressionType(self.__class__, self._get_subtype())

    @property
    def subtype(self):
        """See :meth:`picos.expressions.Expression.subtype`."""
        return self._get_subtype()

    @property
    def refined(self):
        """The set itself, as sets do not support refinement.

        This exists for compatibility with expressions.
        """
        return self

    def __repr__(self):
        return str(glyphs.repr2(self._typeStr, self._symbStr))

    def __str__(self):
        return str(self._symbStr)

    def __format__(self, format_spec):
        return self._symbStr.__format__(format_spec)

    @abstractmethod
    def __rshift__(self, element):
        """Return the constraint that the element is in the set."""
        pass

    @abstractmethod
    def _get_subtype(self):
        """:meth:`picos.expressions.Expression._get_subtype`."""
        pass

    @classmethod
    @abstractmethod
    def _predict(cls, subtype, relation, other):
        """See :meth:`picos.expressions.Expression._predict`."""
        pass

    @abstractmethod
    def _get_variables(self):
        """Return a Python set of variables that are involved in the set."""
        pass

    variables = property(
        lambda self: self._get_variables(),
        doc=_get_variables.__doc__)

    @abstractmethod
    def _replace_variables(self, var_map):
        """See :meth:`~.expression.Expression._replace_variables`."""
        pass

    # HACK: Borrow Expression.replace_variables.
    # TODO: Common base class ExpressionOrSet.
    def replace_variables(self, new_variables):
        """See :meth:`~.expression.Expression.replace_variables`."""
        from .expression import Expression
        return Expression.replace_variables(self, new_variables)


# --------------------------------------
__all__ = api_end(_API_START, globals())
