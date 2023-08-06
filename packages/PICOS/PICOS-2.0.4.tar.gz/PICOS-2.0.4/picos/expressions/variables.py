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

"""Implements all mathematical variable types."""

import random
import threading
from collections import namedtuple
from copy import copy

import cvxopt

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_property
from ..containers import DetailedType
from .data import cvxopt_equals, cvxopt_maxdiff, load_data, load_shape
from .exp_affine import AffineExpression, ComplexAffineExpression
from .expression import Expression, NotValued
from .vectorizations import (ComplexVectorization, FullVectorization,
                             HermitianVectorization,
                             LowerTriangularVectorization,
                             SkewSymmetricVectorization,
                             SymmetricVectorization,
                             UpperTriangularVectorization)

_API_START = api_start(globals())
# -------------------------------


# The variable IDs start at a random value to prevent a clash if variables are
# pickled and loaded in another python session. The choice of 31 bits is to
# produce up to 2**31-1 short hexadecimal IDs for use in private variable names.
_NEXT_VARIABLE_ID = int(random.getrandbits(31))

# A lock for _NEXT_VARIABLE_ID, if the user uses threads to create variables.
_VARIABLE_ID_LOCK = threading.Lock()


def _make_variable_id(dim):
    """Create a unique (starting) ID for a new variable."""
    with _VARIABLE_ID_LOCK:
        global _NEXT_VARIABLE_ID
        id = _NEXT_VARIABLE_ID
        _NEXT_VARIABLE_ID += dim
        return id


# A map used when converting IDs to strings.
_ID_HEX2STR_MAP = {ord(a): ord(b) for a, b in zip(
    "0123456789abcdef", "ABCDEFGHIJKLMNOP")}
_ID_HEX2STR_MAP_PY2 = "".join([chr(_ID_HEX2STR_MAP[i]) if i in _ID_HEX2STR_MAP
    else "_" for i in range(256)])


def _id_to_str(id):
    """Convert a variable id to a short string identifier."""
    try:
        return "{:08x}".format(id).translate(_ID_HEX2STR_MAP)
    except TypeError:  # Python 2
        return "{:08x}".format(id).translate(_ID_HEX2STR_MAP_PY2)


#: Absolute integrality tolerance for integral and binary variables.
INTEGRALITY_ABS_TOL = 1e-4


class VariableType(DetailedType):
    """The detailed type of a variable for predicting reformulation outcomes."""

    pass


