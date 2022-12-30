"""The classes and functions with which cx_Freeze extends setuptools."""

from __future__ import annotations

from setuptools import Distribution

__all__ = ["DistributionMetadata"]


def plugin_install(dist: Distribution) -> None:
    """Use a setuptools extension to customize Distribution options."""

    if getattr(dist, "executables", None) is None:
        return

    # fix package discovery (setuptools >= 61)
    if getattr(dist.metadata, "py_modules", None) is None:
        dist.py_modules = []


DistributionMetadata = type(Distribution().metadata)
"""Dummy class to hold the distribution meta-data: name, version, author,
and so forth."""
