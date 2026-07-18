"""Hooks triggered by finder when comtypes package is included."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for comtypes."""

    def comtypes(self, finder: ModuleFinder, module: Module) -> None:
        """Include the lazily imported stream module."""
        finder.exclude_module("comtypes.test")
        finder.include_module("comtypes.stream", module)
