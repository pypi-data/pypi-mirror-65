# coding: utf-8

# ------------------------------------------------------------------------------
# Copyright (C) 2018 Maximilian Stahlberg
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

"""Backend for constraint type implementations."""

import random
import threading

import cvxopt

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_property, empty_cache
from ..compat import ABC, abstractmethod
from ..containers import DetailedType

_API_START = api_start(globals())
# -------------------------------


# The constraint IDs start at a random value to prevent a clash if constraints
# are are pickled and loaded in another python session.
_LAST_CONSTRAINT_ID = int(random.getrandbits(31))

# A lock for _LAST_CONSTRAINT_ID, if the user threads to create constraints.
_CONSTRAINT_ID_LOCK = threading.Lock()


def _make_constraint_id():
    """Create a unique ID for a new constraint."""
    with _CONSTRAINT_ID_LOCK:
        global _LAST_CONSTRAINT_ID
        _LAST_CONSTRAINT_ID += 1
        return _LAST_CONSTRAINT_ID


class ConstraintType(DetailedType):
    """Container for a pair of constraint class type and constraint subtype."""

    pass


class Constraint(ABC):
    """Abstract base class for optimization constraints.

    Implementations

        * need to implement at least the abstract methods ``_str``,
          ``_expression_names``, and ``_get_slack``,
        * need to implement ``_get_size``, unless duals are not supported, and
        * are supposed to call :meth:`Constraint.__init__` from within their own
          implementation of ``__init__``.
    """

    LE = "<"
    GE = ">"
    EQ = "="

    def __init__(self, typeTerm, customString=None, printSize=False):
        """Perform basic initialization for :class:`Constraint` instances.

        :param str typeTerm: Short string denoting the constraint type.
        :param str customString: Optional string description.
        :param bool printSize: Whether to include the constraint's shape in its
            representation string.
        """
        self.typeTerm     = typeTerm
        self.customString = customString
        self.printSize    = printSize

        self._id = _make_constraint_id()

        self.name  = None
        self._dual = None

    @property
    def type(self):
        """Detailed type of the constraint.

        The detailed type of the constraint, which is suffcient to predict the
        outcome (detailed types and quantities of auxilary variables and
        constraints) of any constraint conversion.
        """
        return ConstraintType(self.__class__, self._subtype())

    subtype = property(lambda self: self._subtype())

    @classmethod
    def make_type(cls, *args, **kwargs):
        """Create a detailed constraint type from subtype parameters."""
        return ConstraintType(cls, cls.Subtype(*args, **kwargs))

    @abstractmethod
    def _subtype(self):
        """Subtype of the constraint.

        :returns: A hashable object that, together with the constraint class,
            is sufficient to predict the outcome (detailed types and quantities
            of auxilary variables and constraints) of any constraint conversion.
        """
        pass

    @classmethod
    @abstractmethod
    def _cost(cls, subtype):
        r"""Report an estimate number of real constraint matrix rows occupied.

        Given the subtype of a constraint, returns an estimate on the number of
        rows that a constraint with this subtype would occupy in the constraint
        matrix of a (hypothetical) solver that supports direct input of such a
        constraint.

        Some conventions:

        - For a conic constraint, this is the cone's dimensionality.
        - For a (complex) affine equality :math:`A = B`, this is the number of
          elements in the matrix :math:`A - B` (times two).
        - For a constraint that poses a bound on a scalar function on an
          :math:`n`-dimensional vector space, this is :math:`n + 1` (:math:`1`
          for the affine bound).
        - In particular, a bound on a function of symmetric (hermitian) matrices
          occupies :math:`\frac{n(n + 1)}{2} + 1` (:math:`n^2 + 1`) rows.
        - For a quadratic constraint, this is the number of coefficients in the
          simplified quadratic form, plus one (for the affine part).
        """
        pass

    def __hash__(self):
        """Return the unique ID."""
        return self._id

    def __eq__(self, other):
        """Whether the unique IDs equal."""
        return self._id == other._id

    def __repr__(self):
        if self.printSize:
            return glyphs.repr2("{} {} Constraint".format(
                glyphs.size(*self.size), self.typeTerm), self.__str__())
        else:
            return glyphs.repr2("{} Constraint".format(self.typeTerm),
                self.__str__())

    def __str__(self):
        return "{}{}".format(
            self.customString if self.customString else self._str(),
            " ({})".format(self.name) if self.name else "")

    def __len__(self):
        """Return number of scalar Lagrange dual variables."""
        return self.size[0] * self.size[1]

    @property
    def id(self):
        """The unique ID of the constraint, assigned at creation.

        The ID is kept when the constraint is copied via
        :meth:`replace_variables`, so that the copy can be identified with the
        original despite pointing to different expressions and variable objects.
        """
        return self._id

    @abstractmethod
    def _expression_names(self):
        """Attribute names of the expressions stored in the constraint."""
        pass

    @abstractmethod
    def _str(self):
        """Algebraic representation of the constraint."""
        pass

    def _get_size(self):
        """Langrange dual variable shape.

        The dimensionality of the constraint, more precisely the dimensionality
        of its Lagrange dual variable, as a pair.
        """
        raise NotImplementedError(
            "{} does not define a constraint (dual value) dimensionality."
            .format(self.__class__.__name__))

    @abstractmethod
    def _get_slack(self):
        """Value of a slack variable or of the negative constraint violation.

        A negative value whose absolute value corresponds to the amount of
        violation, if the constraint is violated, or a non-negative value that
        corresponds to the value of a slack variable, otherwise.
        """
        pass

    def _wrap_get_slack(self):
        """Convert a scalar slack value to float.

        A wrapper retrieving the slack in a consistent manner: If it is a scalar
        value, it is returned as a float, otherwise as a
        :class:`CVXOPT matrix <cvxopt.matrix>`.
        """
        slack = self._get_slack()

        if isinstance(slack, float):
            return slack

        assert isinstance(slack, cvxopt.matrix), "Constraints need to return " \
            "the slack as either a float or a CVXOPT matrix."

        if slack.size == (1, 1):
            return float(slack[0])
        else:
            return slack

    def _get_dual(self):
        return self._dual

    def _set_dual(self, value):
        """Store a constraint's dual value.

        Stores a dual solution value for the dual variable corresponding to the
        constraint in a consistent manner.

        Duals for multidmensional constraints are stored as a
        :class:`CVXOPT matrix <cvxopt.matrix>` while duals for scalar
        constraints are stored as a float.
        """
        if value is None:
            self._dual = None
        elif type(value) in (int, float, complex):
            if len(self) != 1:
                raise ValueError("Incompatible dimensions of dual value: "
                    "Expected {} but got a scalar.".format(self.size))

            self._dual = value
        else:
            try:
                dual = cvxopt.matrix(value, self.size)
            except TypeError:
                raise ValueError("Incompatible dimensions of dual value for {}:"
                    " Expected {} and got container of size {}."
                    .format(self.__class__.__name__, glyphs.size(*self.size),
                    len(value)))

            self._dual = dual[0] if len(dual) == 1 else dual

    size  = property(lambda self: self._get_size(), doc=_get_size.__doc__)
    slack = property(lambda self: self._wrap_get_slack(),
        doc=_get_slack.__doc__)
    dual  = property(lambda self: self._get_dual(), _set_dual)
    """Value of the constraint's Lagrange dual variable."""

    def delete(self):
        """Raise a :exc:`NotImplementedError`.

        Formerly this would remove the constraint from the single problem it is
        assigned to, if any.

        .. deprecated:: 2.0

            Both variables and constraints have been decoupled from problems:
            Both may safely appear in multiple problems but at the same time
            they do not know which problems they were added to. To remove a
            constraint from a problem, you have to call its
            :meth:`~picos.modeling.problem.Problem.remove_constraint` method.
        """
        raise NotImplementedError("Telling a constraint to remove itself from "
            "problems is not possible anymore, use Problem.remove_constraint "
            "on selected problems instead.")

    # TODO: Solve this with inspection instead of _expression_names?
    # TODO: Is this even needed for anything apart from variables and
    #       replace_variables? If not, maybe just implement those two with
    #       every constraint just like for expressions?
    @property
    def expressions(self):
        """Yield expressions stored with the constraint."""
        for name in self._expression_names():
            yield getattr(self, name)

    @cached_property
    def variables(self):
        """All variables referenced by the constraint."""
        vars = frozenset()
        for expression in self.expressions:
            vars = vars.union(expression.variables)
        return vars

    def replace_variables(self, new_variables):
        """Make the constraint concern a different set of variables.

        See :meth:`~.expression.Expression.replace_variables` for more.
        """
        from copy import copy

        theCopy = copy(self)

        # TODO: Reset any dual value assigned to the constraint?
        # theCopy._dual = None

        # Clear the cache of the copy as it can reference old variables.
        empty_cache(theCopy)

        # Rewrite expressions.
        for name in theCopy._expression_names():
            expression = getattr(self, name)
            new_expression = expression.replace_variables(new_variables)
            setattr(theCopy, name, new_expression)

        # HACK: Delete a custom string because it can contain old variable
        #       names. In particular Norm uses it when creating a SOCConstraint.
        # TODO: Get rid of custom strings.
        theCopy.customString = None

        return theCopy

    # TODO: Evaluate uses of this method.
    def constring(self):
        """Return an algebraic string representation of the constraint."""
        return self._str()

    # TODO: Re-implement pretty printing for problems.
    def keyconstring(self):
        """Return the regular string representation."""
        return self.__str__()

    def _assure_lhs_rhs_relation(self):
        if not hasattr(self, "relation") or not hasattr(self, "lhs") \
        or not hasattr(self, "rhs"):
            raise TypeError("{} does not explicitly define a relation "
                "between a left hand side and a right hand side expression."
                .format(self.__class__.__name__))

    def is_equality(self):
        """Whether the constraints states an equality."""
        self._assure_lhs_rhs_relation()
        return self.relation == self.EQ

    def is_inequality(self):
        """Whether the constraints states an inequality."""
        self._assure_lhs_rhs_relation()
        return self.relation != self.EQ

    def is_increasing(self):
        """Whether the left side is posed smaller or equal than the right."""
        self._assure_lhs_rhs_relation()
        return self.relation == self.LE

    def is_decreasing(self):
        """Whether the left side is posed greater or equal than the right."""
        self._assure_lhs_rhs_relation()
        return self.relation == self.GE


