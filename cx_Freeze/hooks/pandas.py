"""A collection of functions which are triggered automatically by finder when
pandas package is included.
"""
from __future__ import annotations

from cx_Freeze.finder import ModuleFinder
from cx_Freeze.hooks._libs import replace_delvewheel_patch
from cx_Freeze.module import Module


def load_pandas(finder: ModuleFinder, module: Module) -> None:
    """The pandas package loads items within itself in a way that causes
    problems without libs and a number of subpackages being present.
    """
    source_dir = module.file.parent.parent / f"{module.name}.libs"
    if source_dir.exists():  # pandas >= 2.1.0
        finder.include_files(source_dir, f"lib/{source_dir.name}")
    replace_delvewheel_patch(module)
    finder.include_package("pandas._libs")
    finder.exclude_module("pandas.conftest")
    finder.exclude_module("pandas.tests")
