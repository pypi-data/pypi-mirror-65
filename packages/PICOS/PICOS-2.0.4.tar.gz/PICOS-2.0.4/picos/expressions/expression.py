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

"""Backend for expression type implementations."""

import functools
import operator
import sys

import cvxopt

from .. import glyphs
from ..apidoc import api_end, api_start
from ..compat import ABC, abstractmethod
from ..constraints import ConstraintType
from ..containers import DetailedType
from ..legacy import deprecated

from .data import convert_operands

_API_START = api_start(globals())
# -------------------------------


class NotValued(RuntimeError):
    """The operation cannot be performed due to a variable without a value.

    Note that the :attr:`~picos.expressions.Expression.value` and
    :attr:`~picos.expressions.Expression.value_as_matrix` attributes do not
    raise this exception, but return :obj:`None`.
    """

    pass


class PredictedFailure(TypeError):
    """Denotes that comparing two expressions will not form a constraint."""

    pass


class ExpressionType(DetailedType):
    """The detailed type of an expression for predicting constraint outcomes.

    This is suffcient to predict the detailed type of any constraint that can be
    created by comparing with another expression.

    The prediction is done by using the relevant operator on instances of this
    class, as opposed to the expressions themselves. Note that operators used to
    create new expressions as opposed to constraints are not handled.
    """

    @staticmethod
    def _relation_str(relation):
        if relation is operator.__eq__:
            return "=="
        elif relation is operator.__le__:
            return "<="
        elif relation is operator.__ge__:
            return ">="
        elif relation is operator.__lshift__:
            return "<<"
        elif relation is operator.__rshift__:
            return ">>"
        else:
            return "??"

    @staticmethod
    def _swap_relation(relation):
        if relation is operator.__eq__:
            return operator.__eq__
        elif relation is operator.__le__:
            return operator.__ge__
        elif relation is operator.__ge__:
            return operator.__le__
        else:
            return None

    def _compare(self, relation, other):
        if not isinstance(other, ExpressionType):
            return NotImplemented  # Results in a regular Python TypeError.

        # Perform the forward prediction.
        result = self.clstype._predict(self.subtype, relation, other)

        # Fall back to the backward prediction.
        if result is NotImplemented:
            reverse = self._swap_relation(relation)
            result  = other.clstype._predict(other.subtype, reverse, self)

        # If both fail, the prediction is "not possible".
        if result is NotImplemented:
            raise PredictedFailure(
                "The statement {} {} {} is predicted to error."
                .format(self, self._relation_str(relation), other))
        else:
            assert isinstance(result, ConstraintType)
            return result

    def __eq__(self, other):
        return self._compare(operator.__eq__, other)

    def __le__(self, other):
        return self._compare(operator.__le__, other)

    __lt__ = __le__

    def __ge__(self, other):
        return self._compare(operator.__ge__, other)

    __gt__ = __ge__

    def __lshift__(self, other):
        return self._compare(operator.__lshift__, other)

    def __rshift__(self, other):
        return self._compare(operator.__rshift__, other)


