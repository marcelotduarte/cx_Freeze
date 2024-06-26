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
    source = rf"""
    # cx_Freeze patch start
    import re as _re
    import sys as _sys
    if len(_sys.argv) >= 2 and _sys.argv[-2] == "-c":
        cmd = _sys.argv[-1]
        if _re.search(r"^from {module.name}.* import main.*", cmd):
            exec(cmd)
            _sys.exit()
    # workaround: inject freeze_support call to avoid an infinite loop
    from {module.name}.spawn import is_forking as _spawn_is_forking
    if _spawn_is_forking(_sys.argv):
        main_module = _sys.modules["__main__"]
        main_spec = main_module.__spec__
        main_code = main_spec.loader.get_code(main_spec.name)
        _names = main_code.co_names
        del main_module, main_spec, main_code
        if "freeze_support" not in _names:
            import BUILD_CONSTANTS as _contants
            _ignore = getattr(_contants, "ignore_freeze_support_message", 0)
            if not _ignore:
                print(
    '''
        An attempt has been made to start a new process before the
        current process has finished its bootstrapping phase.

        This probably means that you are not using fork to start your
        child processes and you have forgotten to use the proper idiom
        in the main module:

            if __name__ == "__main__":
                freeze_support()
                ...

        To fix this issue, or to hide this message, refer to the documentation:
            \
    https://cx-freeze.readthedocs.io/en/stable/faq.html#multiprocessing-support
    ''', file=_sys.stderr)
            #import os, signal
            #os.kill(os.getppid(), signal.SIGHUP)
            #_sys.exit(os.EX_SOFTWARE)
            from {module.name}.spawn import freeze_support as _freeze_support
            _freeze_support()
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


def load_multiprocessing_context(finder: ModuleFinder, module: Module) -> None:
    """Monkeypath get_context to do automatic freeze_support."""
    if IS_MINGW or IS_WINDOWS:
        return
    if module.file.suffix == ".pyc":  # source unavailable
        return
    source = rf"""
    # cx_Freeze patch start
    def _freeze_support(self):
        from {module.root.name}.spawn import freeze_support
        freeze_support()
    BaseContext.freeze_support = _freeze_support
    BaseContext._get_base_context = BaseContext.get_context
    def _get_base_context(self, method=None):
        self.freeze_support()
        return self._get_base_context(method)
    BaseContext.get_context = _get_base_context
    DefaultContext._get_default_context = DefaultContext.get_context
    def _get_default_context(self, method=None):
        self.freeze_support()
        return self._get_default_context(method)
    DefaultContext.get_context = _get_default_context
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
        module.exclude_names.add("_winapi")
    module.ignore_names.update(
        {
            f"{module.root.name}.AuthenticationError",
            f"{module.root.name}.BufferTooShort",
        }
    )


def load_multiprocessing_heap(_, module: Module) -> None:
    """Ignore modules not found in current OS."""
    if not IS_MINGW and not IS_WINDOWS:
        module.exclude_names.add("_winapi")


def load_multiprocessing_managers(_, module: Module) -> None:
    """Ignore modules not found in current os."""
    module.ignore_names.add(f"{module.root.name}.get_context")


def load_multiprocessing_pool(_, module: Module) -> None:
    """Ignore modules not found in current os."""
    module.ignore_names.update(
        {f"{module.root.name}.TimeoutError", f"{module.root.name}.get_context"}
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
    module.ignore_names.add(f"{module.root.name}.get_context")


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
            f"{module.root.name}.get_start_method",
            f"{module.root.name}.set_start_method",
        }
    )


def load_multiprocessing_synchronize(_, module: Module) -> None:
    """Ignore modules not found in current OS."""
    module.ignore_names.update(
        {f"_{module.root.name}.SemLock", f"_{module.root.name}.sem_unlink"}
    )


def load_multiprocessing_util(_, module: Module) -> None:
    """The module uses test for tests and shouldn't be imported."""
    module.exclude_names.add("test")
    if IS_MINGW or IS_WINDOWS:
        module.exclude_names.add("_posixsubprocess")
