"""A collection of functions which are triggered automatically by finder when
matplotlib package is included."""

from __future__ import annotations

import os
from pathlib import Path

from ..common import code_object_replace
from ..finder import ModuleFinder
from ..module import Module


def load_matplotlib(finder: ModuleFinder, module: Module) -> None:
    """The matplotlib package requires mpl-data subdirectory."""
    data_path = module.path[0] / "mpl-data"
    target_path = Path("lib", module.name, "mpl-data")
    # After matplotlib 3.4 mpl-data is guaranteed to be a subdirectory.
    if not data_path.is_dir():
        data_path = __import__("matplotlib").get_data_path()
        need_patch = True
    else:
        need_patch = module.in_file_system == 0
    finder.include_files(data_path, target_path, copy_dependent_files=False)
    finder.include_package("matplotlib")
    finder.exclude_module("matplotlib.tests")
    finder.exclude_module("matplotlib.testing")
    if not need_patch or module.code is None:
        return
    code_to_inject = f"""
def _get_data_path():
    import os, sys
    return os.path.join(os.path.dirname(sys.executable), "{target_path!s}")
"""
    for code_str in [
        code_to_inject,
        code_to_inject.replace("_get_data_path", "get_data_path"),
    ]:
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
