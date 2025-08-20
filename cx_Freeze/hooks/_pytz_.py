"""A collection of functions which are triggered automatically by finder when
pytz package is included.
"""

from __future__ import annotations

import os
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for pytz."""

    def pytz(self, finder: ModuleFinder, module: Module) -> None:
        """The pytz module requires timezone data to be found in a known
        directory or in the zip file where the package is written.
        """
        module.exclude_names.add("doctest")
        source_path = module.file.parent / "zoneinfo"
        if not source_path.is_dir():
            # Fedora (and possibly other systems) use a separate location to
            # store timezone data so look for that here as well
            source_path = Path(
                os.getenv("PYTZ_TZDATADIR", "/usr/share/zoneinfo")
            )
            if not source_path.is_dir():
                return
        code_bytes = module.file.read_bytes()
        if module.in_file_system == 0:
            finder.zip_include_files(source_path, "pytz/zoneinfo")
            # patch source code
            source = """
                # cx_Freeze patch start
                import warnings
                warnings.filterwarnings("ignore", "pkg_resources")
                # cx_Freeze patch end
            """
            code_bytes = dedent(source).encode() + code_bytes
        else:
            target_path = "share/zoneinfo"
            finder.include_files(
                source_path, target_path, copy_dependent_files=False
            )
            # patch source code
            source = f"""
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
                _os.environ["PYTZ_TZDATADIR"] = _os.path.join(
                    _prefix, _os.path.normpath("{target_path}")
                )
                # cx_Freeze patch end
            """
            code_bytes += dedent(source).encode()
        module.code = compile(
            code_bytes,
            module.file.as_posix(),
            "exec",
            dont_inherit=True,
            optimize=finder.optimize,
        )
