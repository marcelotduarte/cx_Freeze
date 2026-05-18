"""A collection of functions which are triggered automatically by finder when
lazy-loader package is included.
"""

from __future__ import annotations

from importlib.machinery import SourceFileLoader
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]

ATTACH_STUB = """
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
        dist = module.distribution
        if dist and (int(dist.version[0]), int(dist.version[1])) < (0, 2):
            msg = "To support cx_Freeze, upgrade 'lazy-loader>=0.2'."
            raise SystemExit(msg)

        # add support to work with zip files
        loader = module.loader
        if not isinstance(loader, SourceFileLoader):
            return
        source_code = loader.get_source(module.name)
        if source_code:
            source_code = source_code.replace(
                "def attach_stub(", "def _attach_stub("
            )
            path = loader.get_filename(module.name)
            module.code = loader.source_to_code(
                source_code + ATTACH_STUB, path, _optimize=finder.optimize
            )
