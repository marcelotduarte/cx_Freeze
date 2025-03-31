"""A collection of functions which are triggered automatically by finder when
torchvision package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_torchvision(finder: ModuleFinder, module: Module) -> None:
    """Hook for torchvision."""
    module_path = module.file.parent
    site_packages_path = module_path.parent

    source_dir = site_packages_path / f"{module.name}.libs"
    if source_dir.exists():
        target_dir = f"lib/{source_dir.name}"
        for source in source_dir.iterdir():
            finder.lib_files[source] = f"{target_dir}/{source.name}"

    # include source files that uses @torch.jit._overload_method
    for source in module_path.rglob("*.py"):  # type: Path
        if b"@torch.jit._overload_method" in source.read_bytes():
            target = "lib" / source.relative_to(site_packages_path)
            finder.include_files(source, target)
