"""A collection of functions which are triggered automatically by finder when
lazy-loader package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]

ATTACH_STUB = b"""
def attach_stub(package_name: str, filename: str):
    exc_reraise = None
    try:
        return _attach_stub(package_name, filename)
    except ValueError as exc:
        exc_reraise = exc
    import importlib.resources, sys, os
    try:
        for path in sys.path:
            if path.endswith(".zip"):
                filename = os.path.relpath(
                    filename,
                    os.path.join(path, package_name.replace(".", os.path.sep))
                )
                filename = os.path.splitext(filename)[0] + ".pyi"
                with importlib.resources.path(package_name, filename) as f:
                    return _attach_stub(package_name, os.fspath(f))
    except (FileNotFoundError, ValueError):
        pass
    raise exc_reraise
"""


class Hook(ModuleHook):
    """The Hook class for lazy-loader."""

    def lazy_loader(self, finder: ModuleFinder, module: Module) -> None:
        """Use lazy-loader package 0.2+ to work with .pyc files."""
        if module.distribution.version < (0, 2):
            msg = "To support cx_Freeze, upgrade 'lazy-loader>=0.2'."
            raise SystemExit(msg)

        # add support to work with zip files
        code_bytes = module.file.read_bytes()
        code_bytes = code_bytes.replace(
            b"def attach_stub(", b"def _attach_stub("
        )
        code_bytes += ATTACH_STUB
        module.code = compile(
            code_bytes,
            module.file.as_posix(),
            "exec",
            dont_inherit=True,
            optimize=finder.optimize,
        )
