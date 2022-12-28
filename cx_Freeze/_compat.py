"""Internal compatible module."""

from __future__ import annotations

import sys
import sysconfig

if sys.version_info >= (3, 10):
    import importlib.metadata as importlib_metadata
else:
    from setuptools.extern import importlib_metadata

__all__ = ["cached_property", "importlib_metadata"]
__all__ += ["PLATFORM", "IS_LINUX", "IS_MACOS", "IS_MINGW", "IS_WINDOWS"]

PLATFORM = sysconfig.get_platform()
IS_LINUX = PLATFORM.startswith("linux")
IS_MACOS = PLATFORM.startswith("macos")
IS_MINGW = PLATFORM.startswith("mingw")
IS_WINDOWS = PLATFORM.startswith("win")


try:
    from functools import cached_property
except ImportError:

    class cached_property:  # pylint: disable=invalid-name
        """Transform a method of a class into a property whose value is
        computed once and then cached as a normal attribute for the life of
        the instance."""

        def __init__(self, func):
            self.func = func
            self.__doc__ = func.__doc__

        def __get__(self, instance, owner=None):
            if instance is None:
                return self

            value = instance.__dict__[self.func.__name__] = self.func(instance)
            return value
