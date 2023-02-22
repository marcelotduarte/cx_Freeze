"""A collection of functions which are triggered automatically by finder when
pytz package is included."""

from __future__ import annotations

import os
from pathlib import Path

from ..finder import ModuleFinder
from ..module import Module


def load_pytz(finder: ModuleFinder, module: Module) -> None:
    """The pytz module requires timezone data to be found in a known directory
    or in the zip file where the package is written."""
    target_path = Path("lib", "pytz", "zoneinfo")
    data_path = module.path[0] / "zoneinfo"
    if not data_path.is_dir():
        # Fedora (and possibly other systems) use a separate location to
        # store timezone data so look for that here as well
        pytz = __import__("pytz")
        data_path = Path(
            getattr(pytz, "_tzinfo_dir", None)
            or os.getenv("PYTZ_TZDATADIR")
            or "/usr/share/zoneinfo"
        )
        if data_path.is_dir():
            finder.add_constant("PYTZ_TZDATADIR", os.fspath(target_path))
    if data_path.is_dir():
        if module.in_file_system >= 1:
            finder.include_files(
                data_path, target_path, copy_dependent_files=False
            )
        else:
            finder.zip_include_files(data_path, Path("pytz", "zoneinfo"))
