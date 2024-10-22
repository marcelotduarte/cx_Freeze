"""A collection of functions which are triggered automatically by finder when
pytz package is included.
"""

from __future__ import annotations

import os
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module

__all__ = ["load_pytz"]


def load_pytz(finder: ModuleFinder, module: Module) -> None:
    """The pytz module requires timezone data to be found in a known directory
    or in the zip file where the package is written.
    """
    module.exclude_names.add("doctest")
    source_path = module.file.parent / "zoneinfo"
    if not source_path.is_dir():
        # Fedora (and possibly other systems) use a separate location to
        # store timezone data so look for that here as well
        source_path = Path(os.getenv("PYTZ_TZDATADIR", "/usr/share/zoneinfo"))
    if source_path.is_dir():
        if module.in_file_system == 0:
            finder.zip_include_files(source_path, "pytz/zoneinfo")
            return
        target_path = "share/zoneinfo"
        finder.include_files(
            source_path, target_path, copy_dependent_files=False
        )
        # patch source code
        source = f"""
            # cx_Freeze patch start
            import os as _os
            import sys as _sys
            _prefix = _sys.prefix if _sys.prefix else _sys.frozen_dir
            if _sys.platform == "darwin":
                _mac_prefix = _os.path.join(
                    _os.path.dirname(_prefix), "Resources"
                )
                if _os.path.exists(_mac_prefix):
                    _prefix = _mac_prefix  # using bdist_mac
            _os.environ["PYTZ_TZDATADIR"] = _os.path.join(
                _prefix, _os.path.normpath("{target_path}")
            )
            # cx_Freeze patch end
        """
        code_string = module.file.read_text(encoding="utf_8")
        module.code = compile(
            code_string + dedent(source),
            module.file.as_posix(),
            "exec",
            dont_inherit=True,
            optimize=finder.optimize,
        )
