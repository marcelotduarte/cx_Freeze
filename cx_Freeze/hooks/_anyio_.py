"""Hooks triggered by finder when anyio package is included."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for anyio."""

    def anyio(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Include backends."""
        finder.exclude_module("anyio.pytest_plugin")
        finder.include_module("anyio._backends._asyncio")

    def anyio__backends__asyncio(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names |= {
            "_pytest.outcomes",
            "uvloop",  # optional on posix
            "winloop",  # optional on win32
        }

    def anyio__core__eventloop(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional module."""
        module.ignore_names.add("sniffio")
