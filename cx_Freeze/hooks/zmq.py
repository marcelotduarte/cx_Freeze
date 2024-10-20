"""A collection of functions which are triggered automatically by finder when
zmq package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_zmq(finder: ModuleFinder, module: Module) -> None:
    """The zmq package loads zmq.backend.cython dynamically and links
    dynamically to zmq.libzmq or shared lib. Tested pyzmq 16.0.4 to 26.2.0.
    """
    source_dir = module.file.parent.parent / "pyzmq.libs"
    if source_dir.exists():  # pyzmq >= 22
        target_dir = f"lib/{source_dir.name}"
        for source in source_dir.iterdir():
            finder.lib_files[source] = f"{target_dir}/{source.name}"

    finder.include_package("zmq.backend.cython")
    # Include the bundled libzmq library, if it exists
    with suppress(ImportError):
        finder.include_module("zmq.libzmq")
    finder.exclude_module("zmq.tests")
    # globals
    module.global_names.update(
        ["EAGAIN", "ETERM", "ZMQError", "zmq_version", "zmq_version_info"]
    )


def load_zmq_backend(_, module: Module) -> None:
    """Add global variables."""
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


def load_zmq_sugar_context(_, module: Module) -> None:
    """Ignore imports."""
    module.ignore_names.add("pyczmq")


def load_zmq_utils_interop(_, module: Module) -> None:
    """Ignore imports."""
    module.ignore_names.add("cffi")
