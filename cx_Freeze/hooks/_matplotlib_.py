"""A collection of functions which are triggered automatically by finder when
matplotlib package is included.
"""

from __future__ import annotations

from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze.common import code_object_replace_function

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_matplotlib(finder: ModuleFinder, module: Module) -> None:
    """The matplotlib package requires mpl-data subdirectory."""
    # mpl-data is always in a subdirectory in matplotlib >= 3.4
    if module.in_file_system == 0:
        # zip_include_packages
        source_data = module.file.parent / "mpl-data"
        target_data = Path("lib", module.name, "mpl-data")
        _patch_data_path(module, target_data)
        finder.include_files(
            source_data, target_data, copy_dependent_files=False
        )
    finder.include_package("matplotlib")
    finder.exclude_module("matplotlib.tests")
    finder.exclude_module("matplotlib.testing")
    with suppress(ImportError):
        finder.include_module("mpl_toolkits")


def _patch_data_path(module: Module, data_path: Path) -> None:
    # fix get_data_path functions when using zip_include_packages or
    # with some distributions that have matplotlib < 3.4 installed.
    code = module.code
    if code is None:
        return
    for name in ("_get_data_path", "get_data_path"):
        source = f"""\
        def {name}():
            import os as _os
            import sys as _sys
            return _os.path.join(_sys.prefix, "{data_path}")
        """
        # patch if the name (_get_data_path and/or get_data_path) is found
        code = code_object_replace_function(code, name, source)
    module.code = code
