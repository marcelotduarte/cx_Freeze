"""A collection of functions which are triggered automatically by finder when
TKinter package is included."""
# pylint: disable=unused-argument
from __future__ import annotations

import os
import sys
from pathlib import Path

from .._compat import IS_WINDOWS
from ..common import get_resource_file_path
from ..finder import ModuleFinder
from ..module import Module


def load_tkinter(finder: ModuleFinder, module: Module) -> None:
    """The tkinter module has data files (also called tcl/tk libraries) that
    are required to be loaded at runtime."""
    folders = []
    tcltk = get_resource_file_path("bases", "tcltk", "")
    if tcltk and tcltk.is_dir():
        # manylinux wheels and macpython wheels store tcl/tk libraries
        folders.append(("TCL_LIBRARY", list(tcltk.glob("tcl*"))[0]))
        folders.append(("TK_LIBRARY", list(tcltk.glob("tk*"))[0]))
    else:
        # Windows, MSYS2, Miniconda: collect the tcl/tk libraries
        try:
            tkinter = __import__("tkinter")
        except (ImportError, AttributeError):
            return
        root = tkinter.Tk(useTk=False)
        source_path = Path(root.tk.exprstring("$tcl_library"))
        folders.append(("TCL_LIBRARY", source_path))
        source_name = source_path.name.replace("tcl", "tk")
        source_path = source_path.parent / source_name
        folders.append(("TK_LIBRARY", source_path))
    for env_name, source_path in folders:
        target_path = Path("lib", "tcltk", source_path.name)
        finder.add_constant(env_name, os.fspath(target_path))
        finder.include_files(source_path, target_path)
        if IS_WINDOWS:
            dll_name = source_path.name.replace(".", "") + "t.dll"
            dll_path = Path(sys.base_prefix, "DLLs", dll_name)
            if not dll_path.exists():
                continue
            finder.include_files(dll_path, Path("lib", dll_name))
