"""A collection of functions which are triggered automatically by finder when
backports namespace is included.
"""
from __future__ import annotations

from cx_Freeze.finder import ModuleFinder
from cx_Freeze.hooks.zoneinfo import load_zoneinfo
from cx_Freeze.module import Module


def load_backports_zoneinfo(finder: ModuleFinder, module: Module) -> None:
    """The backports.zoneinfo module should be a drop-in replacement for the
    Python 3.9 standard library module zoneinfo.
    """
    load_zoneinfo(finder, module)


def load_backports_zoneinfo__common(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """Ignore module not used in Python 3.8."""
    module.ignore_names.add("importlib_resources")


def load_backports_zoneinfo__tzpath(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """Ignore module not used in Python 3.8."""
    module.ignore_names.add("importlib_resources")


__all__ = [
    "load_backports_zoneinfo",
    "load_backports_zoneinfo__common",
    "load_backports_zoneinfo__tzpath",
]
