"""A collection of functions which are triggered automatically by finder when
AV (PyAV) package is included.
"""

from __future__ import annotations

import sys
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze.module import ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for AV (pyAV).

    Supported pypi versions (tested from 11.0 to 16.0.1).
    """

    def av(self, finder: ModuleFinder, module: Module) -> None:
        """The AV (PyAV) package."""
        if module.in_file_system == 0:
            finder.include_package("av")
        with suppress(ImportError):
            finder.include_module("av.deprecation")

        # conda-forge Windows
        source = Path(sys.base_prefix, "Library/bin/SDL3.dll")
        if source.exists():
            target = f"lib/{source.name}"
            finder.lib_files[source] = target
            finder.include_files(source, target)

    def av_container(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Newer version of AV needs uuid."""
        finder.include_module("uuid")
