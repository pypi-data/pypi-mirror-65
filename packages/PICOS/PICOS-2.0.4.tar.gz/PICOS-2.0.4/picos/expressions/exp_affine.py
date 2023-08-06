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

"""Implements affine expression types."""

import math
import operator
from collections import namedtuple
from functools import reduce

import cvxopt
import numpy

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import (cached_property, cached_selfinverse_property,
                       cached_selfinverse_unary_operator,
                       cached_unary_operator)
from ..constraints import (AffineConstraint, ComplexAffineConstraint,
                           ComplexLMIConstraint, Constraint, LMIConstraint)
from ..formatting import detect_range
from ..legacy import deprecated
from .data import (blend_shapes, convert_operands, cvx2np, cvxopt_vcat,
                   left_kronecker_I, load_data, load_dense_data, load_shape,
                   right_kronecker_I, sparse_quadruple)
from .expression import (Expression, ExpressionType, refine_operands,
                         validate_prediction)

_API_START = api_start(globals())
# -------------------------------


RELATIVE_HERMITIANNESS_TOLERANCE = 1e-10
r"""Relative tolerance when checking if an expression is hermitian.

A square (complex) affine expression :math:`A` is considered hermitian if

.. math::

    \max_{1 \leq i, j \leq n} |(A - A^H)_{ij}|
    \leq
    \varepsilon \max_{1 \leq i, j \leq n} |A_{ij}|

where :math:`\varepsilon` is this tolerance.

Used by :meth:`ComplexAffineExpression.hermitian`.
"""


