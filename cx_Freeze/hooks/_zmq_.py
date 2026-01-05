"""A collection of functions which are triggered automatically by finder when
zmq package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MINGW, IS_WINDOWS
from cx_Freeze.hooks.global_names import ZMQ_BACKEND_GLOBAL_NAMES
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for zmq."""

    def zmq(self, finder: ModuleFinder, module: Module) -> None:
        """The zmq package links dynamically to zmq.libzmq or shared lib.
        Tested pyzmq 16.0.4 to 27.0.0.
        """
        # Globals
        module.global_names.update(
            ["EAGAIN", "ETERM", "ZMQError", "zmq_version", "zmq_version_info"]
        )

        # Shared libraries can be found automatically when metadata is correct
        module.update_distribution("pyzmq")

        # Excludes
        finder.exclude_module("zmq.tests")
        try:
            finder.include_module("gevent")
        except ImportError:
            finder.exclude_module("zmq.green")
        try:
            finder.include_module("tornado")
        except ImportError:
            finder.exclude_module("zmq.eventloop")

        # Include the bundled libzmq library, if it exists
        with suppress(ImportError):
            finder.include_module("zmq.libzmq")

    def zmq_backend(self, finder: ModuleFinder, module: Module) -> None:
        """Load the backend dynamically."""
        module.global_names.update(ZMQ_BACKEND_GLOBAL_NAMES)
        try:
            finder.include_module("zmq.backend.cython._zmq")
            finder.exclude_module("zmq.backend.cffi")
        except ImportError:
            finder.include_package("zmq.backend.cffi")
            finder.exclude_module("zmq.backend.cython")

    def zmq_sugar_context(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore imports."""
        module.ignore_names.add("pyczmq")

    def zmq_utils_interop(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore imports."""
        module.ignore_names.add("cffi")

    def zmq_utils_win32(self, _finder: ModuleFinder, module: Module) -> None:
        """Filter imports."""
        if not (IS_MINGW or IS_WINDOWS):
            module.exclude_names.update(["ctypes", "ctypes.wintypes"])
