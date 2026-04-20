"""A collection of functions which are triggered automatically by finder when
zoneinfo package is included.
"""

from __future__ import annotations

from importlib.machinery import SourceFileLoader
from pathlib import Path
from pkgutil import resolve_name
from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze.hooks.global_names import ZONEINFO_GLOBAL_NAMES
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for zoneinfo."""

    def zoneinfo(self, finder: ModuleFinder, module: Module) -> None:
        """The zoneinfo package requires timezone data.
        The timezone data can be retrieved from tzdata package or from the OS.
        """
        module.global_names.update(ZONEINFO_GLOBAL_NAMES)
        # check if zoneinfo directory is available
        source_path = None
        tzpath = resolve_name("zoneinfo.TZPATH")
        if tzpath:
            for path in tzpath:
                if path.endswith("zoneinfo"):
                    source_path = Path(path).resolve()
                    break
        if source_path and source_path.is_dir():
            # remove tzdata from the missing modules
            module.ignore_names.add("tzdata")

        # check if tzdata package is available
        if finder.include_package("tzdata", module) is None:
            if source_path is None:
                return
            target_path = "share/zoneinfo"
            finder.include_files(
                source_path, target_path, copy_dependent_files=False
            )
        else:
            target_path = "lib/tzdata/zoneinfo"  # valid if not using zip file

        # patch source code
        if not isinstance(module.loader, SourceFileLoader):
            return

        patch = f"""
            # cx_Freeze patch start
            def _cx_freeze_patch():
                import os as _os
                import sys as _sys
                _prefix = _sys.prefix
                if _sys.platform == "darwin":
                    _prefix_parent = _os.path.dirname(_prefix)
                    _mac_prefix = _os.path.join(_prefix_parent, "Resources")
                    if _os.path.exists(_mac_prefix):
                        _prefix = _mac_prefix  # using bdist_mac
                _target_path = _os.path.normpath("{target_path}")
                _tzpath = _os.path.join(_prefix, _target_path)
                if not _os.path.exists(_tzpath):
                    try:
                        import tzdata as _tzdata
                    except ImportError:
                        pass
                    else:
                        _tzpath = _os.path.join(
                            _os.path.dirname(_tzdata.__file__), "zoneinfo")
                _os.environ["PYTHONTZPATH"] = _tzpath
            _cx_freeze_patch()
            # cx_Freeze patch end
        """
        loader = module.loader
        path = loader.get_filename(module.name)
        source_code = loader.get_source(module.name)
        module.code = loader.source_to_code(
            dedent(patch) + source_code, path, _optimize=finder.optimize
        )