class BaseVariable:
    """Primary base class for all variable types.

    Variables need to inherit this class with priority (first class listed) and
    :class:`~.exp_affine.ComplexAffineExpression` or
    :class:`~.exp_affine.AffineExpression` without priority.
    """

    # TODO: Document changed variable bound behavior: Only full bounds can be
    #       given but they may contain (-)float("inf").
    def __init__(self, name, vectorization, lower=None, upper=None):
        """Perform basic initialization for :class:`BaseVariable` instances.

        :param str name:
            Name of the variable. A leading `"__"` denotes a private variable
            and is replaced by a sequence containing the variable's unique ID.

        :param vectorization:
            Vectorization format used to store the value.
        :type vectorization:
            ~picos.expressions.vectorizations.BaseVectorization

        :param lower:
            Constant lower bound on the variable. May contain ``float("-inf")``
            to denote unbounded elements.

        :param upper:
            Constant upper bound on the variable. May contain ``float("inf")``
            to denote unbounded elements.
        """
        if not isinstance(self, Expression):
            raise TypeError("{} may not be initialized directly.".format(
                type(self).__name__))

        self._id    = _make_variable_id(vectorization.dim)
        self._vec   = vectorization
        self._lower = None if lower is None else self._load_vectorized(lower)
        self._upper = None if upper is None else self._load_vectorized(upper)
        self._value = None

        if not name or name.startswith("__"):
            id_str = "__{}_".format(_id_to_str(self._id))
            name = name.replace("__", id_str, 1) if name else id_str + "_"

        self._name = name

    @property
    def id(self):
        """The unique (starting) ID of the variable, assigned at creation."""
        return self._id

    VarSubtype = namedtuple("VarSubtype", ("dim", "bnd"))

    @classmethod
    def make_var_type(cls, *args, **kwargs):
        """Create a detailed variable type from subtype parameters.

        See also :attr:`var_type`.
        """
        return VariableType(cls, cls.VarSubtype(*args, **kwargs))

    @property
    def var_subtype(self):
        """The subtype part of the detailed variable type.

        See also :attr:`var_type`.
        """
        return self.VarSubtype(self.dim, self.num_bounds)

    @property
    def var_type(self):
        """The detailed variable type.

        This intentionally does not override
        :meth:`Expression.type <.expression.Expression.type>` so that the
        variable still behaves as the affine expression that it represents when
        prediction constraint outcomes.
        """
        return VariableType(self.__class__, self.var_subtype)

    def id_at(self, index):
        """Return the unique ID of a scalar entry, assigned at creation."""
        if index < 0 or index >= self._vec.dim:
            raise IndexError("Bad index {} for the {} dimensional variable {}."
                .format(index, self._vec.dim, self.name))

        return self._id + index

    @property
    def dim(self):
        """The variable's dimension on the real field.

        This corresponds to the length of its vectorized value.
        """
        return self._vec.dim

    @property
    def name(self):
        """The name of the variable."""
        return self._name

    @cached_property
    def long_string(self):
        """Long string representation for printing a :meth:`~picos.Problem`."""
        lower, upper = self.bound_dicts
        if lower and upper:
            bound_str = "clamped"
        elif lower:
            bound_str = "bounded below"
        elif upper:
            bound_str = "bounded above"
        else:
            bound_str = None

        return "{} {} {}{}".format(
            glyphs.shape(self.shape),
            self._get_type_string_base().lower(),
            self.name,
            " ({})".format(bound_str) if bound_str else "")

        return "{} {} variable {}{}".format(
            self._get_type_string_base().rsplit(" Variable")[0].lower(),
            glyphs.shape(self.shape),
            self.name,
            " ({})".format(bound_str) if bound_str else "")

    @cached_property
    def bound_dicts(self):
        """Variable bounds as a pair of mappings from index to scalar bound.

        The indices and bound values are with respect to the internal
        representation of the variable, whose value can be accessed with
        :attr:`internal_value`.

        Upper and lower bounds set to ``float("inf")`` and ``float("-inf")``
        on variable creation, respectively, are not included.
        """
        posinf = float("+inf")
        neginf = float("-inf")

        if self._lower is None:
            lower = {}
        else:
            lower = {i: self._lower[i] for i in range(self.dim)
                     if self._lower[i] != neginf}

        if self._upper is None:
            upper = {}
        else:
            upper = {i: self._upper[i] for i in range(self.dim)
                     if self._upper[i] != posinf}

        return (lower, upper)

    @property
    def num_bounds(self):
        """Number of scalar bounds associated with the variable."""
        lower, upper = self.bound_dicts
        return len(lower) + len(upper)

    @cached_property
    def bound_constraint(self):
        """The variable bounds as a PICOS constraint, or :obj:`None`."""
        lower, upper = self.bound_dicts

        I, J, V, b = [], [], [], []

        for i, bound in upper.items():
            I.append(i)
            J.append(i)
            V.append(1.0)
            b.append(bound)

        offset = len(I)

        for i, bound in lower.items():
            I.append(offset + i)
            J.append(i)
            V.append(-1.0)
            b.append(-bound)

        if not I:
            return None

        A = cvxopt.spmatrix(V, I, J, size=(len(I), self.dim), tc="d")

        Ax = AffineExpression(string=glyphs.Fn("bnd_con_lhs")(self.name),
            shape=len(I), coefficients={self: A})

        return Ax <= b

    def copy(self, new_name=None):
        """Return an independent copy of the variable."""
        name = self.name if new_name is None else new_name

        if self._lower is not None or self._upper is not None:
            return self.__class__(name, self.shape, self._lower, self._upper)
        else:
            return self.__class__(name, self.shape)

    def _load_vectorized(self, value):
        """Support :meth:`__init__` and ``_set_value``."""
        return self._vec.vectorize(
            load_data(value, self._vec.shape, self._typecode)[0])

    def _check_internal_value(self, value):
        """Support :meth:`_set_value` and :meth:`_set_internal_value`."""
        pass

    # NOTE: This needs to be inherited with priority.
    def _get_value(self):
        return self._vec.devectorize(self._get_internal_value())

    # NOTE: This needs to be inherited with priority.
    def _set_value(self, value):
        if value is None:
            self._value = None
            return

        try:
            value = self._load_vectorized(value)
            self._check_internal_value(value)
        except Exception as error:
            raise type(error)("Failed to assign a value to variable {}: {}"
                .format(self.string, error))
        else:
            self._value = value

    def _get_internal_value(self):
        if self._value is None:
            raise NotValued("Variable {} is not valued.".format(self.string))
        else:
            return copy(self._value)

    def _set_internal_value(self, value):
        if value is None:
            self._value = None
            return

        try:
            value = load_data(value, (self._vec.dim, 1), "d")[0]
            self._check_internal_value(value)
        except Exception as error:
            raise type(error)(
                "Failed to assign an internal value to variable {}: {}"
                .format(self.string, error))
        else:
            self._value = value

    internal_value = property(
        lambda self: self._get_internal_value(),
        lambda self, value: self._set_internal_value(value),
        lambda self: self._set_internal_value(None),
        """The internal (special vectorized) value of the variable.""")

    def _get_clstype(self):
        # Mimic an ordinary (complex) affine expression.
        return self._basetype

    def _get_subtype(self):
        # Mimic an ordinary (complex) affine expression.
        return self._basetype._get_subtype(self)

    @classmethod
    def _predict(cls, subtype, relation, other):
        # Mimic an ordinary (complex) affine expression.
        return cls._get_basetype()._predict(subtype, relation, other)


