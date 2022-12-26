"""The classes and functions with which cx_Freeze extends setuptools."""

from __future__ import annotations

from setuptools import Distribution as _Distribution

__all__ = ["Distribution", "DistributionMetadata"]


class Distribution(_Distribution):
    """Distribution with support for executables."""

    def __init__(self, attrs):
        self.executables = []
        super().__init__(attrs)
        self._fix_py_modules()

    def _fix_py_modules(self):
        # fix package discovery (setuptools >= 61)
        if not self.executables:
            return
        self.include(
            py_modules=[
                executable.main_script.stem for executable in self.executables
            ]
        )

    def has_executables(self):
        """Predicate for build_exe command."""
        return self.executables and len(self.executables) > 0


DistributionMetadata = type(_Distribution().metadata)
"""Dummy class to hold the distribution meta-data: name, version, author,
and so forth."""
