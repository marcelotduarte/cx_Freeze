"""A collection of functions which are triggered automatically by finder when
importlib namespace is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for importlib."""

    def importlib(self, finder: ModuleFinder, module: Module) -> None:
        """The importlib module should filter import names."""
        if module.in_file_system == 1:
            # Use optimized mode
            module.in_file_system = 2
        # include module used by importlib._bootstrap_external
        # (internally mapped to _frozen_importlib_external)
        finder.include_module("importlib.metadata")
        finder.include_module("importlib.readers")

    def importlib_metadata(self, finder: ModuleFinder, module: Module) -> None:
        """The importlib.metadata module should filter import names."""
        if module.name == "importlib.metadata":
            module.ignore_names.add("pep517")
            finder.include_module("email")
