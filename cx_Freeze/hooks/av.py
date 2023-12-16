"""A collection of functions which are triggered automatically by finder when
PyAV package is included.
"""
from __future__ import annotations

from cx_Freeze._compat import IS_WINDOWS
from cx_Freeze.finder import ModuleFinder
from cx_Freeze.hooks._libs import replace_delvewheel_patch
from cx_Freeze.module import Module


def load_av(finder: ModuleFinder, module: Module) -> None:
    """The PyAV package."""
    libs_name = "pyav.libs"
    source_dir = module.file.parent.parent / libs_name
    if source_dir.exists() and IS_WINDOWS:
        finder.include_files(source_dir, f"lib/{libs_name}")
        replace_delvewheel_patch(module, libs_name)
    finder.include_module("av.deprecation")
