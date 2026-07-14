"""Hooks triggered by finder when asuncio package is included."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.hooks.global_names import ASYNCIO_GLOBAL_NAMES
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for asyncio."""

    def asyncio(self, finder: ModuleFinder, module: Module) -> None:
        """Load asyncio as a package."""
        module.global_names.update(ASYNCIO_GLOBAL_NAMES)
        finder.include_package("asyncio")
