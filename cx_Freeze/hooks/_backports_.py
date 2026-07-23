"""Hooks triggered by finder when backports namespace is included."""

from __future__ import annotations

from importlib.machinery import SourceFileLoader
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for backports."""

    def backports(self, finder: ModuleFinder, module: Module) -> None:
        """Hooks for backports namespace."""
        loader = module.loader
        if not isinstance(loader, SourceFileLoader):
            return
        module.code = loader.source_to_code(
            "",
            loader.get_filename(module.name),
            _optimize=finder.optimize,
        )

    def backports_zstd(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Filter import names."""
        finder.exclude_module("backports.zstd._cffi")
