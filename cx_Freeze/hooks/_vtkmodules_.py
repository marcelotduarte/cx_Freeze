"""A collection of functions which are triggered automatically by finder when
VTK package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder

__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for vtkmodules (VTK package).

    Supported pypi versions (tested from 9.2.6 to 9.4.2).
    """

    def vtkmodules(
        self,
        finder: ModuleFinder,  # noqa:ARG002
        module: Module,
    ) -> None:
        """The VTK (vtkmodules) package."""
        module.update_distribution("vtk")
        module.ignore_names.add("_vtkmodules_static")
        module.ignore_names.add("vtkmodules._build_paths")
