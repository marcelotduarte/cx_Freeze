"""A collection of functions which are triggered automatically by finder when
TKinter package is included.
"""

from __future__ import annotations

import sys
from pathlib import Path

from .._compat import IS_WINDOWS
from ..common import get_resource_file_path
from ..finder import ModuleFinder
from ..module import Module


def load_tkinter(finder: ModuleFinder, module: Module) -> None:  # noqa: ARG001
    """The tkinter module has data files (also called tcl/tk libraries) that
    are required to be loaded at runtime.
    """
    folders = {}
    tcltk = get_resource_file_path("bases", "tcltk", "")
    if tcltk and tcltk.is_dir():
        # manylinux wheels and macpython wheels store tcl/tk libraries
        folders["TCL_LIBRARY"] = next(iter(tcltk.glob("tcl*.*")))
        folders["TK_LIBRARY"] = next(iter(tcltk.glob("tk*.*")))
    else:
        # Windows, MSYS2, Miniconda: collect the tcl/tk libraries
        try:
            tkinter = __import__("tkinter")
        except (ImportError, AttributeError):
            return
        root = tkinter.Tk(useTk=False)
        source_path = Path(root.tk.exprstring("$tcl_library"))
        folders["TCL_LIBRARY"] = source_path
        source_name = source_path.name.replace("tcl", "tk")
        source_path = source_path.parent / source_name
        folders["TK_LIBRARY"] = source_path
    for env_name, source_path in folders.items():
        target_path = f"lib/{source_path.name}"
        finder.add_constant(env_name, target_path)
        finder.include_files(source_path, target_path)
        if env_name == "TCL_LIBRARY":
            tcl8_path = source_path.parent / source_path.stem
            if tcl8_path.is_dir():
                finder.include_files(tcl8_path, f"lib/{tcl8_path.name}")
        if IS_WINDOWS:
            dll_name = source_path.name.replace(".", "") + "t.dll"
            dll_path = Path(sys.base_prefix, "DLLs", dll_name)
            if not dll_path.exists():
                continue
            finder.include_files(dll_path, Path("lib", dll_name))
