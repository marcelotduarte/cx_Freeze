"""Hooks triggered by finder when pythonnet (clr) package is included."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder

__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for pythonnet."""

    def clr(self, finder: ModuleFinder, module: Module) -> None:
        """Include the runtime library (Python.Runtime.dll).

        The pythonnet package is imported as 'clr'.
        """
        if module.file is None:
            return
        dll_name = "Python.Runtime.dll"
        dll_path = module.file.parent / dll_name
        if not dll_path.exists():
            dll_path = module.file.parent / "pythonnet" / "runtime" / dll_name
            if not dll_path.exists():
                return
        finder.include_files(dll_path, f"lib/{dll_name}")
