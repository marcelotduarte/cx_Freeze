"""Hooks triggered by finder when ortools package is included."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for ortools."""

    def ortools(self, finder: ModuleFinder, module: Module) -> None:
        distribution = module.distribution
        if distribution:
            major_version = int(distribution.version[0])
            if distribution.installer == "conda":
                finder.include_module("numpy")
        else:
            major_version = 9
        if major_version >= 10:
            if module.in_file_system == 0:
                module.in_file_system = 1
            finder.include_module("google.protobuf.descriptor")
        elif module.in_file_system == 0:
            module.in_file_system = 2

    def ortools_constraint_solver_pywrapcp(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.add("_pywrapcp")
