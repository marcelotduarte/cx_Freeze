"""A collection of functions which are triggered automatically by finder when
zoneinfo package is included.
"""

from __future__ import annotations

from pathlib import Path
from pkgutil import resolve_name
from textwrap import dedent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


__all__ = ["load_zoneinfo"]


def load_zoneinfo(finder: ModuleFinder, module: Module) -> None:
    """The zoneinfo package requires timezone data,
    that can be the in tzdata package, if installed.
    """
    module.global_names.add("TZPATH")
    try:
        finder.include_package("tzdata")
    except ImportError:
        target_path = None
    else:
        target_path = "lib/tzdata/zoneinfo"  # valid if not using zip file

    if target_path is None:
        # without tzdata, copy zoneinfo directory if available
        source_path = None
        tzpath = resolve_name("zoneinfo.TZPATH")
        if tzpath:
            for path in tzpath:
                if path.endswith("zoneinfo"):
                    source_path = Path(path).resolve()
                    break
        if source_path is None or not source_path.is_dir():
            # add tzdata to missing modules
            bad_modules = finder._bad_modules  # noqa: SLF001
            callers = bad_modules.setdefault("tzdata", {})
            callers[f"{module.name}_hook"] = None
            return
        target_path = "share/zoneinfo"
        finder.include_files(
            source_path, target_path, copy_dependent_files=False
        )

    # patch source code
    if module.file.suffix == ".pyc":  # source unavailable
        return

    source = f"""
        # cx_Freeze patch start
        def _cx_freeze_patch():
            import os as _os
            import sys as _sys
            _prefix = _sys.prefix if _sys.prefix else _sys.frozen_dir
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
    code_string = module.file.read_text(encoding="utf_8")
    module.code = compile(
        dedent(source) + code_string,
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )
