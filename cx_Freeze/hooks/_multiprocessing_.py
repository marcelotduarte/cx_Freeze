"""A collection of functions which are triggered automatically by finder when
multiprocessing package is included.
"""

from __future__ import annotations

import sys
from importlib.machinery import SourceFileLoader
from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MINGW, IS_WINDOWS
from cx_Freeze.hooks.global_names import MULTIPROCESSING_GLOBAL_NAMES
from cx_Freeze.module import ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module

__all__ = ["Hook"]

# Notes:
# - fork in Unix (including macOS) is native
# - spawn in Windows is native since 4.3.4, but was improved in v6.2
# - spawn and forkserver in Unix is implemented (v6.15.4 #1956)
# - monkeypatch context to do automatic freeze_support (v7.1 #2382)
# - monkeypatch context to fix bug introduced in Python 3.13.4 (v8.4 #3009)
#   and solved in Python 3.14.4 (v8.6.4 #3298)
# - gh-144503 "Pass sys.argv to forkserver as real argv elements" changed the
#   command line passed to spawned process, in Python 3.14.4 (v8.6.4 #3299)

FREEZE_SUPPORT_MESSAGE = """
    An attempt has been made to start a new process before the
    current process has finished its bootstrapping phase.

    This probably means that you are not using fork to start your
    child processes and you have forgotten to use the proper idiom
    in the main module:

        if __name__ == "__main__":
            freeze_support()
            ...

    To fix this issue (hide this message), refer to the documentation:
        \
https://cx-freeze.readthedocs.io/en/stable/faq.html#multiprocessing-support
"""


class Hook(ModuleHook):
    """The Module Hook class."""

    def multiprocessing(self, finder: ModuleFinder, module: Module) -> None:
        """The forkserver method calls utilspawnv_passfds in ensure_running to
        pass a command line to python. In cx_Freeze the running executable
        is called, then we need to catch this and use exec function.
        For the spawn method there are a similar process to resource_tracker.

        Note: Using multiprocessing.spawn.freeze_support directly because it
        works for all OS, not only Windows.
        """
        # Ignore names that should not be confused with modules to be imported
        module.global_names.update(MULTIPROCESSING_GLOBAL_NAMES)

        if IS_MINGW or IS_WINDOWS:
            return
        if not isinstance(module.loader, SourceFileLoader):
            return
        patch = rf"""
        # cx_Freeze patch start
        import re as _re
        import sys as _sys
        if len(_sys.argv) >= 2 and "-c" in _sys.argv:
            _idx = _sys.argv.index("-c")
            _cmd = _sys.argv[_idx + 1]
            if _re.search(r"from {module.name}.* import main.*", _cmd):
                exec(_cmd)
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
                import BUILD_CONSTANTS as _constants
                _ignore = getattr(
                    _constants, "ignore_freeze_support_message", 0
                )
                if not _ignore:
                    print({FREEZE_SUPPORT_MESSAGE!r}, file=_sys.stderr)
                #import os, signal
                #os.kill(os.getppid(), signal.SIGHUP)
                #_sys.exit(os.EX_SOFTWARE)
                from {module.name}.spawn import \
                    freeze_support as _freeze_support
                _freeze_support()
        # cx_Freeze patch end
        """
        loader = module.loader
        path = loader.get_filename(module.name)
        source_code = loader.get_source(module.name)
        module.code = loader.source_to_code(
            source_code + dedent(patch), path, _optimize=finder.optimize
        )

    def multiprocessing_context(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        """Monkeypath context to do automatic freeze_support on Unix-like.

        For Windows, add a workaround for a bug introduced by gh-80334 in
        Python 3.13.4, which was fixed by gh-135726 in Python 3.14.4.
        """
        if not isinstance(module.loader, SourceFileLoader):
            return
        if IS_MINGW or IS_WINDOWS:
            PY_313_BUGGED = (3, 13, 4) <= sys.version_info[:3] <= (3, 13, 12)
            PY_314_BUGGED = (3, 14, 0) <= sys.version_info[:3] <= (3, 14, 3)
            if PY_313_BUGGED or PY_314_BUGGED:
                patch = rf"""
                # cx_Freeze patch start
                def _freeze_support(self):
                    from {module.root.name}.spawn import freeze_support
                    freeze_support()
                BaseContext.freeze_support = _freeze_support
                # cx_Freeze patch end
                """
            else:
                return
        else:
            patch = rf"""
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
        loader = module.loader
        path = loader.get_filename(module.name)
        source_code = loader.get_source(module.name)
        module.code = loader.source_to_code(
            source_code + dedent(patch), path, _optimize=finder.optimize
        )

    def multiprocessing_synchronize(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        """Ignore modules not found in current OS."""
        module.ignore_names.update(
            {f"_{module.root.name}.SemLock", f"_{module.root.name}.sem_unlink"}
        )