class ComplexAffineExpression(Expression):
    """A multidimensional complex affine expression.

    Base class for the real :class:`AffineExpression`.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    def __init__(self, string, shape=(1, 1), coefficients={}, constant=0j):
        """Initialize a (complex) affine expression.

        This constructor is meant for internal use. As a user, you will most
        likely want to build expressions starting from
        :mod:`~picos.expressions.variables` or a :func:`~picos.Constant`.

        :param str string: A symbolic string description.
        :param shape: Shape of a vector or matrix expression.
        :type shape: int or tuple or list
        :param dict coefficients: The linear part of the affine expression; maps
            the vectorization of :class:`variables <.variables.BaseVariable>` to
            their coefficients.
        :param constant: The constant part of the affine expression.

        .. warning::
            If the given coefficients and constant are already of the desired
            (numeric) type and shape, they are stored by reference. Modifying
            such data can lead to unexpected results as PICOS expressions are
            supposed to be immutable (to allow
            `caching <https://en.wikipedia.org/wiki/Cache_(computing)>`_ of
            results).

            If you create affine expressions by any other means than this
            constructor, PICOS makes a copy of your data to prevent future
            modifications to it from causing inconsistencies.
        """
        from .variables import BaseVariable

        shape  = load_shape(shape)
        length = shape[0]*shape[1]

        if not isinstance(coefficients, dict):
            raise TypeError("Coefficients of {} must be given as a dict."
                .format(type(self).__name__))

        # Store shape.
        self._shape = shape

        # Store coefficients.
        self._coefs = {}
        for var, coef in coefficients.items():
            # Do not store coefficients of zero.
            if not coef:
                continue

            if not isinstance(var, BaseVariable):
                raise TypeError("Coefficients of {} must be indexed by "
                    "variables, not objects of type {}.".format(
                    type(self).__name__, type(var).__name__))

            self._coefs[var] = load_data(
                coef, (length, var.dim), self._typecode, alwaysCopy=False)[0]

        # Store vectorized constant.
        self._const = load_data(
            constant, length, self._typecode, alwaysCopy=False)[0]

        # Determine the type string.
        typeBaseStr = self._get_type_string_base()
        if "{}" in typeBaseStr:
            if self._coefs:
                if self._const:
                    typeBaseStr = typeBaseStr.format("Affine Expression")
                else:
                    typeBaseStr = typeBaseStr.format("Linear Expression")
            else:
                typeBaseStr = typeBaseStr.format("Constant")
        typeStr = "{} {}".format(glyphs.shape(shape), typeBaseStr)

        Expression.__init__(self, typeStr, string)

    @classmethod
    def _get_basetype(cls):
        """Return the first order :class:`Expression` subclass this is based on.

        Enables subclass objects (such as variables) to behave like the returned
        type with respect to algebraic operations. For instance, the sum of
        two :class:`ComplexVariable` is a :class:`ComplexAffineExpression`.
        """
        return ComplexAffineExpression

    @classmethod
    def _get_typecode(cls):
        """See :meth:`_get_basetype`."""
        return "z"

    @classmethod
    def _get_type_string_base(cls):
        """See :meth:`_get_basetype`."""
        return "Complex {}"

    _basetype    = property(lambda self: self._get_basetype())
    _typecode    = property(lambda self: self._get_typecode())
    _typeStrBase = property(lambda self: self._get_type_string_base())

    @classmethod
    def from_constant(cls, constant, shape=None, name=None):
        """Create a class instance from the given numeric constant.

        Loads the given constant as a PICOS expression, optionally broadcasted
        or reshaped to the given shape and named as specified.

        See :func:`~.data.load_data` for supported data formats and broadcasting
        and reshaping rules.

        Unlike :func:`Constant`, this class method always creates an instance of
        the class that it is called on, instead of tailoring towards the numeric
        type of the data.

        .. note::
            When an operation involves both a PICOS expression and a constant
            value of another type, PICOS converts the constant on the fly so
            that you rarely need to use this method.
        """
        constant, string = load_data(constant, shape, cls._get_typecode())
        return cls(name if name else string, constant.size, {}, constant)

    @classmethod
    def zero(cls, shape=(1, 1)):
        """Return a constant zero expression of given shape."""
        shape  = load_shape(shape)
        string = glyphs.scalar(0) if shape == (1, 1) else glyphs.matrix(0)
        return cls(string, shape)

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    @cached_unary_operator
    def _get_refined(self):
        if self.isreal:
            return AffineExpression(
                self._symbStr, self._shape, self._coefs, self._const)
        else:
            return self

    Subtype = namedtuple("Subtype", ("shape", "constant", "nonneg"))
    Subtype.dim = property(lambda self: self.shape[0] * self.shape[1])

    def _get_subtype(self):
        nonneg = self.constant and self.isreal \
            and all(x >= 0 for x in self.value_as_matrix)

        return self.Subtype(self._shape, self.constant, nonneg)

    def _get_value(self):
        # Create a vectorized copy of the constant term.
        value = self._const[:]

        for var, coef in self._coefs.items():
            summand = coef * var._get_internal_value()

            if type(value) == type(summand):
                value += summand
            else:
                # Exactly one of the matrices is sparse.
                value = value + summand

        # Resize the value to the proper shape.
        value.size = self.shape

        return value

    def _devectorize(self, value):
        value.size = self._shape
        return value

    @convert_operands(sameShape=True, allowNone=True)
    def _set_value(self, value):
        if value is None:
            for var in self._coefs:
                var.value = None
            return

        # Since all variables are real-valued, prevent NumPy from finding
        # complex-valued solutions that do not actually work.
        (self.real // self.imag).renamed(self.string).value \
            = (value.real // value.imag)

    def _get_shape(self):
        return self._shape

    @cached_unary_operator
    def _get_variables(self):
        return frozenset(var for var in self._coefs)

    def _is_convex(self):
        return True

    def _is_concave(self):
        return True

    def _replace_variables(self, var_map):
        # Handle the base case where the affine expression is a variable.
        if self in var_map:
            return var_map[self]

        name_map = {old.name: new.name for old, new in var_map.items()}

        string = self.string
        if isinstance(string, glyphs.GlStr):
            string = string.reglyphed(name_map)
        elif string in name_map:
            # Handle corner cases like x + 0 for a variable x.
            string = name_map[string]

        coefs = {var_map[var]: coef for var, coef in self._coefs.items()}

        return self._basetype(string, self._shape, coefs, self._const)

    # --------------------------------------------------------------------------
    # Python special method implementations, except constraint-creating ones.
    # --------------------------------------------------------------------------

    def __len__(self):
        # Faster version that overrides Expression.__len__.
        return self._shape[0] * self._shape[1]

    def __getitem__(self, index):
        def slice2range(s, length):
            """Transform a :class:`slice` to a :class:`range`."""
            assert isinstance(s, slice)

            # Plug in slice's default values.
            ss = s.step if s.step else 1
            if ss > 0:
                sa = s.start if s.start is not None else 0
                sb = s.stop  if s.stop  is not None else length
            else:
                assert ss < 0
                sa = s.start if s.start is not None else length - 1
                sb = s.stop  # Keep it None as -1 would mean length - 1.

            # Wrap negative indices (once).
            ra = length + sa if sa < 0 else sa
            if sb is None:
                # This is the only case where we give a negative index to range.
                rb = -1
            else:
                rb = length + sb if sb < 0 else sb

            # Clamp out-of-bound indices.
            ra = min(max(0,  ra), length - 1)
            rb = min(max(-1, rb), length)

            r = range(ra, rb, ss)

            if not r:
                raise IndexError("Empty slice.")

            return r

        def range2slice(r, length):
            """Transform a :class:`range` to a :class:`slice`, if possible.

            :raises ValueError: If the input cannot be expressed as a slice.
            """
            assert isinstance(r, range)

            if not r:
                raise IndexError("Empty range.")

            ra = r.start
            rb = r.stop
            rs = r.step

            if rs > 0:
                if ra < 0 or rb > length:
                    raise ValueError(
                        "Out-of-bounds range cannot be represented as a slice.")
            else:
                assert rs < 0
                if ra >= length or rb < -1:
                    raise ValueError(
                        "Out-of-bounds range cannot be represented as a slice.")

                if rb == -1:
                    rb = None

            return slice(ra, rb, rs)

        def list2slice(l, length):
            """Transform a :class:`list` to a :class:`slice`, if possible.

            :raises TypeError: If the input is not an integer sequence.
            :raises ValueError: If the input cannot be expressed as a slice.
            """
            r = detect_range(l)

            if isinstance(r, list):  # Python 2
                raise RuntimeError(
                    "Unable to convert from list to slice because the "
                    "intermediate range object does not exist under Python 2.")

            return range2slice(r, length)

        def slice2str(s):
            """Return the short string that produced a :class:`slice`."""
            assert isinstance(s, slice)

            startStr = str(s.start) if s.start is not None else ""
            stopStr  = str(s.stop)  if s.stop  is not None else ""
            if s.step in (None, 1):
                if s.start is not None and s.stop is not None \
                and s.stop == s.start + 1:
                    return startStr
                else:
                    return "{}:{}".format(startStr, stopStr)
            else:
                return "{}:{}:{}".format(startStr, stopStr, str(s.step))

        def list2str(l, length):
            """Return a short string represnetation of a :class:`list`."""
            assert isinstance(l, list)

            # Extract integers wrapped in a list.
            if len(l) == 1:
                return str(l[0])

            # Try to convert the list to a slice.
            try:
                l = list2slice(l, length)
            except (ValueError, RuntimeError):
                pass

            if isinstance(l, list):
                if len(l) > 4:
                    return glyphs.shortint(l[0], l[-1])
                else:
                    return str(l).replace(" ", "")
            else:
                return slice2str(l)

        def any2str(a, length):
            if isinstance(a, slice):
                return slice2str(a)
            elif isinstance(a, list):
                return list2str(a, length)
            else:
                assert False

        m, n = self._shape
        indexStr = None
        isIntList = False

        # Turn the index expression into a mutable list of one index per axis.
        if isinstance(index, tuple):  # Multiple axis slicing.
            index = list(index)
        elif isinstance(index, dict):  # Arbitrary matrix element selection.
            if len(index) != 2:
                "If slicing with a dictionary, there must be exactly two keys."

            keys = index.keys()
            i, j = min(keys), max(keys)
            I, J = index[i], index[j]

            try:
                I = load_dense_data(I, typecode="i", alwaysCopy=False)[0]
                J = load_dense_data(J, typecode="i", alwaysCopy=False)[0]

                if 1 not in I.size or 1 not in J.size:
                    raise TypeError("At least one of the objects is not flat "
                        "but a proper matrix.")

                if len(I) != len(J):
                    raise TypeError("The objects do not have the same length.")

                I, J = list(I), list(J)
            except Exception as error:
                raise TypeError("Loading a sparse index vector pair for {} from"
                    " objects of type {} and {} failed: {}".format(
                    self.string, type(I).__name__, type(J).__name__, error))

            # Represent the selection as a global index list.
            index = [[i + j*m for i, j in zip(I, J)]]

            # Use a special index string.
            indexStr = glyphs.size(list2str(I, n), list2str(J, m))

            # Don't invoke load_dense_data on the list.
            isIntList = True
        else:  # Global indexing.
            index = [index]

        # Make sure either global or row/column indexing is used.
        if not index:
            raise IndexError("Empty index.")
        elif len(index) > 2:
            raise IndexError(
                "PICOS expressions do not have a third axis to slice.")

        # Turn the indices for each axis into either a slice or a list.
        for axis, selection in enumerate(index):
            # Convert anything that is not a slice, including scalars and lists
            # that are not confirmed integer, to an integer row or column
            # vector, then (back) to a list.
            if not isIntList and not isinstance(selection, slice):
                try:
                    matrix = load_dense_data(
                        selection, typecode="i", alwaysCopy=False)[0]

                    if 1 not in matrix.size:
                        raise TypeError("The object is not flat but a {} shaped"
                            " matrix.".format(glyphs.shape(matrix.size)))

                    selection = list(matrix)
                except Exception as error:
                    raise TypeError("Loading a slicing index vector for axis {}"
                        " of {} from an object of type {} failed: {}".format(
                        axis, self.string, type(selection).__name__, error))

            index[axis] = selection

        # Build index string, retrieve new shape, finalize index.
        if len(index) == 1:  # Global indexing.
            index = index[0]

            if isinstance(index, slice):
                shape = len(slice2range(index, len(self)))
            else:
                shape = len(index)

            if indexStr is None:
                indexStr = any2str(index, len(self))
        else:  # Multiple axis slicing.
            if indexStr is None:
                indexStr = "{},{}".format(
                    any2str(index[0], m), any2str(index[1], n))

            # Convert to a global index list.
            RC, shape = [], []
            for axis, selection in enumerate(index):
                k = self._shape[axis]

                if isinstance(selection, slice):
                    # Turn the slice into an iterable range.
                    selection = slice2range(selection, k)

                    # All indices from a slice are nonnegative.
                    assert all(i >= 0 for i in selection)

                if isinstance(selection, list):
                    # Wrap once. This is consistent with CVXOPT.
                    selection = [i if i >= 0 else k + i for i in selection]

                    # Perform a partial out-of-bounds check.
                    if any(i < 0 for i in selection):
                        raise IndexError(
                            "Out-of-bounds access along axis {}.".format(axis))

                # Complete the check for out-of-bounds access.
                if any(i >= k for i in selection):
                    raise IndexError(
                        "Out-of-bounds access along axis {}.".format(axis))

                RC.append(selection)
                shape.append(len(selection))

            rows, cols = RC
            index = [i + j*m for j in cols for i in rows]

        # Finalize the string.
        string = glyphs.slice(self.string, indexStr)

        # Retrieve new coefficients and constant term.
        try:
            coefs = {var: coef[index, :] for var, coef in self._coefs.items()}
            const = self._const[index]
        except IndexError as error:
            raise IndexError("Invalid expression slice {}: {}".format(
                string, error))

        return self._basetype(string, shape, coefs, const)

    def _common_basetype(self, other):
        assert isinstance(other, ComplexAffineExpression)

        if issubclass(other._basetype, self._basetype):
            return self._basetype
        else:
            return other._basetype

    @convert_operands(sameShape=True)
    @refine_operands(stop_at_affine=True)
    def __add__(self, other):
        """Denote addition from the right hand side."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        string = glyphs.clever_add(self.string, other.string)

        coefs = {}
        for var, coef in self._coefs.items():
            coefs[var] = coef+other._coefs[var] if var in other._coefs else coef
        for var, coef in other._coefs.items():
            coefs.setdefault(var, coef)

        const = self._const + other._const

        return self._common_basetype(other)(string, self._shape, coefs, const)

    @convert_operands(sameShape=True)
    @refine_operands(stop_at_affine=True)
    def __radd__(self, other):
        """Denote addition from the left hand side."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        return other.__add__(self)

    @convert_operands(sameShape=True)
    @refine_operands(stop_at_affine=True)
    def __sub__(self, other):
        """Denote substraction from the right hand side."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        string = glyphs.clever_sub(self.string, other.string)

        coefs = {}
        for var, coef in self._coefs.items():
            coefs[var] = coef-other._coefs[var] if var in other._coefs else coef
        for var, coef in other._coefs.items():
            coefs.setdefault(var, -coef)

        const = self._const - other._const

        return self._common_basetype(other)(string, self._shape, coefs, const)

    @convert_operands(sameShape=True)
    @refine_operands(stop_at_affine=True)
    def __rsub__(self, other):
        """Denote substraction with self on the right hand side."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        return other.__sub__(self)

    @cached_selfinverse_unary_operator
    def __neg__(self):
        """Denote negation."""
        string = glyphs.clever_neg(self.string)
        coefs  = {var: -coef for var, coef in self._coefs.items()}
        const  = -self._const

        return self._basetype(string, self._shape, coefs, const)

    @convert_operands(sameShape=True)
    @refine_operands(stop_at_affine=True)
    def __or__(self, other):
        r"""Denote the scalar product with self on the left hand side.

        For (complex) vectors :math:`a` and :math:`b` this is the dot product

        .. math::
            (a \mid b)
            &= \langle a, b \rangle \\
            &= a \cdot b \\
            &= b^H a.

        For (complex) matrices :math:`A` and :math:`B` this is the Frobenius
        inner product

        .. math::
            (A \mid B)
            &= \langle A, B \rangle_F \\
            &= A : B \\
            &= \operatorname{tr}(B^H A) \\
            &= \operatorname{vec}(B)^H \operatorname{vec}(\overline{A})

        .. note::
            Write ``(A|B)`` instead of ``A|B`` for the scalar product of ``A``
            and ``B`` to obtain correct operator binding within a larger
            expression context.
        """
        from .exp_quadratic import QuadraticExpression

        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        # Make a string description.
        string = glyphs.clever_dotp(
            self.string, other.string, other.complex, self.scalar)

        # Handle the complex case: Conjugate the right hand side.
        other = other.conj

        if other.constant:
            factor = other._const.T
            coefs  = {var: factor * coef for var, coef in self._coefs.items()}
            const  = factor * self._const
        elif self.constant:
            factor = self._const.T
            coefs  = {var: factor * coef for var, coef in other._coefs.items()}
            const  = factor * other._const
        else:
            # Compute the affine part of the product.
            affString = glyphs.affpart(string)
            affCoefs  = {}
            for var in set(self._coefs.keys()).union(other._coefs.keys()):
                if var not in other._coefs:
                    affCoefs[var] = other._const.T * self._coefs[var]
                elif var not in self._coefs:
                    affCoefs[var] = self._const.T * other._coefs[var]
                else:
                    affCoefs[var] = other._const.T * self._coefs[var] + \
                        self._const.T * other._coefs[var]
            affConst  = self._const.T * other._const
            affPart   = self._common_basetype(other)(
                affString, (1, 1), affCoefs, affConst)

            # Compute the quadratic part of the product.
            quadPart = {(v, w): self._coefs[v].T * other._coefs[w]
                for v in self._coefs for w in other._coefs}

            # Don't create quadratic expressions without a quadratic part.
            if not any(quadPart.values()):
                affPart._symbStr = string
                return affPart

            # Remember a factorization into two real scalars if applicable.
            # NOTE: If the user enters a multiplication a*b of two scalar affine
            #       expressions, then we have, at this point, self == a.T == a
            #       and other == b.conj.conj == b.
            if len(self) == 1 and len(other) == 1 \
            and self.isreal and other.isreal:
                factors = (self.refined, other.refined)
            else:
                factors = None

            return QuadraticExpression(
                string, quadPart, affPart, scalarFactors=factors)

        return self._common_basetype(other)(string, (1, 1), coefs, const)

    @convert_operands(sameShape=True)
    @refine_operands(stop_at_affine=True)
    def __ror__(self, other):
        """Denote the scalar product with self on the right hand side."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        return other.__or__(self)

    @convert_operands(rMatMul=True)
    @refine_operands(stop_at_affine=True)
    def __mul__(self, other):
        """Denote matrix multiplication from the right hand side."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        string = glyphs.clever_mul(self.string, other.string)

        shape = None
        if other.constant:
            if other._shape == (1, 1):
                factor = other._const[0]
                shape  = self._shape
            elif self._shape == (1, 1):
                factor = other._const
                shape  = other._shape
            else:
                # Use the identity vec(AB) = (Bᵀ ⊗ I)vec(A).
                factor = right_kronecker_I(other._const, self._shape[0],
                    reshape=other._shape, postT=True)

            coefs = {var: factor * coef for var, coef in self._coefs.items()}
            const = factor * self._const
        elif self.constant:
            if self._shape == (1, 1):
                factor = self._const[0]
                shape  = other._shape
            elif other._shape == (1, 1):
                factor = self._const
                shape  = self._shape
            else:
                # Use the identity vec(AB) = (I ⊗ A)vec(B).
                factor = left_kronecker_I(
                    self._const, other._shape[1], reshape=self._shape)

            coefs = {var: factor * coef for var, coef in other._coefs.items()}
            const = factor * other._const
        else:
            # If the result is scalar, allow for quadratic terms.
            if self._shape[0] == 1 and other._shape[1] == 1 \
            and self._shape[1] == other._shape[0]:
                result = self.T.__or__(other.conj)
                # NOTE: __or__ always creates a fresh expression.
                result._symbStr = string
                return result
            else:
                raise NotImplementedError(
                    "PICOS does not support multidimensional quadratic "
                    "expressions at this point. More precisely, one factor must"
                    " be constant or the result must be scalar.")

        if shape is None:
            shape = (self._shape[0], other._shape[1])

        return self._common_basetype(other)(string, shape, coefs, const)

    @convert_operands(lMatMul=True)
    @refine_operands(stop_at_affine=True)
    def __rmul__(self, other):
        """Denote matrix multiplication from the left hand side."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        return other.__mul__(self)

    @convert_operands(sameShape=True)
    @refine_operands(stop_at_affine=True)
    def __xor__(self, other):
        """Denote the elementwise (or Hadamard) product."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        string = glyphs.hadamard(self.string, other.string)

        if other.constant:
            factor = cvxopt.spdiag(other._const)
            coefs  = {var: factor * coef for var, coef in self._coefs.items()}
            const  = factor * self._const
        elif self.constant:
            factor = cvxopt.spdiag(self._const)
            coefs  = {var: factor * coef for var, coef in other._coefs.items()}
            const  = factor * other._const
        else:
            # If the result is scalar, allow for quadratic terms.
            if self._shape == (1, 1):
                result = self.__or__(other.conj)
                # NOTE: __or__ always creates a fresh expression.
                result._symbStr = string
                return result
            else:
                raise NotImplementedError(
                    "PICOS does not support multidimensional quadratic "
                    "expressions at this point. More precisely, one factor must"
                    " be constant or the result must be scalar.")

        return self._common_basetype(other)(string, self._shape, coefs, const)

    @convert_operands(sameShape=True)
    @refine_operands(stop_at_affine=True)
    def __rxor__(self, other):
        """Denote the elementwise (or Hadamard) product."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        return other.__xor__(self)

    @convert_operands()
    @refine_operands(stop_at_affine=True)
    def __matmul__(self, other):
        """Denote the Kronecker product from the right hand side."""
        def vectorized_kron(A, B):
            m, n  = self._shape
            p, q  = other._shape
            mn, r = A.size
            pq, s = B.size
            mnpq  = mn*pq

            assert 1 in (r, s)
            assert m*n == mn
            assert p*q == pq

            if r < s:
                A, P = cvx2np(A, (m, n)), []
                for j in range(s):
                    Bj = cvx2np(B[:, j], (p, q))
                    P.append(numpy.reshape(numpy.kron(A, Bj), (mnpq, 1), "F"))
            else:
                B, P = cvx2np(B, (p, q)), []
                for j in range(r):
                    Aj = cvx2np(A[:, j], (m, n))
                    P.append(numpy.reshape(numpy.kron(Aj, B), (mnpq, 1), "F"))

            assert P
            return load_data(numpy.vstack(P), typecode=tc)[0]

        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        cls = self._common_basetype(other)
        tc  = cls._get_typecode()

        string = glyphs.kron(self.string, other.string)

        m, n  = self._shape
        p, q  = other._shape
        shape = (m*p, n*q)

        if other.constant:
            coefs = {var: vectorized_kron(coef, other._const)
                for var, coef in self._coefs.items()}
        elif self.constant:
            coefs = {var: vectorized_kron(self._const, coef)
                for var, coef in other._coefs.items()}
        else:
            raise NotImplementedError(
                "PICOS does not support multidimensional quadratic expressions "
                "at this point. More precisely, at least one factor of the "
                "Kronecker product must be constant.")

        const = vectorized_kron(self._const, other._const)

        return cls(string, shape, coefs, const)

    @convert_operands()
    @refine_operands(stop_at_affine=True)
    def __rmatmul__(self, other):
        """Denote the Kronecker product from the left hand side."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        return other.__matmul__(self)

    def kron(self, other):
        """Denote the Kronecker product from the right hand side.

        Python 3 users can use the infix ``@`` operator instead.
        """
        # Python 2 does not have the @ operator.
        return self.__matmul__(other)

    def leftkron(self, other):
        """Denote the Kronecker product from the left hand side.

        Python 3 users can use the infix ``@`` operator instead.
        """
        # Python 2 does not have the @ operator.
        return self.__rmatmul__(other)

    @convert_operands(scalarRHS=True)
    @refine_operands(stop_at_affine=True)
    def __truediv__(self, other):
        """Denote elementwise division by a scalar constant."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        if not other.constant:
            raise TypeError(
                "You may only divide {} by a constant.".format(self.string))

        if other.is0:
            raise ZeroDivisionError(
                "Tried to divide {} by zero.".format(self.string))

        divisor = other._const[0]

        string = glyphs.div(self.string, other.string)
        coefs  = {var: coef / divisor for var, coef in self._coefs.items()}
        const  = self._const / divisor

        return self._common_basetype(other)(string, self._shape, coefs, const)

    @convert_operands(scalarLHS=True)
    @refine_operands(stop_at_affine=True)
    def __rtruediv__(self, other):
        """Denote elementwise division by scalar constant self."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        return other.__div__(self)

    def __div__(self, other):
        """Denote elementwise division by a scalar constant."""
        # Python 2 uses this instead of __truediv__.
        return self.__truediv__(other)

    def __rdiv__(self, other):
        """Denote elementwise division by scalar constant self."""
        # Python 2 uses this instead of __rtruediv__.
        return self.__rtruediv__(other)

    @convert_operands(horiCat=True)
    @refine_operands(stop_at_affine=True)
    def __and__(self, other):
        """Denote horizontal concatenation from the right hand side."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        string = glyphs.matrix_cat(self.string, other.string, horizontal=True)
        shape  = (self._shape[0], self._shape[1] + other._shape[1])

        coefs = {}
        for var in set(self._coefs.keys()).union(other._coefs.keys()):
            lhs = self._coefs[var]  if var in self._coefs  else cvxopt.spmatrix(
                [], [], [], (len(self), other._coefs[var].size[1]))
            rhs = other._coefs[var] if var in other._coefs else cvxopt.spmatrix(
                [], [], [], (len(other), self._coefs[var].size[1]))

            coefs[var] = cvxopt_vcat([lhs, rhs])

        const = cvxopt_vcat([self._const, other._const])

        return self._common_basetype(other)(string, shape, coefs, const)

    @convert_operands(horiCat=True)
    @refine_operands(stop_at_affine=True)
    def __rand__(self, other):
        """Denote horizontal concatenation from the left hand side."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        return other.__and__(self)

    @convert_operands(vertCat=True)
    @refine_operands(stop_at_affine=True)
    def __floordiv__(self, other):
        """Denote vertical concatenation from below."""
        def interleave_columns(upper, lower, upperRows, lowerRows, cols):
            p, q = upperRows, lowerRows
            return [column for columnPairs in [
                (upper[j*p:j*p+p, :], lower[j*q:j*q+q, :]) for j in range(cols)]
                for column in columnPairs]

        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        string = glyphs.matrix_cat(self.string, other.string, horizontal=False)

        p, q, c = self._shape[0], other._shape[0], self._shape[1]
        shape = (p + q, c)

        coefs = {}
        for var in set(self._coefs.keys()).union(other._coefs.keys()):
            upr = self._coefs[var]  if var in self._coefs  else cvxopt.spmatrix(
                [], [], [], (len(self), other._coefs[var].size[1]))
            lwr = other._coefs[var] if var in other._coefs else cvxopt.spmatrix(
                [], [], [], (len(other), self._coefs[var].size[1]))

            coefs[var] = cvxopt_vcat(interleave_columns(upr, lwr, p, q, c))

        const = cvxopt_vcat(
            interleave_columns(self._const, other._const, p, q, c))

        return self._common_basetype(other)(string, shape, coefs, const)

    @convert_operands(vertCat=True)
    @refine_operands(stop_at_affine=True)
    def __rfloordiv__(self, other):
        """Denote vertical concatenation from above."""
        if not isinstance(other, ComplexAffineExpression):
            return NotImplemented

        return other.__floordiv__(self)

    @convert_operands(scalarRHS=True)
    @refine_operands()  # Refine both sides to real if possible.
    def __pow__(self, other):
        """Denote exponentiation."""
        from .exp_powtrace import PowerTrace

        if not isinstance(other, AffineExpression):
            return NotImplemented

        if not self.scalar:
            raise TypeError("May only exponentiate a scalar expression.")

        if not other.constant:
            raise TypeError("The exponent must be constant.")

        exponent = other.value

        if exponent == 2:
            return (self | self)  # Works for complex base.
        else:
            return PowerTrace(self, exponent)  # Errors on complex base.

    @cached_unary_operator
    def __abs__(self):
        """Denote the Euclidean or Frobenius norm of the expression."""
        from . import Norm

        return Norm(self)

    # --------------------------------------------------------------------------
    # Properties and functions that describe the expression.
    # --------------------------------------------------------------------------

    @cached_property
    def _sparse_coefs(self):
        """Linear coefficients (re-)cast to sparse matrices."""
        return {var: cvxopt.sparse(coef) for var, coef in self._coefs.items()}

    @property
    def scalar(self):
        """Whether this is a scalar affine expression."""
        return self._shape == (1, 1)

    @property
    def constant(self):
        """Whether the expression involves no variables."""
        return not self._coefs

    @property
    def square(self):
        """Whether the expression is a square matrix."""
        return self._shape[0] == self._shape[1]

    @cached_property
    def hermitian(self):  # noqa (D402 thinks this includes a signature)
        """Whether the expression is a hermitian (or symmetric) matrix.

        A tolerance is used to compensate for small numeric errors that can
        occur when creating hermtian expressions by means of matrix
        multiplication, see
        :data:`~.exp_affine.RELATIVE_HERMITIANNESS_TOLERANCE`.

        If PICOS still rejects your expression as not hermitian (or as not
        symmetric), you can use :meth:`hermitianized` to correct larger numeric
        errors or the effects of noisy data.
        """
        return self.equals(self.H, relTol=RELATIVE_HERMITIANNESS_TOLERANCE)

    @cached_property
    def is0(self):
        """Whether this is a constant scalar, vector or matrix of all zeros."""
        # Must be constant.
        if self._coefs:
            return False

        # May not have a nonzero constant term.
        if self._const:
            return False

        return True

    @cached_property
    def is1(self):
        """Whether this is a constant scalar or vector of all ones."""
        # Must be a scalar or vector.
        if self._shape[0] != 1 and self._shape[1] != 1:
            return False

        # Must be constant.
        if self._coefs:
            return False

        # Constant term must be all ones.
        for index in range(len(self)):
            if self._const[index] != 1:
                return False

        return True

    @cached_property
    def isI(self):
        """Whether this is a constant identity matrix."""
        m, n = self._shape

        # Must be a square matrix.
        if m != n:
            return False

        # Must be constant.
        if self._coefs:
            return False

        # Constant term must be the identity.
        for row in range(m):
            for col in range(n):
                if self._const[col*m + row] != int(row == col):
                    return False

        return True

    @cached_property
    def isreal(self):
        """Whether the expression is always real-valued."""
        if any(self._const.imag()):
            return False

        for coef in self._coefs.values():
            if any(coef.imag()):
                return False

        return True

    @property
    def complex(self):
        """Whether the expression can be complex-valued."""
        return not self.isreal

    @convert_operands()
    def equals(self, other, absTol=None, relTol=None):
        """Check mathematical equality with another affine expression.

        Checks whether the affine expression involves the same variables with
        the same coefficients and an equal constant term as the given PICOS
        (affine) expression or constant term.

        The type of both expressions may differ. In particular, a
        :class:`ComplexAffineExpression` with real coefficients and constant can
        be equal to an :class:`AffineExpression`.

        If the argument is a constant term, no reshaping or broadcasting is used
        to bring it to the same shape as this expression. In particular,

            - ``0`` refers to a scalar zero (see also :meth:`is0`),
            - lists and tuples are treated as column vectors and
            - algebraic strings must specify a shape (see
              :func:`~.data.load_data`).

        :param other: Another PICOS expression or a constant numeric data value
            supported by :func:`~.data.load_data`.
        :param absTol: As long as all absolute differences between scalar
            entries of the coefficient matrices and the constant terms being
            compared does not exceed this bound, consider the expressions equal.
        :param relTol: As long as all absolute differences between scalar
            entries of the coefficient matrices and the constant terms being
            compared divided by the maximum absolute value found in either term
            does not exceed this bound, consider the expressions equal.

        :Example:

        >>> from picos import Constant
        >>> A = Constant("A", 0, (5,5))
        >>> repr(A)
        '<5×5 Real Constant: A>'
        >>> A.is0
        True
        >>> A.equals(0)
        False
        >>> A.equals("|0|(5,5)")
        True
        >>> repr(A*1j)
        '<5×5 Complex Constant: A·1j>'
        >>> A.equals(A*1j)
        True
        """
        def differ(A, B):
            Z = A - B
            if Z:
                if not absTol and not relTol:
                    return True

                M = max(abs(Z))
                if relTol:
                    N = max(max(abs(A)), max(abs(B)))

                if absTol and relTol:
                    if M > absTol and M / N > relTol:
                        return True
                elif absTol:
                    if M > absTol:
                        return True
                else:
                    if M / N > relTol:
                        return True
            return False

        if self is other:
            return True

        if not isinstance(other, ComplexAffineExpression):
            return False

        if self._shape != other._shape:
            return False

        if differ(self._const, other._const):
            return False

        for var in other._coefs:
            if var not in self._coefs:
                return False

        for var, coef in self._coefs.items():
            if var not in other._coefs:
                return False

            if differ(coef, other._coefs[var]):
                return False

        return True

    # --------------------------------------------------------------------------
    # Methods and properties that return modified copies.
    # --------------------------------------------------------------------------

    def renamed(self, string):
        """Return the expression with a modified string description."""
        return self._basetype(string, self._shape, self._coefs, self._const)

    def reshaped(self, shape):
        """Return the expression reshaped in column-major order.

        :Example:

        >>> from picos import Constant
        >>> C = Constant("C", range(6), (2, 3))
        >>> print(C)
        [ 0.00e+00  2.00e+00  4.00e+00]
        [ 1.00e+00  3.00e+00  5.00e+00]
        >>> print(C.reshaped((3, 2)))
        [ 0.00e+00  3.00e+00]
        [ 1.00e+00  4.00e+00]
        [ 2.00e+00  5.00e+00]
        """
        shape = load_shape(shape, wildcards=True)

        if shape == self._shape:
            return self
        elif shape == (None, None):
            return self

        length = len(self)

        if shape[0] is None:
            shape = (length // shape[1], shape[1])
        elif shape[1] is None:
            shape = (shape[0], length // shape[0])

        if shape[0]*shape[1] != length:
            raise ValueError("Can only reshape to a matrix of same size.")

        string = glyphs.reshaped(self.string, glyphs.shape(shape))
        return self._basetype(string, shape, self._coefs, self._const)

    def broadcasted(self, shape):
        """Return the expression broadcasted to the given shape.

        :Example:

        >>> from picos import Constant
        >>> C = Constant("C", range(6), (2, 3))
        >>> print(C)
        [ 0.00e+00  2.00e+00  4.00e+00]
        [ 1.00e+00  3.00e+00  5.00e+00]
        >>> print(C.broadcasted((6, 6)))
        [ 0.00e+00  2.00e+00  4.00e+00  0.00e+00  2.00e+00  4.00e+00]
        [ 1.00e+00  3.00e+00  5.00e+00  1.00e+00  3.00e+00  5.00e+00]
        [ 0.00e+00  2.00e+00  4.00e+00  0.00e+00  2.00e+00  4.00e+00]
        [ 1.00e+00  3.00e+00  5.00e+00  1.00e+00  3.00e+00  5.00e+00]
        [ 0.00e+00  2.00e+00  4.00e+00  0.00e+00  2.00e+00  4.00e+00]
        [ 1.00e+00  3.00e+00  5.00e+00  1.00e+00  3.00e+00  5.00e+00]
        """
        shape = load_shape(shape, wildcards=True)
        shape = blend_shapes(shape, self._shape)

        if shape == self._shape:
            return self

        vdup = shape[0] // self._shape[0]
        hdup = shape[1] // self._shape[1]

        if (self._shape[0] * vdup, self._shape[1] * hdup) != shape:
            raise ValueError("Cannot broadcast from shape {} to {}."
                .format(glyphs.shape(self._shape), glyphs.shape(shape)))

        if self._shape == (1, 1):
            string = glyphs.matrix(self.string)
            return (self * cvxopt.matrix(1.0, shape)).renamed(string)

        string = glyphs.bcasted(self.string, glyphs.shape(shape))
        return self.leftkron(cvxopt.matrix(1.0, (vdup, hdup))).renamed(string)

    def reshaped_or_broadcasted(self, shape):
        """Return the expression :meth:`reshaped` or :meth:`broadcasted`.

        Unlike with :meth:`reshaped` and :meth:`broadcasted`, the target shape
        may not contain a wildcard character.

        If the wildcard-free target shape has the same number of elements as
        the current shape, then this is the same as :meth:`reshaped`, otherwise
        it is the same as :meth:`broadcasted`.
        """
        shape = load_shape(shape, wildcards=False)

        try:
            if shape[0]*shape[1] == len(self):
                return self.reshaped(shape)
            else:
                return self.broadcasted(shape)
        except ValueError:
            raise ValueError("Cannot reshape or broadcast from shape {} to {}."
                .format(glyphs.shape(self._shape), glyphs.shape(shape)))

    @cached_property
    def hermitianized(self):
        r"""The expression projected onto the subspace of hermitian matrices.

        For a square (complex) affine expression :math:`A`, this is
        :math:`\frac{1}{2}(A + A^H)`.

        If the expression is not complex, then this is the projection onto the
        subspace of symmetric matrices.
        """
        if not self.square:
            raise TypeError("Cannot hermitianize non-square {}.".format(self))

        return (self + self.H)/2

    @cached_property
    def real(self):
        """Real part of a complex affine expression."""
        return AffineExpression(
            glyphs.real(self.string),
            self._shape,
            {var: coef.real() for var, coef in self._coefs.items()},
            self._const.real())

    @cached_property
    def imag(self):
        """Imaginary part of a complex affine expression."""
        return AffineExpression(
            glyphs.imag(self.string),
            self._shape,
            {var: coef.imag() for var, coef in self._coefs.items()},
            self._const.imag())

    @cached_property
    def lin(self):
        """Linear part of the affine expression."""
        return self._basetype(
            glyphs.linpart(self._symbStr), self._shape, self._coefs)

    @cached_property
    def cst(self):
        """Constant part of the affine expression."""
        return self._basetype(
            glyphs.cstpart(self._symbStr), self._shape, constant=self._const)

    @cached_selfinverse_property
    def T(self):
        """Matrix transpose."""
        if len(self) == 1:
            return self

        # Construct a commutation matrix to transpose the vectorized data.
        n, m = self._shape
        d = n * m
        V = [1]*d
        I = range(d)
        J = [(k % m)*n + k // m for k in I]
        K = cvxopt.spmatrix(V, I, J, (d, d), self._typecode)

        string = glyphs.transp(self.string)
        shape  = (self._shape[1], self._shape[0])
        coefs  = {var: K * coef for var, coef in self._coefs.items()}
        const  = K * self._const

        return self._basetype(string, shape, coefs, const)

    @cached_selfinverse_property
    def conj(self):
        """Complex conjugate."""
        string = glyphs.conj(self.string)
        coefs  = {var: coef.H.T for var, coef in self._coefs.items()}
        const  = self._const.H.T

        return self._basetype(string, self._shape, coefs, const)

    @cached_selfinverse_property
    def H(self):
        """Conjugate (or Hermitian) transpose."""
        return self.T.conj.renamed(glyphs.htransp(self._symbStr))

    def _square_equal_subsystem_dims(self, diagLen):
        """Support :func:`partial_trace` and :func:`partial_transpose`."""
        m, n = self._shape
        k = math.log(m, diagLen)

        if m != n or int(k) != k:
            raise TypeError("The expression has shape {} so it cannot be "
                "decomposed into subsystems of shape {}.".format(
                glyphs.shape(self._shape), glyphs.shape((diagLen,)*2)))

        return ((diagLen,)*2,)*int(k)

    def partial_transpose(self, subsystems, dimensions=2):
        r"""Return the expression with selected subsystems transposed.

        If the expression can be written as
        :math:`A_0 \otimes \cdots \otimes A_{n-1}` for matrices
        :math:`A_0, \ldots, A_{n-1}` with shapes given in ``dimensions``, then
        this returns :math:`B_0 \otimes \cdots \otimes B_{n-1}` with
        :math:`B_i = A_i^T`, if ``i in subsystems`` (with :math:`i = -1` read as
        :math:`n-1`), and :math:`B_i = A_i`, otherwise.

        :param subsystems: A collection of or a single subystem number, indexed
            from zero, corresponding to subsystems that shall be transposed.
            The value :math:`-1` refers to the last subsystem.
        :type subsystems: int or tuple or list

        :param dimensions: Either an integer :math:`d` so that the subsystems
            are assumed to be all of shape :math:`d \times d`, or a sequence of
            subsystem shapes where an integer :math:`d` within the sequence is
            read as :math:`d \times d`. In any case, the elementwise product
            over all subsystem shapes must equal the expression's shape.
        :type dimensions: int or tuple or list

        :raises TypeError: If the subsystems do not match the expression.
        :raises IndexError: If the subsystem selection is invalid.

        :Example:

        >>> from picos import Constant
        >>> A = Constant("A", range(16), (4, 4))
        >>> print(A) #doctest: +NORMALIZE_WHITESPACE
        [ 0.00e+00  4.00e+00  8.00e+00  1.20e+01]
        [ 1.00e+00  5.00e+00  9.00e+00  1.30e+01]
        [ 2.00e+00  6.00e+00  1.00e+01  1.40e+01]
        [ 3.00e+00  7.00e+00  1.10e+01  1.50e+01]
        >>> A0 = A.partial_transpose(0); A0
        <4×4 Real Constant: A.{[2×2]ᵀ⊗[2×2]}>
        >>> print(A0) #doctest: +NORMALIZE_WHITESPACE
        [ 0.00e+00  4.00e+00  2.00e+00  6.00e+00]
        [ 1.00e+00  5.00e+00  3.00e+00  7.00e+00]
        [ 8.00e+00  1.20e+01  1.00e+01  1.40e+01]
        [ 9.00e+00  1.30e+01  1.10e+01  1.50e+01]
        >>> A1 = A.partial_transpose(1); A1
        <4×4 Real Constant: A.{[2×2]⊗[2×2]ᵀ}>
        >>> print(A1) #doctest: +NORMALIZE_WHITESPACE
        [ 0.00e+00  1.00e+00  8.00e+00  9.00e+00]
        [ 4.00e+00  5.00e+00  1.20e+01  1.30e+01]
        [ 2.00e+00  3.00e+00  1.00e+01  1.10e+01]
        [ 6.00e+00  7.00e+00  1.40e+01  1.50e+01]
        """
        m, n = self._shape

        if isinstance(dimensions, int):
            dimensions = self._square_equal_subsystem_dims(dimensions)
        else:
            dimensions = [
                (d, d) if isinstance(d, int) else d for d in dimensions]

        if reduce(
                lambda x, y: (x[0]*y[0], x[1]*y[1]), dimensions) != self._shape:
            raise TypeError("Subsystem dimensions do not match expression.")

        if isinstance(subsystems, int):
            subsystems = (subsystems,)
        elif not subsystems:
            return self

        numSys     = len(dimensions)
        subsystems = set(numSys - 1 if sys == -1 else sys for sys in subsystems)

        for sys in subsystems:
            if not isinstance(sys, int):
                raise IndexError("Subsystem indices must be integer, not {}."
                    .format(type(sys).__name__))
            elif sys < 0:
                raise IndexError("Subsystem indices must be nonnegative."
                    .format(sys))
            elif sys >= numSys:
                raise IndexError(
                    "Subsystem index {} out of range for {} systems total."
                    .format(sys, numSys))

        # If all subsystems are transposed, this is regular transposition.
        if len(subsystems) == numSys:
            return self.T

        # Prepare sparse K such that K·vec(A) = vec(partial_transpose(A)).
        d = m * n
        V = [1]*d
        I = range(d)
        J = cvxopt.matrix(I)
        T = cvxopt.matrix(0, J.size)
        obh, obw   = 1, 1
        sysStrings = None

        # Apply transpositions starting with the rightmost Kronecker factor.
        for sys in range(numSys - 1, -1, -1):
            # Shape of current system.
            p, q = dimensions[sys]
            sysString = glyphs.matrix(glyphs.shape((p, q)))

            # Height/width of "inner" blocks being moved, initially scalars.
            ibh, ibw = obh, obw

            # Heigh/width of "outer" blocks whose relative position is
            # maintained but that are subject to transposition independently.
            # In the last iteration this is the shape of the resulting matrix.
            obh *= p
            obw *= q

            # Only transpose selected subsystems.
            if sys not in subsystems:
                sysStrings = glyphs.kron(sysString, sysStrings) \
                    if sysStrings else sysString
                continue
            else:
                sysStrings = glyphs.kron(glyphs.transp(sysString), sysStrings) \
                    if sysStrings else glyphs.transp(sysString)

            # Shape of outer blocks after transposition.
            obhT, obwT = obw // ibw * ibh, obh // ibh * ibw

            # Shape of full matrix after transposition.
            mT, nT = m // obh * obhT, n // obw * obwT

            for vi in I:
                # Full matrix column and row.
                c, r = divmod(vi, m)

                # Outer block vertical   index and row    within outer block,
                # outer block horizontal index and column within outer block.
                obi, obr = divmod(r, obh)
                obj, obc = divmod(c, obw)

                # Inner block vertical   index and row    within inner block,
                # inner block horizontal index and column within inner block.
                ibi, ibr = divmod(obr, ibh)
                ibj, ibc = divmod(obc, ibw)

                # (1) ibi*ibw + ibc is column within the transposed outer block;
                # adding obj*obwT yields the column in the transposed matrix.
                # (2) ibj*ibh + ibr is row within the transposed outer block;
                # adding obi*obhT yields the row in the transposed matrix.
                # (3) tvi is index within the vectorized transposed matrix.
                tvi = (obj*obwT + ibi*ibw + ibc)*mT \
                    + (obi*obhT + ibj*ibh + ibr)

                # Prepare the transposition.
                T[tvi] = J[vi]

            # Apply the transposition.
            J, T = T, J
            m, n, obh, obw = mT, nT, obhT, obwT

        # Finalize the partial commutation matrix.
        K = cvxopt.spmatrix(V, I, J, (d, d), self._typecode)

        string = glyphs.ptransp_(self.string, sysStrings)
        shape  = (m, n)
        coefs  = {var: K * coef for var, coef in self._coefs.items()}
        const  = K * self._const

        return self._basetype(string, shape, coefs, const)

    @cached_property
    def T0(self):
        r"""Expression with the first :math:`2 \times 2` subsystem transposed.

        Only available for a :math:`2^k \times 2^k` matrix with all subsystems
        of shape :math:`2 \times 2`. Use :meth:`partial_transpose` otherwise.
        """
        return self.partial_transpose(subsystems=0)

    @cached_property
    def T1(self):
        r"""Expression with the second :math:`2 \times 2` subsystem transposed.

        Only available for a :math:`2^k \times 2^k` matrix with all subsystems
        of shape :math:`2 \times 2`. Use :meth:`partial_transpose` otherwise.
        """
        return self.partial_transpose(subsystems=1)

    @cached_property
    def T2(self):
        r"""Expression with the third :math:`2 \times 2` subsystem transposed.

        Only available for a :math:`2^k \times 2^k` matrix with all subsystems
        of shape :math:`2 \times 2`. Use :meth:`partial_transpose` otherwise.
        """
        return self.partial_transpose(subsystems=2)

    @cached_property
    def T3(self):
        r"""Expression with the fourth :math:`2 \times 2` subsystem transposed.

        Only available for a :math:`2^k \times 2^k` matrix with all subsystems
        of shape :math:`2 \times 2`. Use :meth:`partial_transpose` otherwise.
        """
        return self.partial_transpose(subsystems=3)

    @cached_property
    def Tl(self):
        r"""Expression with the last :math:`2 \times 2` subsystem transposed.

        Only available for a :math:`2^k \times 2^k` matrix with all subsystems
        of shape :math:`2 \times 2`. Use :meth:`partial_transpose` otherwise.
        """
        return self.partial_transpose(subsystems=-1)

    @cached_property
    def sum(self):
        """Sum over all scalar elements of the expression."""
        # NOTE: glyphs.clever_dotp detects this case and uses the sum glyph.
        # NOTE: 1 on the right hand side in case self is complex.
        return (self | 1)

    @cached_property
    def tr(self):
        """Trace of a square expression."""
        if not self.square:
            raise TypeError("Cannot compute the trace of non-square {}."
                .format(self.string))

        # NOTE: glyphs.clever_dotp detects this case and uses the trace glyph.
        # NOTE: "I" on the right hand side in case self is complex.
        return (self | "I")

    def partial_trace(self, subsystems, dimensions=2):
        r"""Return the partial trace over selected subsystems.

        If the expression can be written as
        :math:`A_0 \otimes \cdots \otimes A_{n-1}` for matrices
        :math:`A_0, \ldots, A_{n-1}` with shapes given in ``dimensions``, then
        this returns :math:`B_0 \otimes \cdots \otimes B_{n-1}` with
        :math:`B_i = \operatorname{tr}(A_i)`, if ``i in subsystems`` (with
        :math:`i = -1` read as :math:`n-1`), and :math:`B_i = A_i`, otherwise.

        :param subsystems: A collection of or a single subystem number, indexed
            from zero, corresponding to subsystems that shall be traced over.
            The value :math:`-1` refers to the last subsystem.
        :type subsystems: int or tuple or list

        :param dimensions: Either an integer :math:`d` so that the subsystems
            are assumed to be all of shape :math:`d \times d`, or a sequence of
            subsystem shapes where an integer :math:`d` within the sequence is
            read as :math:`d \times d`. In any case, the elementwise product
            over all subsystem shapes must equal the expression's shape.
        :type dimensions: int or tuple or list

        :raises TypeError: If the subsystems do not match the expression or if
            a non-square subsystem is to be traced over.
        :raises IndexError: If the subsystem selection is invalid in any other
            way.

        :Example:

        >>> from picos import Constant
        >>> A = Constant("A", range(16), (4, 4))
        >>> print(A) #doctest: +NORMALIZE_WHITESPACE
        [ 0.00e+00  4.00e+00  8.00e+00  1.20e+01]
        [ 1.00e+00  5.00e+00  9.00e+00  1.30e+01]
        [ 2.00e+00  6.00e+00  1.00e+01  1.40e+01]
        [ 3.00e+00  7.00e+00  1.10e+01  1.50e+01]
        >>> A0 = A.partial_trace(0); A0
        <2×2 Real Constant: A.{tr([2×2])⊗[2×2]}>
        >>> print(A0) #doctest: +NORMALIZE_WHITESPACE
        [ 1.00e+01  1.80e+01]
        [ 1.20e+01  2.00e+01]
        >>> A1 = A.partial_trace(1); A1
        <2×2 Real Constant: A.{[2×2]⊗tr([2×2])}>
        >>> print(A1) #doctest: +NORMALIZE_WHITESPACE
        [ 5.00e+00  2.10e+01]
        [ 9.00e+00  2.50e+01]
        """
        # Shape of the original matrix.
        m, n = self._shape

        if isinstance(dimensions, int):
            dimensions = self._square_equal_subsystem_dims(dimensions)
        else:
            dimensions = [
                (d, d) if isinstance(d, int) else d for d in dimensions]

        if reduce(
                lambda x, y: (x[0]*y[0], x[1]*y[1]), dimensions) != self._shape:
            raise TypeError("Subsystem dimensions do not match expression.")

        if isinstance(subsystems, int):
            subsystems = (subsystems,)
        elif not subsystems:
            return self

        numSys     = len(dimensions)
        subsystems = set(numSys - 1 if sys == -1 else sys for sys in subsystems)

        for sys in subsystems:
            if not isinstance(sys, int):
                raise IndexError("Subsystem indices must be integer, not {}."
                    .format(type(sys).__name__))
            elif sys < 0:
                raise IndexError("Subsystem indices must be nonnegative."
                    .format(sys))
            elif sys >= numSys:
                raise IndexError(
                    "Subsystem index {} out of range for {} systems total."
                    .format(sys, numSys))
            elif dimensions[sys][0] != dimensions[sys][1]:
                raise TypeError(
                    "Subsystem index {} refers to a non-square subsystem that "
                    "cannot be traced over.".format(sys))

        # If all subsystems are traced over, this is the regular trace.
        if len(subsystems) == numSys:
            return self.tr

        # Prepare sparse T such that T·vec(A) = vec(partial_trace(A)).
        T = []

        # Compute factors of T, one for each subsystem being traced over.
        ibh, ibw   = m, n
        sysStrings = None
        for sys in range(numSys):
            # Shape of current system.
            p, q = dimensions[sys]
            sysString = glyphs.matrix(glyphs.shape((p, q)))

            # Heigh/width of "outer" blocks whose relative position is
            # maintained but that are reduced independently to the size of an
            # inner block if the current system is to be traced over.
            obh, obw = ibh, ibw

            # Height/width of "inner" blocks that are summed if they are
            # main-diagonal blocks of an outer block.
            ibh, ibw = obh // p, obw // q

            # Only trace over selected subsystems.
            if sys not in subsystems:
                sysStrings = glyphs.kron(sysStrings, sysString) \
                    if sysStrings else sysString
                continue
            else:
                sysStrings = glyphs.kron(sysStrings, glyphs.trace(sysString)) \
                    if sysStrings else glyphs.trace(sysString)

            # Shape of new matrix.
            assert p == q
            mN, nN = m // p, n // p

            # Prepare one factor of T.
            oldLen = m  * n
            newLen = mN * nN
            V, I, J = [1]*(newLen*p), [], []
            shape = (newLen, oldLen)

            # Determine the summands that make up each entry of the new matrix.
            for viN in range(newLen):
                # A column/row pair that represents a scalar in the new matrix
                # and a number of p scalars within different on-diagonal inner
                # blocks but within the same outer block in the old matrix.
                cN, rN = divmod(viN, mN)

                # Index pair (obi, obj) for outer block in question, row/column
                # pair (ibr, ibc) identifies the scalar within each inner block.
                obi, ibr = divmod(rN, ibh)
                obj, ibc = divmod(cN, ibw)

                # Collect summands for the current entry of the new matrix; one
                # scalar per on-diagonal inner block.
                for k in range(p):
                    rO = obi*obh + k*ibh + ibr
                    cO = obj*obw + k*ibw + ibc
                    I.append(viN)
                    J.append(cO*m + rO)

            # Store the operator that performs the current subsystem trace.
            T.insert(0, cvxopt.spmatrix(V, I, J, shape, self._typecode))

            # Make next iteration work on the new matrix.
            m, n = mN, nN

        # Multiply out the linear partial trace operator T.
        # TODO: Fast matrix multiplication dynamic program useful here?
        T = reduce(lambda A, B: A*B, T)

        string = glyphs.ptrace_(self.string, sysStrings)
        shape  = (m, n)
        coefs  = {var: T * coef for var, coef in self._coefs.items()}
        const  = T * self._const

        return self._basetype(string, shape, coefs, const)

    @cached_property
    def tr0(self):
        r"""Expression with the first :math:`2 \times 2` subsystem traced out.

        Only available for a :math:`2^k \times 2^k` matrix with all subsystems
        of shape :math:`2 \times 2`. Use :meth:`partial_trace` otherwise.
        """
        return self.partial_trace(subsystems=0)

    @cached_property
    def tr1(self):
        r"""Expression with the second :math:`2 \times 2` subsystem traced out.

        Only available for a :math:`2^k \times 2^k` matrix with all subsystems
        of shape :math:`2 \times 2`. Use :meth:`partial_trace` otherwise.
        """
        return self.partial_trace(subsystems=1)

    @cached_property
    def tr2(self):
        r"""Expression with the third :math:`2 \times 2` subsystem traced out.

        Only available for a :math:`2^k \times 2^k` matrix with all subsystems
        of shape :math:`2 \times 2`. Use :meth:`partial_trace` otherwise.
        """
        return self.partial_trace(subsystems=2)

    @cached_property
    def tr3(self):
        r"""Expression with the fourth :math:`2 \times 2` subsystem traced out.

        Only available for a :math:`2^k \times 2^k` matrix with all subsystems
        of shape :math:`2 \times 2`. Use :meth:`partial_trace` otherwise.
        """
        return self.partial_trace(subsystems=3)

    @cached_property
    def trl(self):
        r"""Expression with the last :math:`2 \times 2` subsystem traced out.

        Only available for a :math:`2^k \times 2^k` matrix with all subsystems
        of shape :math:`2 \times 2`. Use :meth:`partial_trace` otherwise.
        """
        return self.partial_trace(subsystems=-1)

    @cached_property
    def vec(self):
        """Column-major vectorization of the expression as a column vector.

        .. note::
            Given an expression ``A``, ``A.vec`` and ``A[:]`` produce the same
            result (up to its string description) but ``A.vec`` is faster and
            its result is cached.

        :Example:

        >>> from picos import Constant
        >>> A = Constant("A", [[1, 2], [3, 4]])
        >>> A.vec.equals(A[:])
        True
        >>> A[:] is A[:]
        False
        >>> A.vec is A.vec
        True
        """
        if self._shape[1] == 1:
            return self
        else:
            return self._basetype(glyphs.vec(self.string), (len(self), 1),
                self._coefs, self._const)

    def dupvec(self, n):
        """Return a (repeated) column-major vectorization of the expression.

        :param int n: Number of times to duplicate the vectorization.

        :returns: A column vector.

        :Example:

        >>> from picos import Constant
        >>> A = Constant("A", [[1, 2], [3, 4]])
        >>> A.dupvec(1) is A.vec
        True
        >>> A.dupvec(3).equals(A.vec // A.vec // A.vec)
        True
        """
        if not isinstance(n, int):
            raise TypeError("Number of copies must be integer.")

        if n < 1:
            raise ValueError("Number of copies must be positive.")

        if n == 1:
            return self.vec
        else:
            string = glyphs.vec(glyphs.comma(self.string, n))
            shape  = (len(self)*n, 1)
            coefs  = {var: cvxopt_vcat([coef]*n)
                for var, coef in self._coefs.items()}
            const  = cvxopt_vcat([self._const]*n)

            return self._basetype(string, shape, coefs, const)

    @cached_property
    def trilvec(self):
        r"""Column-major vectorization of the lower triangular part.

        :returns:
            A column vector of all elements :math:`A_{ij}` that satisfy
            :math:`i \geq j`.

        .. note::

            If you want a row-major vectorization instead, write ``A.T.triuvec``
            instead of ``A.trilvec``.

        :Example:

        >>> from picos import Constant
        >>> A = Constant("A", [[1, 2], [3, 4], [5, 6]])
        >>> print(A)
        [ 1.00e+00  2.00e+00]
        [ 3.00e+00  4.00e+00]
        [ 5.00e+00  6.00e+00]
        >>> print(A.trilvec)
        [ 1.00e+00]
        [ 3.00e+00]
        [ 5.00e+00]
        [ 4.00e+00]
        [ 6.00e+00]
        """
        m, n = self._shape

        if n == 1:  # Column vector or scalar.
            return self
        elif m == 1:  # Row vector.
            return self[0]

        # Build a transformation D such that D·vec(A) = trilvec(A).
        rows = [j*m + i for j in range(n) for i in range(m) if i >= j]
        d    = len(rows)
        D    = cvxopt.spmatrix([1]*d, range(d), rows, (d, len(self)))

        string = glyphs.trilvec(self.string)
        shape  = (d, 1)
        coefs  = {var: D*coef for var, coef in self._coefs.items()}
        const  = D*self._const

        return self._basetype(string, shape, coefs, const)

    @cached_property
    def triuvec(self):
        r"""Column-major vectorization of the upper triangular part.

        :returns:
            A column vector of all elements :math:`A_{ij}` that satisfy
            :math:`i \leq j`.

        .. note::

            If you want a row-major vectorization instead, write ``A.T.trilvec``
            instead of ``A.triuvec``.

        :Example:

        >>> from picos import Constant
        >>> A = Constant("A", [[1, 2, 3], [4, 5, 6]])
        >>> print(A)
        [ 1.00e+00  2.00e+00  3.00e+00]
        [ 4.00e+00  5.00e+00  6.00e+00]
        >>> print(A.triuvec)
        [ 1.00e+00]
        [ 2.00e+00]
        [ 5.00e+00]
        [ 3.00e+00]
        [ 6.00e+00]
        """
        m, n = self._shape

        if m == 1:  # Row vector or scalar.
            return self
        elif n == 1:  # Column vector.
            return self[0]

        # Build a transformation D such that D·vec(A) = triuvec(A).
        rows = [j*m + i for j in range(n) for i in range(m) if i <= j]
        d    = len(rows)
        D    = cvxopt.spmatrix([1]*d, range(d), rows, (d, len(self)))

        string = glyphs.triuvec(self.string)
        shape  = (d, 1)
        coefs  = {var: D*coef for var, coef in self._coefs.items()}
        const  = D*self._const

        return self._basetype(string, shape, coefs, const)

    def dupdiag(self, n):
        """Return a matrix with the (repeated) expression on the diagonal.

        Vectorization is performed in column-major order.

        :param int n: Number of times to duplicate the vectorization.
        """
        # Vectorize and duplicate the expression.
        vec = self.dupvec(n)
        d   = len(vec)

        # Build a transformation D such that D·vec(A) = vec(diag(vec(A))).
        ones = [1]*d
        D    = cvxopt.spdiag(ones)[:]
        D    = cvxopt.spmatrix(ones, D.I, range(d), (D.size[0], d))

        string = glyphs.diag(vec.string)
        shape  = (d, d)
        coefs  = {var: D*coef for var, coef in vec._coefs.items()}
        const  = D*vec._const

        return self._basetype(string, shape, coefs, const)

    @cached_property
    def diag(self):
        """Diagonal matrix with the expression on the main diagonal.

        Vectorization is performed in column-major order.
        """
        return self.dupdiag(1)

    @cached_property
    def maindiag(self):
        """The main diagonal of the expression as a column vector."""
        if 1 in self._shape:
            return self[0]

        # Build a transformation D such that D·vec(A) = diag(A).
        step = self._shape[0] + 1
        rows = [i*step for i in range(min(self._shape))]
        d    = len(rows)
        D    = cvxopt.spmatrix([1]*d, range(d), rows, (d, len(self)))

        string = glyphs.maindiag(self.string)
        shape  = (d, 1)
        coefs  = {var: D*coef for var, coef in self._coefs.items()}
        const  = D*self._const

        return self._basetype(string, shape, coefs, const)

    # --------------------------------------------------------------------------
    # Constraint-creating operators, and _predict.
    # --------------------------------------------------------------------------

    @classmethod
    def _predict(cls, subtype, relation, other):
        assert isinstance(subtype, cls.Subtype)

        from .set import Set

        if relation == operator.__eq__:
            if issubclass(other.clstype, ComplexAffineExpression):
                return ComplexAffineConstraint.make_type(dim=subtype.dim)
        elif relation == operator.__lshift__:
            if issubclass(other.clstype, ComplexAffineExpression):
                return ComplexLMIConstraint.make_type(int(subtype.dim**0.5))
            elif issubclass(other.clstype, Set):
                return other >> ExpressionType(cls, subtype)
        elif relation == operator.__rshift__:
            if issubclass(other.clstype, ComplexAffineExpression):
                return ComplexLMIConstraint.make_type(int(subtype.dim**0.5))

        return NotImplemented

    @convert_operands(sameShape=True)
    @validate_prediction
    @refine_operands()
    def __eq__(self, other):
        if isinstance(other, ComplexAffineExpression):
            return ComplexAffineConstraint(self, other)
        else:
            return NotImplemented

    # Since we define __eq__, __hash__ is not inherited. Do this manually.
    __hash__ = Expression.__hash__

    @convert_operands(sameShape=True)
    @validate_prediction
    @refine_operands()
    def __lshift__(self, other):
        from .set import Set

        if isinstance(other, ComplexAffineExpression):
            return ComplexLMIConstraint(self, Constraint.LE, other)
        elif isinstance(other, Set):
            # NOTE: We need to swap explicitly because Python does not consider
            #       A << B the same as B >> A.
            return other.__rshift__(self)
        else:
            return NotImplemented

    @convert_operands(sameShape=True)
    @validate_prediction
    @refine_operands()
    def __rshift__(self, other):
        if isinstance(other, ComplexAffineExpression):
            return ComplexLMIConstraint(self, Constraint.GE, other)
        else:
            return NotImplemented

    # --------------------------------------------------------------------------
    # Advanced interface for PICOS-internal use.
    # --------------------------------------------------------------------------

    def sparse_rows(
            self, varOffsetMap, lowerTriangle=False, upperTriangle=False,
            indexFunction=None):
        """Return a sparse list representation of the expression.

        The method is intended for internal use: It simplifies passing affine
        constraints to solvers that support only scalar constraints. The idea is
        to pose the constraint as a single (multidimensional) affine expression
        bounded by zero, and use the coefficients and the constant term of this
        expression to fill the solver's constraint matrix (with columns
        representing scalar variables and rows representing scalar constraints).

        :param dict varOffsetMap: Maps variables to column offsets.
        :param bool lowerTriangle: Whether to return only the lower triangular
            part of the expression.
        :param bool upperTriangle: Whether to return only the upper triangular
            part of the expression.
        :param indexFunction: Instead of adding the local variable index to the
            value returned by varOffsetMap, use the return value of this
            function, that takes as argument the variable and its local index,
            as the "column index", which need not be an integer. When this
            parameter is passed, the parameter varOffsetMap is ignored.

        :returns: A list of triples (J, V, c) where J contains column indices
            (representing scalar variables), V contains coefficients for each
            column index and c is a constant term.
        """
        if lowerTriangle and upperTriangle:
            lowerTriangle = False
            upperTriangle = False

        rows = []
        numRows = len(self)
        m = self.size[0]

        for row in range(numRows):
            i, j = row % m, row // m

            if lowerTriangle and i < j:
                rows.append(None)
            elif upperTriangle and j < i:
                rows.append(None)
            else:
                rows.append([[], [], 0.0])

        for var, coef in self._coefs.items():
            V, I, J, _ = sparse_quadruple(coef)

            for localCoef, localConIndex, localVarIndex in zip(V, I, J):
                row = rows[localConIndex]

                if not row:
                    continue

                # TODO: Use a single parameter for both types.
                if indexFunction:
                    row[0].append(indexFunction(var, localVarIndex))
                else:
                    row[0].append(varOffsetMap[var] + localVarIndex)

                row[1].append(localCoef)

        for localConIndex in range(numRows):
            row = rows[localConIndex]

            if not row:
                continue

            row[2] = self._const[localConIndex]

        return [row for row in rows if row]

    # --------------------------------------------------------------------------
    # Backwards compatibility methods.
    # --------------------------------------------------------------------------

    @classmethod
    @deprecated("2.0", useInstead="from_constant")
    def fromScalar(cls, scalar):
        """Create a :class:`ComplexAffineExpression` from a numeric scalar."""
        return cls.from_constant(scalar, (1, 1))

    @classmethod
    @deprecated("2.0", useInstead="from_constant")
    def fromMatrix(cls, matrix, size=None):
        """Create a :class:`ComplexAffineExpression` from a numeric matrix."""
        return cls.from_constant(matrix, size)

    @deprecated("2.0", useInstead="object.__xor__")
    def hadamard(self, fact):
        """Denote the elementwise (or Hadamard) product."""
        return self.__xor__(fact)

    @deprecated("2.0", useInstead="constant")
    def isconstant(self):
        """Whether the expression involves no variables."""
        return not self._coefs

    @deprecated("2.0", useInstead="equals")
    def same_as(self, other):
        """Check mathematical equality with another affine expression."""
        return self.equals(other)

    @deprecated("2.0", useInstead="T")
    def transpose(self):
        """Return the matrix transpose."""
        return self.T

    @cached_property
    @deprecated("2.0", useInstead="partial_transpose", decoratorLevel=1)
    def Tx(self):
        """Auto-detect few subsystems of same shape and transpose the last."""
        m, n = self._shape
        dims = None

        for k in range(2, int(math.log(min(m, n), 2)) + 1):
            p, q = int(round(m**(1.0/k))), int(round(n**(1.0/k)))
            if m == p**k and n == q**k:
                dims = ((p, q),)*k
                break

        if dims:
            return self.partial_transpose(subsystems=-1, dimensions=dims)
        else:
            raise RuntimeError("Failed to auto-detect subsystem dimensions for "
                "partial transposition: Only supported for {} matrices, {}."
                .format(glyphs.shape(
                    (glyphs.power("m", "k"), glyphs.power("n", "k"))),
                    glyphs.ge("k", 2)))

    @deprecated("2.0", useInstead="conj")
    def conjugate(self):
        """Return the complex conjugate."""
        return self.conj

    @deprecated("2.0", useInstead="H")
    def Htranspose(self):
        """Return the conjugate (or Hermitian) transpose."""
        return self.H

    @deprecated("2.0", reason="PICOS expressions are now immutable.")
    def copy(self):
        """Return a deep copy of the expression."""
        from copy import copy as cp
        return self._basetype(
            cp(self._symbStr),
            self._shape,
            {var: cp(coef) for var, coef in self._coefs.items()},
            cp(self._const))

    @deprecated("2.0", reason="PICOS expressions are now immutable.")
    def soft_copy(self):
        """Return a shallow copy of the expression."""
        return self._basetype(
            self._symbStr, self._shape, self._coefs, self._const)


class AffineExpression(ComplexAffineExpression):
    """A multidimensional real affine expression."""

    # --------------------------------------------------------------------------
    # Method overridings.
    # --------------------------------------------------------------------------

    @classmethod
    def _get_basetype(cls):
        return AffineExpression

    @classmethod
    def _get_typecode(cls):
        return "d"

    @classmethod
    def _get_type_string_base(cls):
        return "Real {}"

    def _get_refined(self):
        return self

    @convert_operands(sameShape=True, allowNone=True)
    def _set_value(self, value):
        if value is None:
            for var in self._coefs:
                var.value = None
            return

        if not isinstance(value, AffineExpression) or not value.constant:
            raise TypeError("Cannot set the value of {} to {}: Not real or not "
                "a constant.".format(repr(self), repr(value)))

        if self.constant:
            raise TypeError("Cannot set the value on a constant expression.")

        y = cvx2np(value._const)

        A = []
        for var, coef in self._coefs.items():
            A.append(cvx2np(coef))
        assert A

        A = numpy.hstack(A)
        b = y - cvx2np(self._const)

        try:
            solution, residual, _, _ = numpy.linalg.lstsq(A, b, rcond=None)
        except numpy.linalg.LinAlgError as error:
            raise RuntimeError("Setting a value on {} failed: {}."
                .format(self.string, error))

        if not numpy.allclose(residual, 0):
            raise ValueError("Setting a value on {} failed: No exact solution "
                "to the associated linear system found.".format(self.string))

        offset = 0
        for var in self._coefs:
            var.internal_value = solution[offset:offset+var.dim]
            offset += var.dim

    @property
    def isreal(self):
        """Always true for :class:`AffineExpression` instances."""  # noqa
        return True

    @property
    def real(self):
        """The :class:`AffineExpression` as is."""  # noqa
        return self

    @cached_property
    def imag(self):
        """A zero of same shape as the :class:`AffineExpression`."""  # noqa
        return self._basetype.zero(self._shape)

    @property
    def conj(self):
        """The :class:`AffineExpression` as is."""  # noqa
        return self

    @property
    def H(self):
        """The regular transpose of the :class:`AffineExpression`."""  # noqa
        return self.T

    # --------------------------------------------------------------------------
    # Additional methods for real affine expressions only.
    # --------------------------------------------------------------------------

    @cached_property
    def exp(self):
        """The exponential function applied to the expression."""  # noqa
        from . import SumExponentials
        return SumExponentials(self)

    @cached_property
    def log(self):
        """The Logarithm of the expression."""  # noqa
        from . import Logarithm
        return Logarithm(self)

    # --------------------------------------------------------------------------
    # Constraint-creating operators, and _predict.
    # --------------------------------------------------------------------------

    @classmethod
    def _predict(cls, subtype, relation, other):
        assert isinstance(subtype, cls.Subtype)

        from .set import Set

        if relation in (operator.__eq__, operator.__le__, operator.__ge__):
            if issubclass(other.clstype, AffineExpression):
                return AffineConstraint.make_type(
                    dim=subtype.dim, eq=(relation is operator.__eq__))
        elif relation == operator.__lshift__:
            if issubclass(other.clstype, AffineExpression):
                return LMIConstraint.make_type(int(subtype.dim**0.5))
            elif issubclass(other.clstype, ComplexAffineExpression):
                return ComplexLMIConstraint.make_type(int(subtype.dim**0.5))
            elif issubclass(other.clstype, Set):
                return other >> ExpressionType(cls, subtype)
        elif relation == operator.__rshift__:
            if issubclass(other.clstype, AffineExpression):
                return LMIConstraint.make_type(int(subtype.dim**0.5))
            elif issubclass(other.clstype, ComplexAffineExpression):
                return ComplexLMIConstraint.make_type(int(subtype.dim**0.5))

        return NotImplemented

    @convert_operands(sameShape=True)
    @validate_prediction
    @refine_operands()
    def __le__(self, other):
        if isinstance(other, AffineExpression):
            return AffineConstraint(self, Constraint.LE, other)
        else:
            return NotImplemented

    @convert_operands(sameShape=True)
    @validate_prediction
    @refine_operands()
    def __ge__(self, other):
        if isinstance(other, AffineExpression):
            return AffineConstraint(self, Constraint.GE, other)
        else:
            return NotImplemented

    @convert_operands(sameShape=True)
    @validate_prediction
    @refine_operands()
    def __eq__(self, other):
        if isinstance(other, AffineExpression):
            return AffineConstraint(self, Constraint.EQ, other)
        else:
            return NotImplemented

    # Since we define __eq__, __hash__ is not inherited. Do this manually.
    __hash__ = Expression.__hash__

    @convert_operands(sameShape=True)
    @validate_prediction
    @refine_operands()
    def __lshift__(self, other):
        from .set import Set

        if isinstance(other, AffineExpression):
            return LMIConstraint(self, Constraint.LE, other)
        elif isinstance(other, ComplexAffineExpression):
            return ComplexLMIConstraint(self, Constraint.LE, other)
        elif isinstance(other, Set):
            # NOTE: We need to swap explicitly because Python does not consider
            #       A << B the same as B >> A.
            return other.__rshift__(self)
        else:
            return NotImplemented

    @convert_operands(sameShape=True)
    @validate_prediction
    @refine_operands()
    def __rshift__(self, other):
        if isinstance(other, AffineExpression):
            return LMIConstraint(self, Constraint.GE, other)
        elif isinstance(other, ComplexAffineExpression):
            return ComplexLMIConstraint(self, Constraint.GE, other)
        else:
            return NotImplemented


def Constant(name_or_value, value=None, shape=None):
    """Create a constant PICOS expression.

    Loads the given numeric value as a constant
    :class:`~picos.expressions.ComplexAffineExpression` or
    :class:`~picos.expressions.AffineExpression`, depending on the value.
    Optionally, the value is broadcasted or reshaped according to the shape
    argument.

    :param str name_or_value: Symbolic string description of the constant. If
        :obj:`None` or the empty string, a string will be generated. If this is
        the only positional parameter (i.e.``value`` is not given), then this
        position is used as the value argument instead!
    :param value: The numeric constant to load.

    See :func:`~.data.load_data` for supported data formats and broadcasting and
    reshaping rules.

    :Example:

    >>> from picos import Constant
    >>> Constant(1)
    <1×1 Real Constant: 1>
    >>> Constant(1, shape=(2, 2))
    <2×2 Real Constant: [1]>
    >>> Constant("one", 1)
    <1×1 Real Constant: one>
    >>> Constant("J", 1, (2, 2))
    <2×2 Real Constant: J>
    """
    if value is None:
        value = name_or_value
        name  = None
    else:
        name  = name_or_value

    value, valStr = load_data(value, shape)

    if value.typecode == "z":
        cls = ComplexAffineExpression
    else:
        cls = AffineExpression

    return cls(name if name else valStr, value.size, {}, value)


# --------------------------------------
__all__ = api_end(_API_START, globals())
