"""A collection of functions which are triggered automatically by finder when
shapely package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_shapely(finder: ModuleFinder, module: Module) -> None:
    """Hook for shapely."""
    module_path = module.file.parent
    source_dir = module_path.parent / f"{module.name}.libs"
    if source_dir.exists():
        target_dir = f"lib/{source_dir.name}"
        for source in source_dir.iterdir():
            finder.lib_files[source] = f"{target_dir}/{source.name}"
