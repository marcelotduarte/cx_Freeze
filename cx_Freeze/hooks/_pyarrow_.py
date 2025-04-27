"""A collection of functions which are triggered automatically by finder when
pyarrow package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.hooks.libs import replace_delvewheel_patch

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_pyarrow(finder: ModuleFinder, module: Module) -> None:
    """The pyarrow must include vendored modules.

    Supported pypi and conda-forge versions (tested from 14.0 to 20.0).
    """
    source_dir = module.file.parent.parent / f"{module.name}.libs"
    if source_dir.exists():
        # pyarrow >= 20.0 windows
        finder.include_files(source_dir, f"lib/{source_dir.name}")
        replace_delvewheel_patch(module)
    finder.exclude_module("pyarrow.tests")
    finder.include_module("pyarrow.vendored.docscrape")
    finder.include_module("pyarrow.vendored.version")
    finder.include_module("queue")
