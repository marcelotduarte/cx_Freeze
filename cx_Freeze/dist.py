"""The classes and functions with which cx_Freeze extends setuptools."""

from distutils.dist import DistributionMetadata  # pylint: disable=W0402

from setuptools import Distribution as _Distribution

__all__ = ["Distribution", "DistributionMetadata"]


class Distribution(_Distribution):
    """Distribution with support for executables."""

    def __init__(self, attrs):
        self.executables = []
        super().__init__(attrs)

    def has_executables(self):
        """Predicate for build_exe command."""
        return self.executables and len(self.executables) > 0