class RealVariable(BaseVariable, AffineExpression):
    """A real-valued variable."""

    def __init__(self, name, shape=(1, 1), lower=None, upper=None):
        """Create a :class:`RealVariable`.

        :param str name: The variable's name, used for both string description
            and identification.
        :param shape: The shape of a vector or matrix variable.
        :type shape: int or tuple or list
        :param lower: Constant lower bound on the variable. May contain
            ``float("-inf")`` to denote unbounded elements.
        :param upper: Constant upper bound on the variable. May contain
            ``float("inf")`` to denote unbounded elements.
        """
        shape = load_shape(shape)
        vec = FullVectorization(shape)
        BaseVariable.__init__(self, name, vec, lower, upper)
        AffineExpression.__init__(self, self.name, shape, {self: vec.identity})

    @classmethod
    def _get_type_string_base(cls):
        return "Real Variable"


class IntegerVariable(BaseVariable, AffineExpression):
    """An integer-valued variable."""

    def __init__(self, name, shape=(1, 1), lower=None, upper=None):
        """Create an :class:`IntegerVariable`.

        :param str name: The variable's name, used for both string description
            and identification.
        :param shape: The shape of a vector or matrix variable.
        :type shape: int or tuple or list
        :param lower: Constant lower bound on the variable. May contain
            ``float("-inf")`` to denote unbounded elements.
        :param upper: Constant upper bound on the variable. May contain
            ``float("inf")`` to denote unbounded elements.
        """
        shape = load_shape(shape)
        vec = FullVectorization(shape)
        BaseVariable.__init__(self, name, vec, lower, upper)
        AffineExpression.__init__(self, self.name, shape, {self: vec.identity})

    @classmethod
    def _get_type_string_base(cls):
        return "Integer Variable"

    def _check_internal_value(self, value):
        fltData = list(value)

        if not fltData:
            return  # All elements are exactly zero.

        intData = cvxopt.matrix([round(x) for x in fltData])
        fltData = cvxopt.matrix(fltData)

        if not cvxopt_equals(intData, fltData, INTEGRALITY_ABS_TOL):
            raise ValueError("Data is not near-integral with absolute tolerance"
                " {:.1e}: Largest difference is {:.1e}.".format(
                INTEGRALITY_ABS_TOL, cvxopt_maxdiff(intData, fltData)))