class Expression(ABC):
    """Abstract base class for mathematical expressions, including variables.

    For variables, this is the secondary base class, with
    :class:`~.variables.BaseVariable` being the primary one.
    """

    def __init__(self, typeStr, symbStr):
        """Perform basic initialization for :class:`Expression` instances.

        :param str typeStr: Short string denoting the expression type.
        :param str symbStr: Algebraic string description of the expression.
        """
        self._typeStr = typeStr
        """A string describing the expression type."""

        self._symbStr = symbStr
        """A symbolic string representation of the expression. It is always used
        by __descr__, and it is equivalent to the value returned by __str__ when
        the expression is not fully valued."""

    @property
    def string(self):
        """Symbolic string representation of the expression.

        Use this over Python's :class:`str` if you want to output the symbolic
        representation even when the expression is valued.
        """
        return self._symbStr

    # --------------------------------------------------------------------------
    # Abstract and default-implementation methods.
    # --------------------------------------------------------------------------

    def _get_refined(self):
        """See :attr:`refined`."""
        return self

    def _get_clstype(self):
        """Return the Python class part of the expression's detailed type."""
        return self.__class__

    @property
    @abstractmethod
    def Subtype(self):
        """The class of which :attr:`subtype` returns an instance.

        Instances must be hashable. By convention a
        :func:`namedtuple <collections.namedtuple>` class.

        .. warning::
            This should be declared in the class body as e.g.
            `Subtype = namedtuple(…)` and not as a property so that it's static.
        """
        pass

    @abstractmethod
    def _get_subtype(self):
        """See :attr:`subtype`."""
        pass

    @classmethod
    @abstractmethod
    def _predict(cls, subtype, relation, other):
        """Predict the constraint outcome of a comparison.

        :param object subtype: An object returned by the :meth:`_get_subtype`
            instance method of :class:`cls`.
        :param method-wrapper relation: A function from the :mod:`operator`
            namespace, such as :func:`operator.__le__`. See
            :class:`ExpressionType` for what operators are defined.
        :param ExpressionType other: The detailed type of another expression.
        :returns: Either the :obj:`NotImplemented` token or a
            :class:`ConstraintType` object such that an instance of :class:`cls`
            with the given subtype, when compared with another expression with
            the given expression type, returns a constraint with that constraint
            type.
        """
        pass

    @abstractmethod
    def _get_value(self):
        """Return the numeric value of the expression as a CVXOPT matrix.

        :raises NotValued: When the value is not fully defined.

        Method implementations need to return an independent copy of the value
        that the user is allowed to change without affecting the expression.
        """
        pass

    def _set_value(self, value):
        raise NotImplementedError("Setting the value on an instance of {} is "
            "not supported, but you can value any variables involved instead."
            .format(type(self).__name__))

    def _get_shape(self):
        """Return the algebraic shape of the expression."""
        return (1, 1)

    @abstractmethod
    def _get_variables(self):
        """Return the set of variables that are involved in the expression."""
        pass

    @abstractmethod
    def _is_convex(self):
        """Whether the expression is convex."""
        pass

    @abstractmethod
    def _is_concave(self):
        """Whether the expression is concave."""
        pass

    @abstractmethod
    def _replace_variables(self, var_map):
        """Return a copy of the expression concerning different variables.

        This is the fast internal-use counterpart to :meth:`replace_variables`.

        :param dict var_map:
            Maps old to old or new variables. The map must be complete and sane,
            that is every variable involved in the expression must occur in the
            map and be mapped either to itself or another variable of same shape
            and vectorization format.
        """
        pass

    # --------------------------------------------------------------------------
    # An interface to the abstract and default-implementation methods above.
    # --------------------------------------------------------------------------

    def replace_variables(self, new_variables):
        """Return a copy of the expression concerning different variables.

        New variables must have the same shape and vectorization format as the
        variables that they replace. This means in particular that
        :class:`~.variables.RealVariable`, :class:`~.variables.IntegerVariable`
        and :class:`~.variables.BinaryVariable` of same shape are
        interchangeable.

        If the variables to be replaced do not appear in the expression, then
        the expression is not copied but returned as is.

        :param new_variables:
            Either a map from variables or variable names to new variables or an
            iterable of new variables to replace existing variables of same name
            with.
        :type new_variables:
            tuple or list or dict
        """
        old_variables = {var.name: var for var in self.variables}

        # Check unique naming of existing variables.
        if len(old_variables) != len(self.variables):
            raise RuntimeError("Cannot perform variable replacement on {} as "
                "its variables are not uniquely named.".format(self.string))

        # Obtain an existing variable to new variable mapping.
        if isinstance(new_variables, dict):
            # Replace keys that are variables with their respective names.
            new_new_variables = {
                (old if isinstance(old, str) else old.name): new_var
                for old, new_var in new_variables.items()}
            if len(new_new_variables) != len(new_variables):
                raise ValueError("New variables must have unique names.")
            new_variables = new_new_variables

            replacement = {old_variables[common_name]: new_var
                for common_name, new_var in new_variables.items()
                if common_name in old_variables}
        else:
            replacement = {old_variables[new_var.name]: new_var
                for new_var in new_variables if new_var.name in old_variables}

        if not replacement:
            return self

        # Validate replacement requirements.
        for old_var, new_var in replacement.items():
            if old_var.shape != new_var.shape:
                raise TypeError(
                    "Cannot replace {} with {} in {}: Differing shape."
                    .format(old_var.name, new_var.name, self.string))
            elif type(old_var._vec) != type(new_var._vec):  # noqa: E721
                raise TypeError(
                    "Cannot replace {} with {} in {}: Differing vectorization."
                    .format(old_var.name, new_var.name, self.string))

        var_map = {var: var for var in self.variables}
        var_map.update(replacement)

        return self._replace_variables(var_map)

    @property
    def refined(self):
        """A refined version of the expression.

        The refined expression can be an instance of a different
        :class:`Expression` subclass than the original expression, if that type
        is better suited for the mathematical object in question.

        The refined expression is automatically used instead of the original one
        whenever a constraint is created, and in some other places.

        The idea behind refined expressions is that operations that produce new
        expressions can be executed quickly without checking for exceptionnel
        cases. For instance, the sum of two
        :class:`~.exp_affine.ComplexAffineExpression` instances could have the
        complex part eliminated so that storing the result as an
        :class:`~.exp_affine.AffineExpression` would be prefered, but checking
        for this case on every addition would be too slow. Refinement is used
        sparingly to detect such cases at times where it makes the most sense.
        """
        fine = self._get_refined()

        if fine is not self:
            # Recursively refine until the expression doesn't change further.
            return fine.refined
        else:
            return fine

    @property
    def subtype(self):
        """The subtype part of the expression's detailed type.

        Returns a hashable object that, together with the Python class part of
        the expression's type, is sufficient to predict the constraint outcome
        (constraint class and subtype) of any comparison operation with any
        other expression.

        By convention the object returned is a
        :func:`namedtuple <collections.namedtuple>` instance.
        """
        return self._get_subtype()

    @property
    def type(self):
        """The expression's detailed type for constraint prediction.

        The returned value is suffcient to predict the detailed type of any
        constraint that can be created by comparing with another expression.

        Since constraints are created from
        :attr:`~picos.expressions.Expression.refined` expressions only, the
        Python class part of the detailed type may differ from the type of the
        expression whose :attr:`type` is queried.
        """
        refined = self.refined
        return ExpressionType(refined._get_clstype(), refined._get_subtype())

    @classmethod
    def make_type(cls, *args, **kwargs):
        """Create a detailed expression type from subtype parameters."""
        return ExpressionType(cls, cls.Subtype(*args, **kwargs))

    def _wrap_get_value(self, asMatrix):
        """Enhance the implementation of :attr:`_get_value`.

        This turns :exc:`NotValued` exceptions into a return value of
        :obj:`None` and checks the type of any value returned.

        :param bool asMatrix: Whether scalar values are returned as matrices.
        """
        try:
            value = self._get_value()
        except NotValued:
            return None

        assert isinstance(value, (cvxopt.matrix, cvxopt.spmatrix)), \
            "Expression._get_value implementations must return a CVXOPT matrix."

        if value.size == (1, 1) and not asMatrix:
            return value[0]
        else:
            return value

    value = property(
        lambda self: self._wrap_get_value(asMatrix=False),
        lambda self, x: self._set_value(x),
        lambda self: self._set_value(None),
        r"""Value of the expression.

        It is defined (not :obj:`None`) if the expression is constant or if all
        variables involved in the expression are valued. Variables can be valued
        directly by writing to their :attr:`value` attribute, or they can be
        valued by PICOS when an optimization solution is found.

        Some expressions can also be valued directly if PICOS can find a minimal
        norm variable assignment that makes the expression have the desired
        value. In particular, this works with affine expressions whose linear
        part has an under- or well-determined coefficient matrix.

        :Example:

        >>> from picos import RealVariable
        >>> x = RealVariable("x", (1,3))
        >>> y = RealVariable("y", (1,3))
        >>> e = x - 2*y + 3
        >>> print("e:", e)
        e: x - 2·y + [3]
        >>> e.value = [4, 5, 6]
        >>> print("e: ", e, "\nx: ", x, "\ny: ", y, sep = "")
        e: [ 4.00e+00  5.00e+00  6.00e+00]
        x: [ 2.00e-01  4.00e-01  6.00e-01]
        y: [-4.00e-01 -8.00e-01 -1.20e+00]

        Unlike :attr:`value_as_matrix`, scalars are returned as scalar types.
        """)

    value_as_matrix = property(
        lambda self: self._wrap_get_value(asMatrix=True),
        lambda self, x: self._set_value(x),
        lambda self: self._set_value(None),
        """Value of the expression, as a CVXOPT matrix type.

        Refer to :attr:`value` for when it is defined (not :obj:`None`).

        Unlike :attr:`value`, scalars are returned in the form of 1x1 matrices.
        """)

    @property
    def valued(self):
        """Whether the expression is valued.

        .. note::

            Querying this attribute is *not* faster than immediately querying
            :attr:`value` and checking whether it is :obj:`None`. Use it only if
            you do not need to know the value, but only whether it is available.

        :Example:

        >>> from picos import RealVariable
        >>> x = RealVariable("x", 3)
        >>> x.valued
        False
        >>> x.value
        >>> print((x|1))
        ∑(x)
        >>> x.value = [1, 2, 3]
        >>> (x|1).valued
        True
        >>> print((x|1))
        6.0
        """
        try:
            self._get_value()
        except NotValued:
            return False
        else:
            return True

    @valued.setter
    def valued(self, x):
        if x is False:
            self._set_value(None)
        else:
            raise ValueError("You may only assign 'False' to the 'valued' "
                "attribute, which is the same as setting 'value' to 'None'.")

    shape = property(
        lambda self: self._get_shape(),
        doc=_get_shape.__doc__)

    size = property(
        lambda self: self._get_shape(),
        doc="""The same as :attr:`shape`.""")

    variables = property(
        lambda self: self._get_variables(),
        doc=_get_variables.__doc__)

    convex = property(
        lambda self: self._is_convex(),
        doc=_is_convex.__doc__)

    concave = property(
        lambda self: self._is_concave(),
        doc=_is_concave.__doc__)

    # --------------------------------------------------------------------------
    # Python special method implementations and their helpers.
    # --------------------------------------------------------------------------

    def __len__(self):
        return self.shape[0] * self.shape[1]

    def __le__(self, other):
        # Try to refine self and see if the operation is then supported.
        # This allows e.g. a <= 0 if a is a real-valued complex expression.
        refined = self.refined
        if type(refined) != type(self):
            return refined.__le__(other)

        # HACK: Mimic Python 3's exception when neither a.__le__(b) nor
        #       b.__ge__(a) are implemented.
        if sys.version_info[0] == 2:
            setattr(self, "LT_HACK_TOKEN", None)
            try:
                if hasattr(other, "__ge__") \
                and not hasattr(other, "GT_HACK_TOKEN"):
                    retval = other.__ge__(self)
                    if retval is not NotImplemented:
                        return retval

                raise TypeError(
                    "Constraints of the form '{} <= {}' are not supported."
                    .format(type(self).__name__, type(other).__name__))
            finally:
                delattr(self, "LT_HACK_TOKEN")
        else:
            return NotImplemented

    def __ge__(self, other):
        # Try to refine self and see if the operation is then supported.
        # This allows e.g. a >= 0 if a is a real-valued complex expression.
        refined = self.refined
        if type(refined) != type(self):
            return refined.__ge__(other)

        # HACK: Mimic Python 3's exception when neither a.__le__(b) nor
        #       b.__ge__(a) are implemented.
        if sys.version_info[0] == 2:
            setattr(self, "GT_HACK_TOKEN", None)
            try:
                if hasattr(other, "__le__") \
                and not hasattr(other, "LT_HACK_TOKEN"):
                    retval = other.__le__(self)
                    if retval is not NotImplemented:
                        return retval

                raise TypeError(
                    "Constraints of the form '{} >= {}' are not supported."
                    .format(type(self).__name__, type(other).__name__))
            finally:
                delattr(self, "GT_HACK_TOKEN")
        else:
            return NotImplemented

    def __invert__(self):
        """Convert between a valued expression and its value.

        The value is returned as a constant affine expression whose conversion
        returns the original expression.
        """
        if hasattr(self, "_origin"):
            return self._origin
        elif self.constant:
            return self

        from .exp_affine import Constant

        A = Constant(glyphs.value(self.string), self._get_value(), self.shape)
        A._origin = self
        return A

    def __contains__(self, variable):
        """Whether the expression concerns the given variable."""
        return variable in self.variables

    def __eq__(self, exp):
        raise NotImplementedError("PICOS supports equality comparison only "
            "between affine expressions, as otherwise the problem would "
            "become non-convex. Choose either <= or >= if possible.")

    def __repr__(self):
        return str(glyphs.repr2(self._typeStr, self._symbStr))

    def __str__(self):
        """Return a dynamic string description of the expression.

        The description is based on whether the expression is valued. If it is
        valued, then a string representation of the value is returned.
        Otherwise, the symbolic description of the expression is returned.
        """
        if self.valued:
            return str(self.value).strip()
        else:
            return str(self._symbStr)

    def __format__(self, format_spec):
        if self.valued:
            return self.value.__format__(format_spec)
        else:
            return self._symbStr.__format__(format_spec)

    def __index__(self):
        if len(self) != 1:
            raise TypeError("Cannot use multidimensional expression {} as an "
                "index.".format(self.string))

        if not self.valued:
            raise NotValued("Cannot use unvalued expression {} as an index."
                .format(self.string))

        value = self.value

        try:
            fltValue = float(value)
            intValue = int(fltValue)

            if intValue != fltValue:
                raise ValueError
        except (TypeError, ValueError):
            raise RuntimeError("Cannot use {} as an index as its value of {} is"
                " not integral.".format(self.string, value))

        return intValue

    def _casting_helper(self, theType):
        assert theType in (int, float, complex)

        if len(self) != 1:
            raise TypeError(
                "Cannot cast multidimensional expression {} as {}."
                .format(self.string, theType.__name__))

        if not self.valued:
            raise NotValued("Cannot cast unvalued expression {} as {}."
                .format(self.string, theType.__name__))

        value = self.value_as_matrix

        return theType(value[0])

    def __int__(self):
        return self._casting_helper(int)

    def __long__(self):
        # Python 2 only.
        return self._casting_helper(int).__long__()

    def __float__(self):
        return self._casting_helper(float)

    def __complex__(self):
        return self._casting_helper(complex)

    def __round__(self, ndigits=None):
        return round(float(self), ndigits)

    # Since we define __eq__, __hash__ is not inherited. Do this manually.
    __hash__ = object.__hash__

    # HACK: This prevents NumPy operators from iterating over PICOS expressions.
    __array_priority__ = float("inf")

    # --------------------------------------------------------------------------
    # Fallback algebraic operations: Try again with converted RHS, refined LHS.
    # --------------------------------------------------------------------------

    @convert_operands(sameShape=True)
    def __add__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__add__(other)
        else:
            return NotImplemented

    @convert_operands(sameShape=True)
    def __radd__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__radd__(other)
        else:
            return NotImplemented

    @convert_operands(sameShape=True)
    def __sub__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__sub__(other)
        else:
            return NotImplemented

    @convert_operands(sameShape=True)
    def __rsub__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__rsub__(other)
        else:
            return NotImplemented

    @convert_operands(sameShape=True)
    def __or__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__or__(other)
        else:
            return NotImplemented

    @convert_operands(sameShape=True)
    def __ror__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__ror__(other)
        else:
            return NotImplemented

    @convert_operands(rMatMul=True)
    def __mul__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__mul__(other)
        else:
            return NotImplemented

    @convert_operands(lMatMul=True)
    def __rmul__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__rmul__(other)
        else:
            return NotImplemented

    @convert_operands(sameShape=True)
    def __xor__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__xor__(other)
        else:
            return NotImplemented

    @convert_operands(sameShape=True)
    def __rxor__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__rxor__(other)
        else:
            return NotImplemented

    @convert_operands()
    def __matmul__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__matmul__(other)
        else:
            return NotImplemented

    @convert_operands()
    def __rmatmul__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__rmatmul__(other)
        else:
            return NotImplemented

    @convert_operands(scalarRHS=True)
    def __truediv__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__truediv__(other)
        else:
            return NotImplemented

    @convert_operands(scalarLHS=True)
    def __rtruediv__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__rtruediv__(other)
        else:
            return NotImplemented

    @convert_operands(scalarRHS=True)
    def __div__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__div__(other)
        else:
            return NotImplemented

    @convert_operands(scalarLHS=True)
    def __rdiv__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__rdiv__(other)
        else:
            return NotImplemented

    @convert_operands(horiCat=True)
    def __and__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__and__(other)
        else:
            return NotImplemented

    @convert_operands(horiCat=True)
    def __rand__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__rand__(other)
        else:
            return NotImplemented

    @convert_operands(vertCat=True)
    def __floordiv__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__floordiv__(other)
        else:
            return NotImplemented

    @convert_operands(vertCat=True)
    def __rfloordiv__(self, other):
        if type(self.refined) != type(self):
            return self.refined.__rfloordiv__(other)
        else:
            return NotImplemented

    def __neg__(self):
        if type(self.refined) != type(self):
            return self.refined.__neg__()
        else:
            return NotImplemented

    def __abs__(self):
        if type(self.refined) != type(self):
            return self.refined.__abs__()
        else:
            return NotImplemented

    # --------------------------------------------------------------------------
    # Backwards compatibility methods.
    # --------------------------------------------------------------------------

    @deprecated("2.0", useInstead="valued")
    def is_valued(self):
        """Whether the expression is valued."""
        return self.valued

    @deprecated("2.0", useInstead="value")
    def set_value(self, value):
        """Set the value of an expression, usually a variable."""
        self.value = value

    @deprecated("2.0", "PICOS treats all inequalities as non-strict. Using the "
        "strict inequality comparison operators may lead to unexpected results "
        "when dealing with integer problems.")
    def __lt__(self, exp):
        return self.__le__(exp)

    @deprecated("2.0", "PICOS treats all inequalities as non-strict. Using the "
        "strict inequality comparison operators may lead to unexpected results "
        "when dealing with integer problems.")
    def __gt__(self, exp):
        return self.__ge__(exp)


