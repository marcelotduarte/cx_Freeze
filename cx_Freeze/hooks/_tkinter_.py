"""A collection of functions which are triggered automatically by finder when
TKinter package is included.
"""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import EXT_SUFFIX, IS_WINDOWS
from cx_Freeze.common import get_resource_file_path

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_tkinter(finder: ModuleFinder, module: Module) -> None:
    """The tkinter module has data files (also called tcl/tk libraries) that
    are required to be loaded at runtime.
    """
    tcl_library = None
    tk_library = None
    # manylinux (and macpython) wheels store tcl/tk libraries and extension
    share = get_resource_file_path("bases", "share", "")
    lib_dynload_tkinter = get_resource_file_path(
        "bases", "lib-dynload/_tkinter", EXT_SUFFIX
    )
    if (
        share
        and share.is_dir()
        and lib_dynload_tkinter
        and lib_dynload_tkinter.exists()
    ):
        tcl_library = next(share.glob("tcl*.*"), None)
        tk_library = next(share.glob("tk*.*"), None)
    if tcl_library is None:
        # search for the tcl/tk libraries (Windows, MSYS2, conda-forge, etc)
        try:
            tkinter = __import__("tkinter")
        except ImportError:
            return
        try:
            root = tkinter.Tk(useTk=False)
        except tkinter.TclError:
            # provisional fix for Python 3.13 beta and rc1 [windows]
            tcl_library = Path(
                sys.base_prefix, "tcl", f"tcl{tkinter.TclVersion}"
            )
            if not tcl_library.exists():
                return
        else:
            tcl_library = Path(root.tk.exprstring("$tcl_library"))
        tk_library = tcl_library.parent / tcl_library.name.replace("tcl", "tk")
    # include tcl/tk files
    for source_path in [tcl_library, tcl_library.with_suffix(""), tk_library]:
        if source_path.is_dir():
            finder.include_files(source_path, f"share/{source_path.name}")
        if IS_WINDOWS:  # include dlls like tcl86t.dll and tk86t.dll
            dll_name = source_path.name.replace(".", "") + "t.dll"
            dll_path = Path(sys.base_prefix, "DLLs", dll_name)
            if dll_path.exists():
                finder.include_files(dll_path, f"lib/{dll_name}")
    # patch source code
    source = rf"""
        # cx_Freeze patch start
        import os as _os
        import sys as _sys
        _prefix = _sys.prefix if _sys.prefix else _sys.frozen_dir
        if _sys.platform == "darwin":
            _mac_prefix = _os.path.join(_os.path.dirname(_prefix), "Resources")
            if _os.path.exists(_mac_prefix):
                _prefix = _mac_prefix  # using bdist_mac
        _tcl_library = _os.path.join(_prefix, "share", "{tcl_library.name}")
        _tk_library = _os.path.join(_prefix, "share", "{tk_library.name}")
        _os.environ["TCL_LIBRARY"] = _os.path.normpath(_tcl_library)
        _os.environ["TK_LIBRARY"] = _os.path.normpath(_tk_library)

        # cx_Freeze patch end
    """
    code_string = module.file.read_text(encoding="utf_8") + dedent(source)
    module.code = compile(
        code_string,
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )
