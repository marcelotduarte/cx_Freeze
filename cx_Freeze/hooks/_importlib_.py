"""A collection of functions which are triggered automatically by finder when
importlib namespace is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_importlib(finder: ModuleFinder, module: Module) -> None:
    """The importlib module should filter import names."""
    if module.in_file_system == 1:
        # Use optimized mode
        module.in_file_system = 2
    # include module used by importlib._bootstrap_external
    # (internally mapped to _frozen_importlib_external)
    finder.include_module("importlib.metadata")
    with suppress(ImportError):
        finder.include_module("importlib.readers")  # Python 3.10+


def load_importlib_metadata(finder: ModuleFinder, module: Module) -> None:
    """The importlib.metadata module should filter import names."""
    if module.name == "importlib.metadata":
        module.ignore_names.add("pep517")
        finder.include_module("email")