class BinaryVariable(BaseVariable, AffineExpression):
    r"""A :math:`\{0,1\}`-valued variable."""

    def __init__(self, name, shape=(1, 1)):
        """Create a :class:`BinaryVariable`.

        :param str name: The variable's name, used for both string description
            and identification.
        :param shape: The shape of a vector or matrix variable.
        :type shape: int or tuple or list
        """
        shape = load_shape(shape)
        vec = FullVectorization(shape)
        BaseVariable.__init__(self, name, vec)
        AffineExpression.__init__(self, self.name, shape, {self: vec.identity})

    @classmethod
    def _get_type_string_base(cls):
        return "Binary Variable"

    def _check_internal_value(self, value):
        fltData = list(value)

        if not fltData:
            return  # All elements are exactly zero.

        binData = cvxopt.matrix([float(bool(round(x))) for x in fltData])
        fltData = cvxopt.matrix(fltData)

        if not cvxopt_equals(binData, fltData, INTEGRALITY_ABS_TOL):
            raise ValueError("Data is not near-binary with absolute tolerance"
                " {:.1e}: Largest difference is {:.1e}.".format(
                INTEGRALITY_ABS_TOL, cvxopt_maxdiff(binData, fltData)))


class ComplexVariable(BaseVariable, ComplexAffineExpression):
    """A complex-valued variable.

    Passed to solvers as a real variable vector with :math:`2mn` entries.
    """

    def __init__(self, name, shape=(1, 1)):
        """Create a :class:`ComplexVariable`.

        :param str name: The variable's name, used for both string description
            and identification.
        :param shape: The shape of a vector or matrix variable.
        :type shape: int or tuple or list
        """
        shape = load_shape(shape)
        vec = ComplexVectorization(shape)
        BaseVariable.__init__(self, name, vec)
        ComplexAffineExpression.__init__(
            self, self.name, shape, {self: vec.identity})

    @classmethod
    def _get_type_string_base(cls):
        return "Complex Variable"


class SymmetricVariable(BaseVariable, AffineExpression):
    r"""A symmetric matrix variable.

    Stored internally and passed to solvers as a symmetric vectorization with
    only :math:`\frac{n(n+1)}{2}` entries.
    """

    def __init__(self, name, shape=(1, 1), lower=None, upper=None):
        """Create a :class:`SymmetricVariable`.

        :param str name: The variable's name, used for both string description
            and identification.
        :param shape: The shape of the matrix.
        :type shape: int or tuple or list
        :param lower: Constant lower bound on the variable. May contain
            ``float("-inf")`` to denote unbounded elements.
        :param upper: Constant upper bound on the variable. May contain
            ``float("inf")`` to denote unbounded elements.
        """
        shape = load_shape(shape, squareMatrix=True)
        vec = SymmetricVectorization(shape)
        BaseVariable.__init__(self, name, vec, lower, upper)
        AffineExpression.__init__(self, self.name, shape, {self: vec.identity})

    @classmethod
    def _get_type_string_base(cls):
        return "Symmetric Variable"


