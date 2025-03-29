"""A collection of functions which are triggered automatically by finder when
VTK package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_WINDOWS
from cx_Freeze.hooks.libs import replace_delvewheel_patch

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_vtkmodules(finder: ModuleFinder, module: Module) -> None:
    """The VTK (vtkmodules) package.

    Supported pypi versions (tested from 9.2.6 to 9.3.1).
    """
    source_dir = module.file.parent.parent / "vtk.libs"
    if source_dir.exists():  # vtk >= 9.3.0
        target_dir = f"lib/{source_dir.name}"
        if IS_WINDOWS:
            finder.include_files(source_dir, target_dir)
            replace_delvewheel_patch(module, source_dir.name)
        else:
            for source in source_dir.iterdir():
                finder.lib_files[source] = f"{target_dir}/{source.name}"
    module.ignore_names.add("_vtkmodules_static")
    module.ignore_names.add("vtkmodules._build_paths")
