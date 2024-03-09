"""A collection of functions which are triggered automatically by finder when
torchvision package is included.
"""

from __future__ import annotations

from cx_Freeze.finder import ModuleFinder
from cx_Freeze.module import Module


def load_torchvision_models(finder: ModuleFinder, module: Module) -> None:
    """Hook for torchvision."""
    source_path = module.file.parent
    for source in source_path.rglob("*.py"):  # type: Path
        target = "lib" / source.relative_to(source_path)
        finder.include_files(source, target)
