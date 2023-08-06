# coding: utf-8

# ------------------------------------------------------------------------------
# Copyright (C) 2019-2020 Maximilian Stahlberg
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

"""Optimization problem description classes.

This module implements a footprint of a single problem, storing number and types
of expressions and constraints, and the specification of a problem class.
"""

import math
from inspect import isclass
from itertools import chain

from .. import constraints, expressions, glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_property
from ..containers import RecordTree
from ..expressions import variables
# from .options import OPTION_OBJS, Options  # Circular import.

_API_START = api_start(globals())
# -------------------------------


# Constants used by both Footprint and Specification.
_OBJS = tuple(exp for exp in expressions.__dict__.values() if isclass(exp)
    and issubclass(exp, expressions.Expression)
    and exp != expressions.Expression)  # ALl proper Expression subclasses.
_DIRS = ("find", "min", "max")
_VARS = tuple(var for var in expressions.__dict__.values() if isclass(var)
    and issubclass(var, expressions.BaseVariable)
    and var != expressions.BaseVariable)  # ALl proper BaseVariable subclasses.
_CONS = tuple(con for con in constraints.__dict__.values() if isclass(con)
    and issubclass(con, constraints.Constraint)
    and con != constraints.Constraint)  # All proper Constraint subclasses.
# _OPTS = tuple(option.name for option in OPTION_OBJS)  # All option names.


