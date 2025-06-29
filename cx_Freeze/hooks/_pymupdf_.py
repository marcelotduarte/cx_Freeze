"""A collection of functions which are triggered automatically by finder when
pymupdf package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]

# Support for pymupdf >= 1.24.4


class Hook(ModuleHook):
    """The Hook class for pymupdf."""

    def pymupdf(self, finder: ModuleFinder, module: Module) -> None:
        """The pymupdf must include hidden modules."""
        if module.in_file_system == 0:
            module.in_file_system = 1
        module.ignore_names.update(
            ["mupdf_cppyy", "mupdf", "pymupdf_fonts", "PIL"]
        )
        with suppress(ImportError):
            finder.include_package("mupdf")  # conda
        with suppress(ImportError):
            finder.include_module("pymupdf.mupdf")
        with suppress(ImportError):
            finder.include_module("pymupdf.utils")
        with suppress(ImportError):
            finder.include_module("pymupdf._wxcolors")  # 1.25.4

    def pymupdf_extra(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore development import."""
        module.ignore_names.add("_extra")

    def pymupdf_mupdf(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore development import."""
        module.ignore_names.add("_mupdf")

    def pymupdf_table(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional package."""
        module.ignore_names.add("pandas")

    def pymupdf_utils(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore development import and optional package."""
        module.ignore_names.update(["mupdf", "fontTools.subset"])
