"""A collection of functions which are triggered automatically by finder when
timm package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_timm(finder: ModuleFinder, module: Module) -> None:
    """Hook for timm. Tested in Windows and Linux."""
    module_path = module.file.parent
    site_packages_path = module_path.parent

    # Activate the optimized mode by default
    if module.name in finder.zip_exclude_packages:
        print(f"WARNING: {module.name} hook optimizations disabled.")
        module.in_file_system = 1
    elif module.name in finder.zip_include_packages:
        print(f"WARNING: {module.name} hook optimizations enabled.")
        module.in_file_system = 2
    else:
        module.in_file_system = 2

    # include source files using @torch.jit._overload_method
    for source in module_path.rglob("*.py"):  # type: Path
        if b"@torch.jit._overload_method" in source.read_bytes():
            target = "lib" / source.relative_to(site_packages_path)
            finder.include_files(source, target)
