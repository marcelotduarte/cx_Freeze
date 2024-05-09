"""Initialization script for cx_Freeze which manipulates the path so that the
directory in which the executable is found is searched for extensions but
no other directory is searched. The environment variable LD_LIBRARY_PATH is
manipulated first, however, to ensure that shared libraries found in the
target directory are found. This requires a restart of the executable because
the environment variable LD_LIBRARY_PATH is only checked at startup.

"""

from __future__ import annotations

import importlib.util
import os
import sys

DIR_NAME = os.path.dirname(sys.executable)

paths = os.environ.get("LD_LIBRARY_PATH", "").split(os.pathsep)

if DIR_NAME not in paths:
    paths.insert(0, DIR_NAME)
    os.environ["LD_LIBRARY_PATH"] = os.pathsep.join(paths)
    os.execv(sys.executable, sys.argv)  # noqa: S606

sys.frozen = True
sys.path = sys.path[:4]


def run(name) -> None:
    """Execute the main script of the frozen application."""
    spec = importlib.util.find_spec(name)
    code = spec.loader.get_code(name)
    main_module = sys.modules["__main__"]
    main_globals = main_module.__dict__
    main_globals.update(
        __cached__=spec.cached,
        __file__=spec.cached,
        __loader__=spec.loader,
        __spec__=spec,
    )
    exec(code, main_globals)
