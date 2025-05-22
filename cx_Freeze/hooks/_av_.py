"""A collection of functions which are triggered automatically by finder when
AV (PyAV) package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from cx_Freeze.module import ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for AV (pyAV).

    Supported pypi versions (tested from 11.0 to 14.4.0).
    """

    def av(self, finder: ModuleFinder, module: Module) -> None:
        """The AV (PyAV) package."""
        if module.in_file_system == 0:
            finder.include_package("av")
        with suppress(ImportError):
            finder.include_module("av.deprecation")

    def av_container(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa:ARG002
    ) -> None:
        """Newer version of AV needs uuid."""
        finder.include_module("uuid")
