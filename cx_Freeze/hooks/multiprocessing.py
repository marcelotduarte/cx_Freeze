"""A collection of functions which are triggered automatically by finder when
multiprocessing package is included.
"""

from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MINGW, IS_WINDOWS

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_multiprocessing(finder: ModuleFinder, module: Module) -> None:
    """The forkserver method calls utilspawnv_passfds in ensure_running to
    pass a command line to python. In cx_Freeze the running executable
    is called, then we need to catch this and use exec function.
    For the spawn method there are a similar process to resource_tracker.

    Note: Using multiprocessing.spawn.freeze_support directly because it works
    for all OS, not only Windows.
    """
    # Support for:
    # - fork in Unix (including macOS) is native;
    # - spawn in Windows is native since 4.3.4, but was improved in 6.2;
    # - spawn and forkserver in Unix is implemented here in 6.15.4 #1956;
    # - monkeypath get_context to do automatic freeze_support in 7.1 #2382;
    if IS_MINGW or IS_WINDOWS:
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
    # workaround: inject freeze_support call to avoid an infinite loop
    from multiprocessing.spawn import freeze_support as _spawn_freeze_support
    from multiprocessing.context import BaseContext
    BaseContext._get_context = BaseContext.get_context
    def _get_freeze_context(self, method=None):
        ctx = self._get_context(method)
        _spawn_freeze_support()
        return ctx
    BaseContext.get_context = \
        lambda self, method=None: _get_freeze_context(self, method)
    # disable freeze_support, because it cannot be run twice
    BaseContext.freeze_support = lambda self: None
    # cx_Freeze patch end
    """
    code_string = module.file.read_text(encoding="utf_8") + dedent(source)
    module.code = compile(
        code_string,
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )


def load_multiprocessing_connection(_, module: Module) -> None:
    """Ignore modules not found in current OS."""
    if not IS_MINGW and not IS_WINDOWS:
        module.exclude_names.update({"_winapi"})
    module.ignore_names.update(
        {
            "multiprocessing.AuthenticationError",
            "multiprocessing.BufferTooShort",
        }
    )


def load_multiprocessing_heap(_, module: Module) -> None:
    """Ignore modules not found in current OS."""
    if not IS_MINGW and not IS_WINDOWS:
        module.exclude_names.add("_winapi")


def load_multiprocessing_managers(_, module: Module) -> None:
    """Ignore modules not found in current os."""
    module.ignore_names.add("multiprocessing.get_context")


def load_multiprocessing_pool(_, module: Module) -> None:
    """Ignore modules not found in current os."""
    module.ignore_names.update(
        {"multiprocessing.TimeoutError", "multiprocessing.get_context"}
    )


def load_multiprocessing_popen_spawn_win32(_, module: Module) -> None:
    """Ignore modules not found in current OS."""
    if not IS_MINGW and not IS_WINDOWS:
        module.exclude_names.update({"msvcrt", "_winapi"})


def load_multiprocessing_reduction(_, module: Module) -> None:
    """Ignore modules not found in current OS."""
    if not IS_MINGW and not IS_WINDOWS:
        module.exclude_names.add("_winapi")


def load_multiprocessing_resource_tracker(_, module: Module) -> None:
    """Ignore modules not found in current OS."""
    if IS_MINGW or IS_WINDOWS:
        module.exclude_names.add("_posixshmem")


def load_multiprocessing_sharedctypes(_, module: Module) -> None:
    """Ignore modules not found in current os."""
    module.ignore_names.add("multiprocessing.get_context")


def load_multiprocessing_shared_memory(_, module: Module) -> None:
    """Ignore modules not found in current OS."""
    if not IS_MINGW and not IS_WINDOWS:
        module.exclude_names.add("_winapi")
    else:
        module.exclude_names.add("_posixshmem")


def load_multiprocessing_spawn(_, module: Module) -> None:
    """Ignore modules not found in current OS."""
    if not IS_MINGW and not IS_WINDOWS:
        module.exclude_names.update({"msvcrt", "_winapi"})
    module.ignore_names.update(
        {
            "multiprocessing.get_start_method",
            "multiprocessing.set_start_method",
        }
    )


def load_multiprocessing_util(_, module: Module) -> None:
    """The module uses test for tests and shouldn't be imported."""
    module.exclude_names.add("test")
    if IS_MINGW or IS_WINDOWS:
        module.exclude_names.add("_posixsubprocess")
