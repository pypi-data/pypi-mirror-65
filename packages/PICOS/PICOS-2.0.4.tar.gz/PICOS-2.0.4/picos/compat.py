# coding: utf-8

# ------------------------------------------------------------------------------
# Copyright (C) 2019 Maximilian Stahlberg
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

"""Python 2/3 compatibility helpers."""

import sys
from abc import ABCMeta
from abc import abstractmethod as _abstractmethod
from copy import copy

from .apidoc import api_end, api_start

_API_START = api_start(globals())
# -------------------------------


VERSION = sys.version_info  #: The same as :obj:`sys.version_info`.
MAJOR   = VERSION.major  #: Major Python version.
MINOR   = VERSION.minor  #: Minor Python version.

# Import the 'builtins' module for both Pythons.
if MAJOR >= 3:
    import builtins  # noqa
else:
    import __builtin__ as builtins  # noqa

# Import 'MutableSet' for both Pythons.
if MAJOR >= 3:
    from collections.abc import MutableSet  # noqa
else:
    from collections import MutableSet  # noqa

# Allow the long type to be referenced in Python 3.
long = int if MAJOR >= 3 else long  # noqa

# Import abstract base class support for both Pythons.
ABC = ABCMeta("ABC", (object,), {"__slots__": ()})
ABC.__doc__ = "Base class for abstract classes."
abstractmethod = copy(_abstractmethod)
# HACK: Fix abstractmethod's docstring so Sphinx doesn't warn about it.
abstractmethod.__doc__ = "A decorator indicating abstract methods."


# TODO: Implement lru_cache for Python 2.
def _lru_cache(maxsize=128, typed=False):
    def decorator(function):
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper
    return decorator


# Make lru_cache available.
try:
    from functools import lru_cache
except ImportError:
    try:
        from functools32 import lru_cache
    except ImportError:
        try:
            from repoze.lru import lru_cache
        except ImportError:
            lru_cache = _lru_cache


# Import or implement MappingProxyType.
try:
    from types import MappingProxyType
except ImportError:  # Python < 3.3
    from collections import Mapping as _Mapping

    class MappingProxyType(_Mapping):  # noqa
        def __init__(self, mapping):  # noqa
            self._mapping = mapping

        def __getitem__(self, key):
            return self._mapping[key]

        def __iter__(self):
            return iter(self._mapping)

        def __len__(self):
            return len(self._mapping)

        def copy(self):  # noqa
            return self._mapping.copy()


def import_exists(importName):
    """Check if a package or module name is available for import."""
    if MAJOR >= 3:
        if MINOR >= 4:
            import importlib.util
            return importlib.util.find_spec(importName) is not None
        else:
            import importlib
            return importlib.find_loader(importName) is not None
    else:
        import pkgutil
        return pkgutil.find_loader(importName) is not None


def assert_import_exists(importName):
    """Error if the given package or module name is not available for import.

    :raises ModuleNotFoundError or ImportError: If no module with the given name
         is available for import, denpending on the Python version.
    """
    if not import_exists(importName):
        if MAJOR >= 3:
            Error = ModuleNotFoundError
        else:
            Error = ImportError
        raise Error("Python module '{}' not found.".format(importName))


__all__ = api_end(_API_START, globals())