class ConstraintConversion(ABC):
    """Recipe for conversion from one constraint to a set of other constraints.

    Implementations of this class are defined within the class body of a
    Constraint implementation to tell PICOS' reformulation framework how that
    constraint can be reformulated into a number of other constraints and
    auxiliary variables.

    Implementation class names must end in ``Conversion``, and in particular may
    be called just ``Conversion``. If for instance
    :class:`AbsoluteValueConstraint <picos.constraints.AbsoluteValueConstraint>`
    defines :class:`AffineConversion
    <picos.constraints.AbsoluteValueConstraint.AffineConversion>`, then the
    reformulation will be coined ``AbsoluteValueToAffineReformulation``. If the
    conversions was just named ``Conversion``, the result would be a class named
    ``AbsoluteValueReformulation``.
    """

    @classmethod
    @abstractmethod
    def predict(cls, subtype, options):
        """Predict the outcome of a constraint conversion.

        :param object subtype: A hashable object as could be returned by the
            ``_subtype`` method of the parent constraint implementation.
        :param ~picos.Options options: Solution options to assume used.
        :yields: Records to be added to a problem footprint when an instance of
            the parent constraint with the given subtype is converted according
            to this conversion.
        """
        pass

    # TODO: Make this yield variables and constraints instad of returning a
    #       Problem instance (this was not possible with the old expressions).
    @classmethod
    @abstractmethod
    def convert(cls, constraint, options):
        """Convert a given constraint.

        Returns a temporary problem instance that contains auxilary constraints
        and variables replacing the given constraint.
        """
        pass

    @classmethod
    def dual(cls, auxVarPrimals, auxConDuals, options):
        """Convert back the dual value of a constraint that was converted.

        Given a mapping of auxilary variable names (as named in :meth:`convert`)
        to primals and a list of auxilary constraint duals (in the order as the
        constraints were added in :meth:`convert`), returns a dual value for the
        converted constraint.

        :raises NotImplementedError: When dual format not decided upon or not
            known. This will be caught by the reformulation's backward method.
        """
        raise NotImplementedError(
            "{} does not describe how to convert back the dual.".format(
            cls.__qualname__ if hasattr(cls, "__qualname__") else cls.__name__))

    def __init__(self):
        """Raise a :exc:`TypeError` on instanciation."""
        raise TypeError("Constraint conversion classes are not supposed to be "
            "instanciated.")


# --------------------------------------
__all__ = api_end(_API_START, globals())
