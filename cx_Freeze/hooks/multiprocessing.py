"""A collection of functions which are triggered automatically by finder when
multiprocessing package is included.
"""
from __future__ import annotations

import os
from textwrap import dedent

from cx_Freeze._compat import IS_WINDOWS
from cx_Freeze.finder import ModuleFinder
from cx_Freeze.module import Module


def load_multiprocessing(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The forkserver method calls utilspawnv_passfds in ensure_running to
    pass a command line to python. In cx_Freeze the running executable
    is called, then we need to catch this and use exec function.
    For the spawn method there are a similar process to resource_tracker.

    Note: Using multiprocessing.spawn.freeze_support directly because it works
    for all OS, not only Windows.
    """
    # Support for:
    # - fork in Unix (including macOS) is native;
    # - spawn in Windows is native (since 4.3.4) but was improved in v6.2;
    # - spawn and forkserver in Unix is implemented here.
    if IS_WINDOWS:
        return
    if module.file.suffix == ".pyc":  # source unavailable
        return
    source = r"""
    # cx_Freeze patch start
    import re
    import sys
    if len(sys.argv) >= 2 and sys.argv[-2] == "-c":
        cmd = sys.argv[-1]
        if re.search(r"^from multiprocessing.* import main.*", cmd):
            exec(cmd)
            sys.exit()
    # workaround for python docs: run the freeze_support to avoid infinite loop
    from multiprocessing.spawn import freeze_support as spawn_freeze_support
    spawn_freeze_support()
    del spawn_freeze_support
    # disable it, cannot run twice
    freeze_support = lambda: None
    # cx_Freeze patch end
    """
    code_string = module.file.read_text(encoding="utf-8") + dedent(source)
    module.code = compile(code_string, os.fspath(module.file), "exec")