class Footprint(RecordTree):
    """Statistics on an optimization problem.

    Subtree comparison (`<<`) can be used to check if a specific problem
    represented by a :class:`Footprint` instance is contained in a problem class
    represented by a :class:`Specification` instance.
    """

    _ADD_VALUES = [("var",), ("con",)]

    def __init__(self, recordsOrDict):
        """Construct a :class:`Footprint` from raw data.

        See :class:`picos.containers.RecordTree.__init__`. The ``addValues``
        argument is fixed; only variable and constraint paths are added.
        """
        super(Footprint, self).__init__(recordsOrDict, self._ADD_VALUES)

        # Sanity check records.
        for path, value in self.items:
            pathLen  = len(path)
            category = path[0] if pathLen > 0 else None
            suptype  = path[1] if pathLen > 1 else None
            subtype  = path[2] if pathLen > 2 else None

            if category == "dir":
                if pathLen == 2 and suptype in _DIRS and value is None:
                    continue
            elif category == "obj":
                if pathLen == 3 and suptype in _OBJS \
                and isinstance(subtype, suptype.Subtype) and value is None:
                    continue
            elif category == "var":
                if pathLen == 3 and suptype in _VARS \
                and isinstance(subtype, suptype.VarSubtype) \
                and isinstance(value, int):
                    continue
            elif category == "con":
                if pathLen == 3 and suptype in _CONS \
                and isinstance(subtype, suptype.Subtype) \
                and isinstance(value, int):
                    continue
            elif category == "opt":
                # if pathLen == 2 and suptype in _OPTS:
                if pathLen == 2 and isinstance(suptype, str):
                    continue

            raise ValueError("Invalid problem footprint record: {} = {}."
                .format(path, value))

        # Sanity check for inconsistent duplicates or missing fields.
        if len(self["dir"]) != 1:
            raise TypeError("Not exactly one optimization direction defined for"
                " a problem footprint (but {}).".format(len(self["dir"])))
        elif len(self["obj"]) != 1:
            raise TypeError("Not exactly one objective function defined for a "
                "problem footprint (but {}).".format(len(self["obj"])))

    def updated(self, recordsOrDict):
        """Override :class:`~picos.containers.RecordTree.updated`.

        This method, just like :meth:`__init__`, does not take the additional
        ``addValues`` argument.
        """
        return self.__class__(
            chain(self.records, self._record_iterator(recordsOrDict)))

    @property
    def direction(self):
        """Objective function optimization direction."""
        return next(self["dir"].paths)[0]

    @property
    def objective(self):
        """Detailed type of the objective function."""
        clstype, subtype = next(self["obj"].paths)
        return expressions.ExpressionType(clstype, subtype)

    @cached_property
    def variables(self):
        """A dictionary mapping detailed variable types to their quantity."""
        return {variables.VariableType(*ts): n
            for ts, n in self.get("var").items}

    @cached_property
    def constraints(self):
        """A dictionary mapping detailed constraint types to their quantity."""
        return {constraints.ConstraintType(*ts): n
            for ts, n in self.get("con").items}

    @cached_property
    def nondefault_options(self):
        """A dictionary mapping option names to their nondefault values.

        .. warning::

            This property is cached for performance reasons, do not modify any
            mutable option value (make a deep copy instead)!
        """
        return {path[0]: value for path, value in self.get("opt").items}

    @cached_property
    def options(self):
        """An :class:`~picos.Options` object.

        .. warning::

            This property is cached for performance reasons, do not modify the
            returned object (make a :meth:`~picos.Options.copy` instead)!
        """
        from .options import Options
        return Options(**self.nondefault_options)

    @cached_property
    def integer(self):
        """Whether an integral variable type is present."""
        return any(("var", vtype) in self for vtype in (
            expressions.BinaryVariable, expressions.IntegerVariable))

    @property
    def continuous(self):
        """Whether no integral variable type is present."""
        return not self.integer

    @cached_property
    def nonconvex_quadratic_objective(self):
        """Whether the problem has a nonconvex quadratic objective."""
        if self.objective.clstype is expressions.QuadraticExpression:
            direction = self.direction
            subtype   = self.objective.subtype

            assert direction in ("min", "max")

            if   direction == "min" and not subtype.convex:
                return True
            elif direction == "max" and not subtype.concave:
                return True

        return False

    def __str__(self):
        dirStr = self.direction.capitalize()
        objStr = str(self.objective)
        varStr = ", ".join(sorted("{} {}".format(n, v)
            for v, n in self.variables.items()))
        conStr = ", ".join(sorted("{} {}".format(n, c)
            for c, n in self.constraints.items()))
        optStr = ", ".join(sorted("{}={}".format(n, v)
            for n, v in self.nondefault_options.items()))

        return "{} {} subject to {} using {} and {}.".format(
            dirStr, objStr,
            conStr if conStr else "no constraints",
            varStr if varStr else "no variables",
            optStr if optStr else "default options")

    def __repr__(self):
        return glyphs.repr2("Footprint", str(self))

    @classmethod
    def from_problem(cls, problem):
        """Create a footprint from a problem instance."""
        return cls(chain(
            (("dir", problem.objective.direction, None),
             ("obj", problem.objective.normalized.function.type, None)),
            (("var", v.var_type, 1) for v in problem.variables.values()),
            (("con", con.type, 1) for con in problem.constraints.values()),
            (("opt", n, v) for n, v in problem.options.nondefaults.items())))

    @classmethod
    def from_types(cls, obj_dir, obj_func, vars=[], cons=[], nd_opts={}):
        """Create a footprint from collections of detailed types.

        :param str obj_dir:
            Objective direction.

        :param obj_func:
            Detailed objective function type.

        :parm list(tuple) vars:
            A list of pairs of detailed variable type and occurence count.

        :parm list(tuple) cons:
            A list of pairs of detailed constraint type and occurence count.

        :param list(str) nd_opts:
            A dictionary mapping option names to nondefault values.
        """
        return cls(chain(
            (("dir", obj_dir, None),
             ("obj", obj_func, None)),
            (("var", vn[0], vn[1]) for vn in vars),
            (("con", cn[0], cn[1]) for cn in cons),
            (("opt", name, value) for name, value in nd_opts.items())))

    def with_extra_options(self, **extra_options):
        """Return a copy with additional solution search options applied."""
        # Determine the new option set.
        options = self.options.self_or_updated(**extra_options)

        # Delete old nondefault options and set new ones.
        return self.updated(chain(
            (("opt", self.NONE),),
            (("opt", n, v) for n, v in options.nondefaults.items())
        ))

    @cached_property
    def size(self):
        """Return the estimated size of the (dense) scalar constraint matrix."""
        num_vars = 0
        num_cons = 0

        for dim in self.variables.values():
            num_vars += dim

        for con, num in self.constraints.items():
            num_cons += con.clstype._cost(con.subtype)*num

        return max(1, num_vars)*max(1, num_cons)

    @property
    def cost(self):
        """A very rough measure on how expensive solving such a problem is.

        This is logarithmic in the estimated size of the constraint matrix.
        """
        return math.log(self.size, 10)


