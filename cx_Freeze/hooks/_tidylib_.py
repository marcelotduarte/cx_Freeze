"""A collection of functions which are triggered automatically by finder when
tidylib package is included.
"""

from __future__ import annotations

import sysconfig
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_LINUX
from cx_Freeze.dep_parser import ELFParser

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_tidylib(finder: ModuleFinder, module: Module) -> None:  # noqa: ARG001
    """The tidylib module implicitly loads a shared library."""
    if not IS_LINUX:
        return

    parser = ELFParser(finder.path, [sysconfig.get_config_var("LIBDIR")])
    library_path = parser.find_library("tidy")
    if library_path:
        finder.include_files(library_path, f"lib/{library_path.name}")
