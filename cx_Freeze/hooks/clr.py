"""A collection of functions which are triggered automatically by finder when
pythonnet package is included.
"""

from __future__ import annotations

from ..finder import ModuleFinder
from ..module import Module


def load_clr(finder: ModuleFinder, module: Module) -> None:
    """The pythonnet package (imported as 'clr') needs Python.Runtime.dll
    in runtime.
    """
    dll_name = "Python.Runtime.dll"
    dll_path = module.file.parent / dll_name
    if not dll_path.exists():
        dll_path = module.file.parent / "pythonnet/runtime" / dll_name
        if not dll_path.exists():
            return
    finder.include_files(dll_path, f"lib/{dll_name}")