class Specification(RecordTree):
    """Representation of a mathematical class of optimization problems.

    Subtree comparison (`<<`) can be used to check if a specific problem
    represented by a :class:`Footprint` instance is contained in a problem class
    represented by a :class:`Specification` instance.
    """

    def __init__(self, recordsOrDict):
        """Construct a :class:`Specification` from raw data.

        See :class:`picos.containers.RecordTree.__init__`.
        """
        super(Specification, self).__init__(recordsOrDict)

        # Sanity check records (up to expression and constraint subtypes).
        for path, value in self.items:
            pathLen  = len(path)
            category = path[0] if pathLen > 0 else None
            suptype  = path[1] if pathLen > 1 else None
            subtype  = path[2] if pathLen > 2 else None

            if category and pathLen == 1 and value is self.ALL:
                continue

            if category == "dir":
                if pathLen == 2 and suptype in _DIRS and value is None:
                    continue
            elif category == "obj":
                if pathLen == 3 and suptype in _OBJS \
                and isinstance(subtype, suptype.Subtype) and value is None:
                    continue
                elif pathLen == 2 and suptype in _OBJS and value is self.ALL:
                    continue
            elif category == "var":
                if pathLen == 3 and suptype in _VARS \
                and isinstance(subtype, suptype.VarSubtype) and value is None:
                    continue
                elif pathLen == 2 and suptype in _VARS and value is self.ALL:
                    continue
            elif category == "con":
                if pathLen == 3 and suptype in _CONS \
                and isinstance(subtype, suptype.Subtype) and value is None:
                    continue
                elif pathLen == 2 and suptype in _CONS and value is self.ALL:
                    continue
            elif category == "opt":
                # if pathLen == 3 and suptype in _OPTS and value is None:
                if pathLen == 3 and isinstance(suptype, str) and value is None:
                    continue
                # if pathLen == 2 and suptype in _OPTS and value is self.ALL:
                if pathLen == 2 and isinstance(suptype, str) \
                and value is self.ALL:
                    continue

            raise ValueError("Invalid problem specification record: {} = {}."
                .format(path, value))

    @staticmethod
    def _paths_str(paths):
        return ", ".join(":".join(p.__name__ if isclass(p) else str(p) for p in
            path) for path in paths)

    def __str__(self):
        dirs, objs, vars, cons, opts = \
            (self.get(x) for x in ("dir", "obj", "var", "con", "opt"))

        if not dirs:
            dirStr = "Load"
        elif dirs is self.ALL:
            dirStr = "Optimize"
        else:
            dirStr = self._paths_str(dirs.paths).capitalize()

        if not objs:
            objStr = "no objective"
        elif objs is self.ALL:
            objStr = "any objective"
        else:
            objStr = self._paths_str(objs.paths)

        if not vars:
            varStr = "no variables"
        elif vars is self.ALL:
            varStr = "any variables"
        else:
            varStr = self._paths_str(vars.paths)

        if not cons:
            conStr = "no constraint"
        elif cons is self.ALL:
            conStr = "any constraint"
        else:
            conStr = self._paths_str(cons.paths)

        if not opts:
            optStr = "default options"
        elif opts is self.ALL:
            optStr = "any options"
        else:
            optStr = "nondefault values for " + self._paths_str(opts.paths)

        return "{} {} subject to {} using {} and {}.".format(
            dirStr, objStr, conStr, varStr, optStr)

    def __repr__(self):
        return glyphs.repr2("Specification", str(self))

    @classmethod
    def compile(cls, directions=(), objectives=(), variables=(),
            constraints=(), nondefault_options=RecordTree.ALL):
        """Create a specification from the given features."""
        return cls(chain(
            (("dir", cls.ALL),) if directions is cls.ALL else
            (("dir", dir, None) for dir in directions),

            (("obj", cls.ALL),) if objectives is cls.ALL else
            (("obj", obj, cls.ALL) for obj in objectives),

            (("var", cls.ALL),) if variables is cls.ALL else
            (("var", var, cls.ALL) for var in variables),

            (("con", cls.ALL),) if constraints is cls.ALL else
            (("con", con, cls.ALL) for con in constraints),

            (("opt", cls.ALL),) if nondefault_options is cls.ALL else
            (("opt", opt, cls.ALL) for opt in nondefault_options)
        ))


# --------------------------------------
__all__ = api_end(_API_START, globals())
