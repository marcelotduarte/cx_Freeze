"""Helper functions for hooks."""

from __future__ import annotations

from types import CodeType

from ..common import code_object_replace_function
from ..module import Module


def replace_delvewheel_patch(module: Module) -> None:
    """Replace delvewheel injections of code to not find for module.libs
    directory.
    """
    code = module.code
    if code is None:
        return

    delvewheel_func = "_delvewheel_init_patch_"
    consts = list(code.co_consts)
    for constant in consts:
        if isinstance(constant, CodeType):
            name = constant.co_name
            if name.startswith(delvewheel_func):
                source = f"""\
                def {name}():
                    import os, sys

                    libs_path = os.path.join(
                        sys.frozen_dir, "lib", "{module.name}.libs"
                    )
                    try:
                        os.add_dll_directory(libs_path)
                    except (OSError, AttributeError):
                        pass
                    env_path = os.environ.get("PATH", "").split(os.pathsep)
                    if libs_path not in env_path:
                        env_path.insert(0, libs_path)
                        os.environ["PATH"] = os.pathsep.join(env_path)
                """
                code = code_object_replace_function(code, name, source)
                break
    module.code = code
