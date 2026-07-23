"""Hooks triggered by finder when rtree package is included."""

from __future__ import annotations

import os
from importlib.machinery import SourceFileLoader
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for rtree."""

    def rtree_finder(self, finder: ModuleFinder, module: Module) -> None:
        spatialindex = None
        for source, target in finder.lib_files.items():
            if source.name.startswith(("spatialindex", "libspatialindex")):
                finder.include_files(source, target)
                spatialindex = os.path.normpath(target)
                break
        if spatialindex is None:
            return

        loader = module.loader
        if not isinstance(loader, SourceFileLoader):
            return
        source_code = loader.get_source(module.name)
        if source_code is None:
            return
        source_code = source_code.replace(
            "_candidates = []", f"_candidates = [_sys_prefix/{spatialindex!r}]"
        )
        module.code = loader.source_to_code(
            source_code,
            loader.get_filename(module.name),
            _optimize=finder.optimize,
        )
