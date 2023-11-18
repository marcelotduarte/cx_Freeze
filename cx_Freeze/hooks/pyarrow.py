"""A collection of functions which are triggered automatically by finder when
pyarrow package is included.
"""
from __future__ import annotations

from cx_Freeze.finder import ModuleFinder
from cx_Freeze.module import Module


def load_pyarrow(finder: ModuleFinder, module: Module) -> None:  # noqa: ARG001
    """The pyarrow must include vendored modules."""
    finder.exclude_module("pyarrow.tests")
    finder.include_module("pyarrow.vendored.docscrape")
    finder.include_module("pyarrow.vendored.version")