def validate_prediction(operator):
    """Validate that the constraint outcome matches the predicted outcome."""
    @functools.wraps(operator)
    def wrapper(lhs, rhs, *args, **kwargs):
        from .set import Set

        def what():
            return "({}).{}({})".format(
                lhs._symbStr, operator.__name__, rhs._symbStr)

        assert isinstance(lhs, (Expression, Set)) \
            and isinstance(rhs, (Expression, Set)), \
            "validate_prediction must occur below convert_operands."

        lhs_type = lhs.type

        assert hasattr(lhs_type, operator.__name__), "Constraint outcome " \
            "prediction is not implemented for the operation {}." \
            .format(operator.__name__)

        try:
            predictedType = getattr(lhs_type, operator.__name__)(rhs.type)
        except NotImplementedError:
            predictedType = None  # No prediction was made.
        except PredictedFailure:
            predictedType = NotImplemented  # Prediction is "not possible".
        except Exception as error:
            raise AssertionError("Cannot validate the prediciton for {}: {}"
                .format(what(), error))

        try:
            outcome = operator(lhs, rhs, *args, **kwargs)
        except Exception as error:
            # Case where the prediction is positive and the outcome is negative.
            if predictedType not in (None, NotImplemented):
                raise AssertionError(
                    "Outcome for {} was predicted {} but the operation raised "
                    "an error: {}".format(what(), predictedType, error))
            else:
                raise

        # Case where the prediction is negative and the outcome is positive.
        if predictedType is NotImplemented and outcome is not NotImplemented:
            raise AssertionError(
                "The operation {} was predicted to fail but it produced "
                "an output of {}.".format(what(), outcome.type))

        # Case where no prediction was made.
        if not predictedType:
            return outcome

        # Case where the outcome is try-to-reverse-the-operation.
        if outcome is NotImplemented:
            return outcome

        # Case where the prediction and the outcome are positive but differ.
        outcomeType = outcome.type
        if not predictedType.equals(outcomeType):
            raise AssertionError("Outcome for {} was predicted {} but is {}."
                .format(what(), predictedType, outcomeType))

        return outcome
    return wrapper


