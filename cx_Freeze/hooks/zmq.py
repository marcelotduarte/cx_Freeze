"""A collection of functions which are triggered automatically by finder when
zmq package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MINGW, IS_WINDOWS

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_zmq(finder: ModuleFinder, module: Module) -> None:
    """The zmq package links dynamically to zmq.libzmq or shared lib.
    Tested pyzmq 16.0.4 to 26.2.0.
    """
    # Globals
    module.global_names.update(
        ["EAGAIN", "ETERM", "ZMQError", "zmq_version", "zmq_version_info"]
    )

    # Include the bundled libzmq library, if it exists
    with suppress(ImportError):
        finder.include_module("zmq.libzmq")

    # Shared libraries
    source_dir = module.file.parent.parent / "pyzmq.libs"
    if source_dir.exists():  # pyzmq >= 22
        target_dir = f"lib/{source_dir.name}"
        for source in source_dir.iterdir():
            finder.lib_files[source] = f"{target_dir}/{source.name}"

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


def load_zmq_backend(finder: ModuleFinder, module: Module) -> None:
    """Load the backend dynamically."""
    module.global_names.update(
        [
            "Context",
            "Frame",
            "Socket",
            "strerror",
            "zmq_errno",
            "zmq_poll",
            "zmq_version_info",
        ]
    )
    try:
        finder.include_module("zmq.backend.cython._zmq")
        finder.exclude_module("zmq.backend.cffi")
    except ImportError:
        finder.include_package("zmq.backend.cffi")
        finder.exclude_module("zmq.backend.cython")


def load_zmq_sugar_context(_, module: Module) -> None:
    """Ignore imports."""
    module.ignore_names.add("pyczmq")


def load_zmq_utils_interop(_, module: Module) -> None:
    """Ignore imports."""
    module.ignore_names.add("cffi")


def load_zmq_utils_win32(_, module: Module) -> None:
    """Filter imports."""
    if not (IS_MINGW or IS_WINDOWS):
        module.exclude_names.update(["ctypes", "ctypes.wintypes"])


def load_zmq__typing(_, module: Module) -> None:
    """Filter imports."""
    module.exclude_names.add("typing_extensions")
