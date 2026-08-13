"""Hooks triggered by finder when TKinter package is included."""

from __future__ import annotations

import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import EXT_SUFFIX, IS_WINDOWS
from cx_Freeze.common import resource_path
from cx_Freeze.hooks.global_names import TKINTER_GLOBAL_NAMES
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for TKinter."""

    def tkinter(self, finder: ModuleFinder, module: Module) -> None:
        """Include required tcl/tk 8.x script library to be loaded at runtime.

        Tcl/Tk 9 embeds the script library in the DLLs on Windows and has been
        used in Python 3.14.7+.
        """
        # Ignore names that should not be confused with modules to be imported
        module.global_names.update(TKINTER_GLOBAL_NAMES)

        # The tcl/tk 8.x script library are stored in the wheel of freeze-core
        # when using manylinux and macpython.
        tcl_library = None
        tk_library = None
        share = resource_path("share")
        lib_tkinter = resource_path(f"lib/_tkinter{EXT_SUFFIX}")
        if share and share.is_dir() and lib_tkinter and lib_tkinter.exists():
            tcl_library = next(share.glob("tcl*.*"), None)
            tk_library = next(share.glob("tk*.*"), None)
        if tcl_library is None or tk_library is None:
            # Check for tcl/tk >= 9.0 (initially only on Windows)
            try:
                tkinter = __import__("tkinter")
            except ImportError:
                return
            tcl_version = tkinter.TclVersion
            tk_version = tkinter.TkVersion
            # Include dlls for Windows (when using lief, they are detected)
            if IS_WINDOWS:
                tk_ext = finder.include_module("_tkinter")
                if tk_ext is None or tk_ext.file is None:
                    return
                if tcl_version >= 9.0:
                    # Include dlls like tcl90.dll and tcl9tk90.dll
                    dll_names = (
                        f"tcl{int(tcl_version * 10)}.dll",
                        f"tcl{int(tcl_version)}tk{int(tk_version * 10)}.dll",
                    )
                else:
                    # Include dlls like tcl86t.dll and tk86t.dll
                    dll_names = (
                        f"tcl{int(tcl_version * 10)}t.dll",
                        f"tk{int(tk_version * 10)}t.dll",
                    )
                for dll_name in dll_names:
                    dll_path = tk_ext.file.parent / dll_name
                    if dll_path.exists():
                        finder.include_files(dll_path, f"lib/{dll_name}")
                if tcl_version >= 9.0:
                    return

            # Search tcl/tk 8.x libraries (Windows, MSYS2, conda-forge, etc)
            # And tcl/tk 9.x for Linux (at least with uv python)
            try:
                root = tkinter.Tk(useTk=False)
            except tkinter.TclError:
                # provisional fix for Python 3.13 beta and rc1 [windows]
                tcl_prefix = Path(sys.base_prefix, "tcl")
                tcl_library = tcl_prefix / f"tcl{tcl_version}"
                if not tcl_library.exists():
                    return
                tk_library = tcl_prefix / f"tk{tk_version}"
            else:
                tcl_library_expr = root.tk.exprstring("$tcl_library")
                if tcl_library_expr.startswith("//zipfs:"):
                    # tcl/tk 9.0+ embebed scripts
                    return
                tcl_library = Path(tcl_library_expr)
                tk_library = tcl_library.parent.joinpath(
                    tcl_library.name.replace("tcl", "tk")
                )

        # Include tcl/tk 8.x/9.x script libraries
        self._include_script_libraries(finder, module, tcl_library, tk_library)

    def _include_script_libraries(
        self,
        finder: ModuleFinder,
        module: Module,
        tcl_library: Path,
        tk_library: Path,
    ) -> None:
        # Include tcl/tk 8.x directories
        for source_path in [
            tcl_library,
            tcl_library.with_suffix(""),
            tk_library,
        ]:
            if source_path.is_dir():
                finder.include_files(source_path, f"share/{source_path.name}")
        # Patch source code to point to shared data
        patch = rf"""
            # cx_Freeze patch start
            import os as _os
            import sys as _sys
            _prefix = _sys.prefix
            if _sys.platform == "darwin":
                _mac_prefix = _os.path.join(
                    _os.path.dirname(_prefix), "Resources"
                )
                if _os.path.exists(_mac_prefix):
                    _prefix = _mac_prefix  # using bdist_mac
            _tcl_library = _os.path.join(
                _prefix, "share", "{tcl_library.name}"
            )
            _tk_library = _os.path.join(_prefix, "share", "{tk_library.name}")
            _os.environ["TCL_LIBRARY"] = _os.path.normpath(_tcl_library)
            _os.environ["TK_LIBRARY"] = _os.path.normpath(_tk_library)
            # cx_Freeze patch end
        """
        loader = module.loader
        if not isinstance(loader, SourceFileLoader):
            return
        source_code = loader.get_source(module.name)
        if source_code is None:
            return
        module.code = loader.source_to_code(
            source_code + dedent(patch),
            loader.get_filename(module.name),
            _optimize=finder.optimize,
        )