def refine_operands(stop_at_affine=False):
    """Cast :meth:`~Expression.refined` on both operands.

    If the left hand side operand (i.e. ``self``) is refined to an instance of a
    different type, then, instead of the decorated method, the method with the
    same name on the refined type is invoked with the (refined) right hand side
    operand as its argument.

    This decorator is supposed to be used on all constraint creating binary
    operator methods so that degenerated instances (e.g. a complex affine
    expression an imaginary part of zero) can occur but are not used in
    constraints. This speeds up many computations involving expressions as these
    degenerate cases do not need to be detected. See also :attr:`type`, which
    describes the refined version of an expression as well.

    :param bool stop_at_affine: Do not refine any affine expressions, in
        particular do not refine complex affine expressions to real ones.
    """
    def decorator(operator):
        @functools.wraps(operator)
        def wrapper(lhs, rhs, *args, **kwargs):
            from .set import Set
            from .exp_affine import ComplexAffineExpression

            assert isinstance(lhs, (Expression, Set)) \
                and isinstance(rhs, (Expression, Set)), \
                "refine_operands must occur below convert_operands."

            if stop_at_affine and isinstance(lhs, ComplexAffineExpression):
                lhs_refined = lhs
            else:
                lhs_refined = lhs.refined

            if type(lhs_refined) is not type(lhs):
                assert hasattr(lhs_refined, operator.__name__), \
                    "refine_operand transformed 'self' to another type that " \
                    "does not define an operator with the same name as the " \
                    "decorated one."

                refined_operation = getattr(lhs_refined, operator.__name__)

                return refined_operation(rhs, *args, **kwargs)

            if stop_at_affine and isinstance(rhs, ComplexAffineExpression):
                rhs_refined = rhs
            else:
                rhs_refined = rhs.refined

            return operator(lhs_refined, rhs_refined, *args, **kwargs)
        return wrapper
    return decorator


# --------------------------------------
__all__ = api_end(_API_START, globals())
