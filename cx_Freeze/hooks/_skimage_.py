"""A collection of functions which are triggered automatically by finder when
scikit-image package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MACOS

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_skimage(finder: ModuleFinder, module: Module) -> None:
    """Include the full skimage package, because of the heavy use of
    lazy_loader.
    """
    # Fix distribution
    if module.distribution is None:
        module.update_distribution("scikit_image")
    distribution = module.distribution

    # Exclude all tests
    if distribution:
        tests = set()
        for file in distribution.original.files:
            if file.parent.match("**/tests"):
                tests.add(file.parent.as_posix().replace("/", "."))
        for test in tests:
            finder.exclude_module(test)
    finder.exclude_module("skimage.conftest")

    # Include pillow plugin
    try:
        finder.include_module("PIL")
    except ImportError:
        pass
    else:
        finder.include_module("imageio.plugins.pillow")

    # [macos] copy dependent files when using zip_include_packages
    if IS_MACOS:
        source_dir = module.file.parent / ".dylibs"
        if source_dir.exists() and module.in_file_system == 0:
            finder.include_files(source_dir, "lib/.dylibs")

    # Include the full skimage package
    finder.include_package("skimage")
