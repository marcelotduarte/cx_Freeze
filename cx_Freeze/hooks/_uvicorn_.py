"""Hooks triggered by finder when uvicorn package is included."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for uvicorn."""

    def uvicorn_importer(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Include subpackages required by import_from_string."""
        finder.include_package("uvicorn.protocols")
        finder.include_package("uvicorn.lifespan")
        finder.include_package("uvicorn.loops")
