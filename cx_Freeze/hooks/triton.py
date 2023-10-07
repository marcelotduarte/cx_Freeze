"""A collection of functions which are triggered automatically by finder when
triton package is included.
"""
from __future__ import annotations

from cx_Freeze.finder import ModuleFinder
from cx_Freeze.module import Module


def load_triton(finder: ModuleFinder, module: Module) -> None:  # noqa: ARG001
    """Hook for triton."""
    # exclude C files and testing
    finder.exclude_module("triton._C")
    finder.exclude_module("triton.testing")
