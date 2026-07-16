"""Hooks triggered by finder when importlib package is included."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for importlib package."""

    def importlib(self, finder: ModuleFinder, module: Module) -> None:
        """Hooks for importlib package."""

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

    def importlib_metadata(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        """Ignore optional modules."""
        if module.name == "importlib.metadata":
            module.ignore_names.add("pep517")  # Python 3.10
