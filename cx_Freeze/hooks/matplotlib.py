"""A collection of functions which are triggered automatically by finder when
matplotlib package is included.
"""

from __future__ import annotations

import os
from pathlib import Path

from ..common import code_object_replace
from ..finder import ModuleFinder
from ..module import Module


def load_matplotlib(finder: ModuleFinder, module: Module) -> None:
    """The matplotlib package requires mpl-data subdirectory."""
    target_path = Path("lib", module.name, "mpl-data")
    # mpl-data is always in a subdirectory in matplotlib >= 3.4
    data_path = module.path[0] / "mpl-data"
    if not data_path.is_dir():
        data_path = __import__("matplotlib").get_data_path()
        need_patch = True
    else:
        need_patch = module.in_file_system == 0  # zip_include_packages
    finder.include_files(data_path, target_path, copy_dependent_files=False)
    finder.include_package("matplotlib")
    finder.exclude_module("matplotlib.tests")
    finder.exclude_module("matplotlib.testing")
    # matplotlib >= 3.7 uses an additional library directory
    module_libs_name = "matplotlib.libs"
    source_dir = module.path[0].parent / module_libs_name
    if source_dir.exists():
        finder.include_files(source_dir, f"lib/{module_libs_name}")
    # Patch is used only if using zip_include_packages or
    # with some distributions that have matplotlib < 3.4 installed.
    if not need_patch or module.code is None:
        return
    code_to_inject = f"""
def _get_data_path():
    import os, sys
    return os.path.join(sys.frozen_dir, "{target_path}")
"""
    for code_str in [
        code_to_inject,
        code_to_inject.replace("_get_data_path", "get_data_path"),
    ]:
        # path if the name (_get_data_path and/or get_data_path) is found
        new_code = compile(code_str, os.fspath(module.file), "exec")
        co_func = new_code.co_consts[0]
        name = co_func.co_name
        code = module.code
        consts = list(code.co_consts)
        for i, constant in enumerate(consts):
            if isinstance(constant, type(code)) and constant.co_name == name:
                consts[i] = co_func
                break
        module.code = code_object_replace(code, co_consts=consts)
