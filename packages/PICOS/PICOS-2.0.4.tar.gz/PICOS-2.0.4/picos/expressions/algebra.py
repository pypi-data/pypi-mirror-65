# coding: utf-8

# ------------------------------------------------------------------------------
# Copyright (C) 2019 Maximilian Stahlberg
# Based on parts of the tools module by Guillaume Sagnol.
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

"""Implements functions that create or modify algebraic expressions."""

import functools

from .. import glyphs
from ..apidoc import api_end, api_start
from ..compat import builtins
from ..formatting import parameterized_string
from ..legacy import deprecated, throw_deprecation_warning
from .data import convert_and_refine_arguments
from .exp_affine import ComplexAffineExpression, Constant
from .exp_detrootn import DetRootN
from .exp_entropy import NegativeEntropy
from .exp_geomean import GeometricMean
from .exp_logsumexp import LogSumExp
from .exp_norm import Norm
from .exp_powtrace import PowerTrace
from .exp_sumexp import SumExponentials
from .exp_sumxtr import SumExtremes
from .expression import Expression
from .set_ball import Ball
from .set_expcone import ExponentialCone
from .set_rsoc import RotatedSecondOrderCone
from .set_simplex import Simplex
from .set_soc import SecondOrderCone

_API_START = api_start(globals())
# -------------------------------


# ------------------------------------------------------------------------------
# Algebraic functions with a logic of their own.
# ------------------------------------------------------------------------------


def sum(lst, it=None, indices=None):
    """Sum PICOS expressions and give the result a meaningful description.

    This is a replacement for Python's :func:`sum` that produces sensible string
    representations when summing PICOS expressions.

    :param lst: A list of
        :class:`~picos.expressions.ComplexAffineExpression`, or a
        single affine expression whose elements shall be summed.
    :type lst: list or tuple or
        ~picos.expressions.ComplexAffineExpression

    :param it: DEPRECATED
    :param indices: DEPRECATED

    :Example:

    >>> import builtins
    >>> import picos
    >>> x = picos.RealVariable("x", 5)
    >>> e = [x[i]*x[i+1] for i in range(len(x) - 1)]
    >>> builtins.sum(e)
    <Quadratic Expression: x[0]·x[1] + x[1]·x[2] + x[2]·x[3] + x[3]·x[4]>
    >>> picos.sum(e)
    <Quadratic Expression: ∑(x[i]·x[i+1] : i ∈ [0…3])>
    >>> picos.sum(x)  # The same as (x|1).
    <1×1 Real Linear Expression: ∑(x)>
    """
    if it is not None or indices is not None:
        # Deprecated as of 2.0.
        throw_deprecation_warning("Arguments 'it' and 'indices' to picos.sum "
            "are deprecated and ignored.")

    if isinstance(lst, Expression):
        if isinstance(lst, ComplexAffineExpression):
            return (lst | 1.0)
        else:
            raise TypeError(
                "PICOS doesn't know how to sum over a single {}."
                .format(type(lst).__name__))

    if any(not isinstance(expression, Expression) for expression in lst):
        return builtins.sum(lst)

    if len(lst) == 0:
        return Constant(0)
    elif len(lst) == 1:
        return lst[0]
    elif len(lst) == 2:
        return lst[0] + lst[1]

    theSum = lst[0]
    for expression in lst[1:]:
        theSum += expression

    try:
        template, data = parameterized_string([exp.string for exp in lst])
    except ValueError:
        theSum._symbStr = glyphs.sum(
            glyphs.fromto(lst[0].string + ", ", ", " + lst[-1].string))
    else:
        theSum._symbStr = glyphs.sum(glyphs.sep(template, data))

    return theSum


# ------------------------------------------------------------------------------
# Functions that call expression methods.
# ------------------------------------------------------------------------------


