"""A collection of functions which are triggered automatically by finder when
pymupdf package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_pymupdf(finder: ModuleFinder, module: Module) -> None:  # noqa: ARG001
    """The pymupdf must include mupdf."""
    finder.include_module("pymupdf.mupdf")
