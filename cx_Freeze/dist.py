"""The classes and functions with which cx_Freeze extends setuptools."""

from setuptools import Distribution as _Distribution

__all__ = ["Distribution", "DistributionMetadata"]


class DistributionMetadata:
    """Dummy class to hold the distribution meta-data: name, version,
    author, and so forth."""


class Distribution(_Distribution):
    """Distribution with support for executables."""

    def __init__(self, attrs):
        self.executables = []
        super().__init__(attrs)
        self.metadata = self._patch_metadata()

    def _patch_metadata(self) -> DistributionMetadata:
        old_metadata = self.metadata
        new_metadata = DistributionMetadata()
        for var in dir(old_metadata):
            if not hasattr(new_metadata, var):
                setattr(new_metadata, var, getattr(old_metadata, var))
        self.distutils_metadata = old_metadata
        return new_metadata

    def has_executables(self):
        """Predicate for build_exe command."""
        return self.executables and len(self.executables) > 0
