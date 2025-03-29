"""A collection of functions which are triggered automatically by finder when
pymupdf package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_pymupdf(finder: ModuleFinder, module: Module) -> None:
    """The pymupdf must include hidden modules."""
    module.ignore_names.update(
        ["mupdf_cppyy", "mupdf", "pymupdf_fonts", "PIL"]
    )
    finder.include_module("pymupdf.mupdf")
    finder.include_module("pymupdf.utils")
    finder.include_module("pymupdf._wxcolors")


def load_pymupdf_extra(_, module: Module) -> None:
    """Ignore development import."""
    module.ignore_names.add("_extra")


def load_pymupdf_mupdf(_, module: Module) -> None:
    """Ignore development import."""
    module.ignore_names.add("_mupdf")


def load_pymupdf_table(_, module: Module) -> None:
    """Ignore optional package."""
    module.ignore_names.add("pandas")


def load_pymupdf_utils(_, module: Module) -> None:
    """Ignore development import and optional package."""
    module.ignore_names.update(["mupdf", "fontTools.subset"])
