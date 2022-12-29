"""The classes and functions with which cx_Freeze extends setuptools."""

from __future__ import annotations

from setuptools import Distribution
from setuptools.errors import SetupError

from .executable import Executable

__all__ = ["Distribution", "DistributionMetadata"]


# pylint: disable-next=unused-argument
def validate_executables(dist: Distribution, attr: str, value):
    """Verify that value is a Executable list."""

    try:
        # verify that value is a list or tuple to exclude unordered
        # or single-use iterables
        assert isinstance(value, (list, tuple))
        # verify that elements of value are Executable
        for executable in value:
            assert isinstance(executable, Executable)
    except (TypeError, ValueError, AttributeError, AssertionError) as exc:
        raise SetupError(
            f"{attr!r} must be a list of Executable (got {value!r})"
        ) from exc


def finalize_distribution_options(dist: Distribution) -> None:
    """Use a setuptools extension to customize Distribution options."""

    if getattr(dist, "executables", None) is None:
        return

    # fix package discovery (setuptools >= 61)
    if getattr(dist.metadata, "py_modules", None) is None:
        dist.py_modules = []


DistributionMetadata = type(Distribution().metadata)
"""Dummy class to hold the distribution meta-data: name, version, author,
and so forth."""
