"""A collection of functions which are triggered automatically by finder when
Pillow (PIL) package is included.
"""

from __future__ import annotations

from .._compat import IS_MACOS
from ..finder import ModuleFinder
from ..module import Module


def load_pil(finder: ModuleFinder, module: Module) -> None:
    """The Pillow must be loaded as a package."""
    finder.include_package("PIL")

    # [macos] copy dependent files when using zip_include_packages
    if IS_MACOS:
        source_dir = module.file.parent / ".dylibs"
        if source_dir.exists() and module.in_file_system == 0:
            finder.include_files(source_dir, "lib/.dylibs")
