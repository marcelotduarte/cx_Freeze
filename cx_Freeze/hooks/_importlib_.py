"""Hooks triggered by finder when importlib package is included."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for importlib."""

    def importlib(self, finder: ModuleFinder, module: Module) -> None:
        """Hooks for importlib package."""
        if module.in_file_system == 1:
            # Use optimized mode
            module.in_file_system = 2
        # include module used by importlib._bootstrap_external
        # (internally mapped to _frozen_importlib_external)
        finder.include_module("importlib.metadata")
        finder.include_module("importlib.readers")

    def importlib__bootstrap(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        """Set importlib._bootstrap as an alias."""
        finder.add_alias(module.name, "_frozen_importlib")

    def importlib__bootstrap_external(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        """Set importlib._bootstrap_external as an alias."""
        finder.add_alias(module.name, "_frozen_importlib_external")

    def importlib_metadata(self, finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        if module.name == "importlib.metadata":
            module.ignore_names.add("pep517")
            finder.include_module("email")