def _error_on_none(func):
    """Raise a :exc:`TypeError` if the function returns :obj:`None`."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if result is None:
            raise TypeError("PICOS does not have a representation for {}({})."
                .format(func.__qualname__ if hasattr(func, "__qualname__") else
                func.__name__, ", ".join([type(x).__name__ for x in args] +
                ["{}={}".format(k, type(x).__name__) for k, x in kwargs.items()]
                )))

        return result
    return wrapper


@_error_on_none
@convert_and_refine_arguments("x")
def exp(x):
    """Denote the exponential."""
    if hasattr(x, "exp"):
        return x.exp


@_error_on_none
@convert_and_refine_arguments("x")
def log(x):
    """Denote the natural logarithm."""
    if hasattr(x, "log"):
        return x.log


@_error_on_none
@convert_and_refine_arguments("x", "y")
def kron(x, y):
    """Denote the kronecker product.

    Note that with Python 3, you can just write ``x @ y``.
    """
    if hasattr(x, "kron"):
        return x.kron(y)


@_error_on_none
@convert_and_refine_arguments("x")
def diag(x, n=1):
    r"""Form a diagonal matrix from the column-major vectorization of :math:`x`.

    If :math:`n \neq 1`, then the vectorization is repeated :math:`n` times.
    """
    if hasattr(x, "diag") and n == 1:
        return x.diag
    elif hasattr(x, "dupdiag"):
        return x.dupdiag(n)


@_error_on_none
@convert_and_refine_arguments("x")
def maindiag(x):
    """Extract the diagonal of :math:`x` as a column vector."""
    if hasattr(x, "maindiag"):
        return x.maindiag


@_error_on_none
@convert_and_refine_arguments("x")
def trace(x):
    """Denote the trace of a square matrix."""
    if hasattr(x, "tr"):
        return x.tr


@_error_on_none
@convert_and_refine_arguments("x")
def partial_trace(x, subsystems=0, dimensions=2, k=None, dim=None):
    """See :meth:`.expressions.ComplexAffineExpression.partial_trace`.

    The parameters `k` and `dim` are for backwards compatibility.
    """
    if k is not None:
        throw_deprecation_warning("Argument 'k' to partial_trace is "
            "deprecated: Use 'subsystems' instead.", decoratorLevel=2)
        subsystems = k

    if dim is not None:
        throw_deprecation_warning("Argument 'dim' to partial_trace is "
            "deprecated: Use 'dimensions' instead.", decoratorLevel=2)
        dimensions = dim

    if isinstance(x, ComplexAffineExpression):
        return x.partial_trace(subsystems, dimensions)


@_error_on_none
@convert_and_refine_arguments("x")
def partial_transpose(x, subsystems=0, dimensions=2, k=None, dim=None):
    """See :meth:`.expressions.ComplexAffineExpression.partial_transpose`.

    The parameters `k` and `dim` are for backwards compatibility.
    """
    if k is not None:
        throw_deprecation_warning("Argument 'k' to partial_transpose is "
            "deprecated: Use 'subsystems' instead.", decoratorLevel=2)
        subsystems = k

    if dim is not None:
        throw_deprecation_warning("Argument 'dim' to partial_transpose is "
            "deprecated: Use 'dimensions' instead.", decoratorLevel=2)
        dimensions = dim

    if isinstance(x, ComplexAffineExpression):
        return x.partial_transpose(subsystems, dimensions)


# ------------------------------------------------------------------------------
# Alias functions for expression classes meant to be instanciated by the user.
# ------------------------------------------------------------------------------


def _shorthand(cls):
    def shorthand(*args, **kwargs):
        return cls(*args, **kwargs)

    shorthand.__doc__ = "Shorthand for :class:`~picos.{}`.".format(cls.__name__)

    return shorthand


expcone = _shorthand(ExponentialCone)
geomean = _shorthand(GeometricMean)
kldiv   = _shorthand(NegativeEntropy)
lse     = _shorthand(LogSumExp)
rsoc    = _shorthand(RotatedSecondOrderCone)
soc     = _shorthand(SecondOrderCone)
sumexp  = _shorthand(SumExponentials)


def max(x):
    """Wrapper for :class:`~picos.SumExtremes`.

    Sets ``k = 1``, ``largest = True`` and ``eigenvalues = False``.

    :Example:

    >>> from picos import RealVariable, max
    >>> x = RealVariable("x", 5)
    >>> max(x)
    <Largest Element: max(x)>
    >>> max(x) <= 2  # The same as x <= 2.
    <Largest Element Constraint: max(x) ≤ 2>
    """
    return SumExtremes(x, 1, largest=True, eigenvalues=False)


def min(x):
    """Wrapper for :class:`~picos.SumExtremes`.

    Sets ``k = 1``, ``largest = False`` and ``eigenvalues = False``.

    :Example:

    >>> from picos import RealVariable, min
    >>> x = RealVariable("x", 5)
    >>> min(x)
    <Smallest Element: min(x)>
    >>> min(x) >= 2  # The same as x >= 2.
    <Smallest Element Constraint: min(x) ≥ 2>
    """
    return SumExtremes(x, 1, largest=False, eigenvalues=False)


def sum_k_largest(x, k):
    """Wrapper for :class:`~picos.SumExtremes`.

    Sets ``largest = True`` and ``eigenvalues = False``.

    :Example:

    >>> from picos import RealVariable, sum_k_largest
    >>> x = RealVariable("x", 5)
    >>> sum_k_largest(x, 2)
    <Sum of Largest Elements: sum_2_largest(x)>
    >>> sum_k_largest(x, 2) <= 2
    <Sum of Largest Elements Constraint: sum_2_largest(x) ≤ 2>
    """
    return SumExtremes(x, k, largest=True, eigenvalues=False)


def sum_k_smallest(x, k):
    """Wrapper for :class:`~picos.SumExtremes`.

    Sets ``largest = False`` and ``eigenvalues = False``.

    :Example:

    >>> from picos import RealVariable, sum_k_smallest
    >>> x = RealVariable("x", 5)
    >>> sum_k_smallest(x, 2)
    <Sum of Smallest Elements: sum_2_smallest(x)>
    >>> sum_k_smallest(x, 2) >= 2
    <Sum of Smallest Elements Constraint: sum_2_smallest(x) ≥ 2>
    """
    return SumExtremes(x, k, largest=False, eigenvalues=False)


def lambda_max(x):
    """Wrapper for :class:`~picos.SumExtremes`.

    Sets ``k = 1``, ``largest = True`` and ``eigenvalues = True``.

    :Example:

    >>> from picos import SymmetricVariable, lambda_max
    >>> X = SymmetricVariable("X", 5)
    >>> lambda_max(X)
    <Largest Eigenvalue: λ_max(X)>
    >>> lambda_max(X) <= 2
    <Largest Eigenvalue Constraint: λ_max(X) ≤ 2>
    """
    return SumExtremes(x, 1, largest=True, eigenvalues=True)


def lambda_min(x):
    """Wrapper for :class:`~picos.SumExtremes`.

    Sets ``k = 1``, ``largest = False`` and ``eigenvalues = True``.

    :Example:

    >>> from picos import SymmetricVariable, lambda_min
    >>> X = SymmetricVariable("X", 5)
    >>> lambda_min(X)
    <Smallest Eigenvalue: λ_min(X)>
    >>> lambda_min(X) >= 2
    <Smallest Eigenvalue Constraint: λ_min(X) ≥ 2>
    """
    return SumExtremes(x, 1, largest=False, eigenvalues=True)


def sum_k_largest_lambda(x, k):
    """Wrapper for :class:`~picos.SumExtremes`.

    Sets ``largest = True`` and ``eigenvalues = True``.

    :Example:

    >>> from picos import SymmetricVariable, sum_k_largest_lambda
    >>> X = SymmetricVariable("X", 5)
    >>> sum_k_largest_lambda(X, 2)
    <Sum of Largest Eigenvalues: sum_2_largest_λ(X)>
    >>> sum_k_largest_lambda(X, 2) <= 2
    <Sum of Largest Eigenvalues Constraint: sum_2_largest_λ(X) ≤ 2>
    """
    return SumExtremes(x, k, largest=True, eigenvalues=True)


def sum_k_smallest_lambda(x, k):
    """Wrapper for :class:`~picos.SumExtremes`.

    Sets ``largest = False`` and ``eigenvalues = True``.

    :Example:

    >>> from picos import SymmetricVariable, sum_k_smallest_lambda
    >>> X = SymmetricVariable("X", 5)
    >>> sum_k_smallest_lambda(X, 2)
    <Sum of Smallest Eigenvalues: sum_2_smallest_λ(X)>
    >>> sum_k_smallest_lambda(X, 2) >= 2
    <Sum of Smallest Eigenvalues Constraint: sum_2_smallest_λ(X) ≥ 2>
    """
    return SumExtremes(x, k, largest=False, eigenvalues=True)


# ------------------------------------------------------------------------------
# Legacy algebraic functions for backwards compatibility.
# ------------------------------------------------------------------------------


def _deprecated_shorthand(cls, new_shorthand=None):
    shRef = "~picos.{}".format(cls.__name__)
    uiRef = "~picos.{}".format(new_shorthand) if new_shorthand else shRef

    # FIXME: This doesn't show the name of the deprecated shorthand function.
    @deprecated("2.0", useInstead=uiRef)
    def shorthand(*args, **kwargs):
        """|PLACEHOLDER|"""  # noqa
        return cls(*args, **kwargs)

    shorthand.__doc__ = shorthand.__doc__.replace("|PLACEHOLDER|",
        "Legacy shorthand for :class:`{}`.".format(shRef))

    return shorthand


ball             = _deprecated_shorthand(Ball)
detrootn         = _deprecated_shorthand(DetRootN)
kullback_leibler = _deprecated_shorthand(NegativeEntropy, "kldiv")
logsumexp        = _deprecated_shorthand(LogSumExp, "lse")
norm             = _deprecated_shorthand(Norm)


@deprecated("2.0", useInstead="~picos.PowerTrace")
def tracepow(exp, num=1, denom=1, coef=None):
    """Legacy shorthand for :class:`~picos.PowerTrace`."""
    return PowerTrace(exp, num / denom, coef)


@deprecated("2.0", useInstead="~picos.Constant")
def new_param(name, value):
    """Create a constant or a list or dict or tuple thereof."""
    if isinstance(value, list):
        # Handle a vector.
        try:
            for x in value:
                complex(x)
        except Exception:
            pass
        else:
            return Constant(name, value)

        # Handle a matrix.
        if all(isinstance(x, list) for x in value) \
        and all(len(x) == len(value[0]) for x in value):
            try:
                for x in value:
                    for y in x:
                        complex(y)
            except Exception:
                pass
            else:
                return Constant(name, value)

        # Return a list of constants.
        return [Constant(glyphs.slice(name, i), x) for i, x in enumerate(value)]
    elif isinstance(value, tuple):
        # Return a list of constants.
        # NOTE: This is very inconsistent, but legacy behavior.
        return [Constant(glyphs.slice(name, i), x) for i, x in enumerate(value)]
    elif isinstance(value, dict):
        return {k: Constant(glyphs.slice(name, k), x) for k, x in value.items()}
    else:
        return Constant(name, value)


@deprecated("2.0", useInstead="~picos.FlowConstraint")
def flow_Constraint(*args, **kwargs):
    """Legacy shorthand for :class:`~picos.FlowConstraint`."""
    from ..constraints.con_flow import FlowConstraint
    return FlowConstraint(*args, **kwargs)


@deprecated("2.0", useInstead="~picos.maindiag")
def diag_vect(x):
    """Extract the diagonal of :math:`x` as a column vector."""
    return maindiag(x)


@deprecated("2.0", useInstead="~picos.Simplex")
def simplex(gamma):
    r"""Create a standard simplex of radius :math:`\gamma`."""
    return Simplex(gamma, truncated=False, symmetrized=False)


@deprecated("2.0", useInstead="~picos.Simplex")
def truncated_simplex(gamma, sym=False):
    r"""Create a truncated simplex of radius :math:`\gamma`."""
    return Simplex(gamma, truncated=True, symmetrized=sym)


# --------------------------------------
__all__ = api_end(_API_START, globals())