class SkewSymmetricVariable(BaseVariable, AffineExpression):
    r"""A skew-symmetric matrix variable.

    Stored internally and passed to solvers as a skew-symmetric vectorization
    with only :math:`\frac{n(n-1)}{2}` entries.
    """

    def __init__(self, name, shape=(1, 1), lower=None, upper=None):
        """Create a :class:`SkewSymmetricVariable`.

        :param str name: The variable's name, used for both string description
            and identification.
        :param shape: The shape of the matrix.
        :type shape: int or tuple or list
        :param lower: Constant lower bound on the variable. May contain
            ``float("-inf")`` to denote unbounded elements.
        :param upper: Constant upper bound on the variable. May contain
            ``float("inf")`` to denote unbounded elements.
        """
        shape = load_shape(shape, squareMatrix=True)
        vec = SkewSymmetricVectorization(shape)
        BaseVariable.__init__(self, name, vec, lower, upper)
        AffineExpression.__init__(self, self.name, shape, {self: vec.identity})

    @classmethod
    def _get_type_string_base(cls):
        return "Skew-symmetric Variable"


class HermitianVariable(BaseVariable, ComplexAffineExpression):
    r"""A hermitian matrix variable.

    Stored internally and passed to solvers as the horizontal concatenation of
    a real symmetric vectorization with :math:`\frac{n(n+1)}{2}` entries and a
    real skew-symmetric vectorization with :math:`\frac{n(n-1)}{2}` entries,
    resulting in a real vector with only :math:`n^2` entries total.
    """

    def __init__(self, name, shape):
        """Create a :class:`HermitianVariable`.

        :param str name: The variable's name, used for both string description
            and identification.
        :param shape: The shape of the matrix.
        :type shape: int or tuple or list
        """
        shape = load_shape(shape, squareMatrix=True)
        vec = HermitianVectorization(shape)
        BaseVariable.__init__(self, name, vec)
        ComplexAffineExpression.__init__(
            self, self.name, shape, {self: vec.identity})

    @classmethod
    def _get_type_string_base(cls):
        return "Hermitian Variable"


class LowerTriangularVariable(BaseVariable, AffineExpression):
    r"""A lower triangular matrix variable.

    Stored internally and passed to solvers as a lower triangular vectorization
    with only :math:`\frac{n(n+1)}{2}` entries.
    """

    def __init__(self, name, shape=(1, 1), lower=None, upper=None):
        """Create a :class:`LowerTriangularVariable`.

        :param str name: The variable's name, used for both string description
            and identification.
        :param shape: The shape of the matrix.
        :type shape: int or tuple or list
        :param lower: Constant lower bound on the variable. May contain
            ``float("-inf")`` to denote unbounded elements.
        :param upper: Constant upper bound on the variable. May contain
            ``float("inf")`` to denote unbounded elements.
        """
        shape = load_shape(shape, squareMatrix=True)
        vec = LowerTriangularVectorization(shape)
        BaseVariable.__init__(self, name, vec)
        AffineExpression.__init__(self, self.name, shape, {self: vec.identity})

    @classmethod
    def _get_type_string_base(cls):
        return "Lower Triangular Variable"


class UpperTriangularVariable(BaseVariable, AffineExpression):
    r"""An upper triangular matrix variable.

    Stored internally and passed to solvers as an upper triangular vectorization
    with only :math:`\frac{n(n+1)}{2}` entries.
    """

    def __init__(self, name, shape=(1, 1), lower=None, upper=None):
        """Create a :class:`UpperTriangularVariable`.

        :param str name: The variable's name, used for both string description
            and identification.
        :param shape: The shape of the matrix.
        :type shape: int or tuple or list
        :param lower: Constant lower bound on the variable. May contain
            ``float("-inf")`` to denote unbounded elements.
        :param upper: Constant upper bound on the variable. May contain
            ``float("inf")`` to denote unbounded elements.
        """
        shape = load_shape(shape, squareMatrix=True)
        vec = UpperTriangularVectorization(shape)
        BaseVariable.__init__(self, name, vec)
        AffineExpression.__init__(self, self.name, shape, {self: vec.identity})

    @classmethod
    def _get_type_string_base(cls):
        return "Lower Triangular Variable"


CONTINUOUS_VARTYPES = (RealVariable, ComplexVariable, SymmetricVariable,
                       SkewSymmetricVariable, HermitianVariable,
                       LowerTriangularVariable, UpperTriangularVariable)


# --------------------------------------
__all__ = api_end(_API_START, globals())
