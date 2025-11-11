"""A collection of functions which are triggered automatically by finder when
winrt package (pywinrt) is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for winrt (pywinrt)."""

    def winrt(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        finder.include_package("winrt")

    def __getattr__(self, name: str) -> Any:
        if name.startswith("winrt_"):

            def _include_subpackage(
                finder: ModuleFinder, module: Module
            ) -> None:
                finder.include_package(module.name)

            return _include_subpackage
        return super().__getattribute__(name)
