"""A collection of functions which are triggered automatically by finder when
tzdata package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_tzdata(finder: ModuleFinder, module: Module) -> None:
    """The tzdata package requires its zone and timezone data."""
    if module.in_file_system == 0:
        finder.zip_include_files(module.file.parent, "tzdata")
