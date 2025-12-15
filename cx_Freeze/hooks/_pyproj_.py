"""A collection of functions which are triggered automatically by finder when
pyproj package is included.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_WINDOWS
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for pyproj."""

    def pyproj_datadir(self, finder: ModuleFinder, module: Module) -> None:
        """Hook for pyproj.datadir."""
        distribution = module.root.distribution
        if distribution and distribution.installer == "conda":
            if IS_WINDOWS:
                source_path = Path(sys.prefix, "Library", "share", "proj")
            else:
                source_path = Path(sys.prefix, "share", "proj")
            if source_path.is_dir():
                finder.include_files(
                    source_path, "share/proj", copy_dependent_files=False
                )
            return
        if module.in_file_system == 0:
            # in zip file
            source_path = module.file.parent / "proj_dir" / "share" / "proj"
            if source_path.is_dir():
                finder.include_files(
                    source_path, "share/proj", copy_dependent_files=False
                )
