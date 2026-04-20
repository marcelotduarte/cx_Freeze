"""A collection of functions which are triggered automatically by finder when
backports namespace is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for backports."""

    def backports(self, finder: ModuleFinder, module: Module) -> None:
        """The backports namespace cleanup."""
        loader = module.loader
        path = loader.get_filename(module.name)
        module.code = loader.source_to_code(
            "", path, _optimize=finder.optimize
        )

    def backports_zstd(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The backports.zstd module should filter import names."""
        finder.exclude_module("backports.zstd._cffi")
