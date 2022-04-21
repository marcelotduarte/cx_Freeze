"""Internal compatible module."""
import sys

__all__ = ["cached_property", "importlib_metadata"]

if sys.version_info >= (3, 10):
    import importlib.metadata as importlib_metadata
else:
    try:
        import importlib_metadata
    except ImportError:
        import importlib.metadata as importlib_metadata


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
