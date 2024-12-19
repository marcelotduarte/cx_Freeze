"""A collection of functions which are triggered automatically by finder when
opencv-python package is included.
"""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MACOS, IS_MINGW, IS_WINDOWS, PYTHON_VERSION

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module

WARNING_NUMPY_VERSION = """WARNING:

    {cv2_name} {cv2_version} isn't compatible with numpy {numpy_version}.
    To fix this issue, the easiest solution will be to
    downgrade to 'numpy<2' or try to upgrade {cv2_name}.
"""


def load_cv2(finder: ModuleFinder, module: Module) -> None:
    """Versions of cv2 (opencv-python) above 4.5.3 may require additional
    configuration files.

    Additionally, on Linux the opencv_python.libs directory is not
    copied across for versions above 4.5.3.
    """
    source_dir = module.file.parent
    target_dir = Path("lib", "cv2")

    if module.distribution is None:
        module.update_distribution("opencv-python")
    if module.distribution is None:
        module.update_distribution("opencv-python-headless")

    if module.distribution:
        name = module.distribution.normalized_name
        version = module.distribution.version
        if version[:2] < (4, 10):
            m_numpy = finder.include_package("numpy")
            if m_numpy.distribution and m_numpy.distribution.version[0] >= 2:
                msg = WARNING_NUMPY_VERSION.format(
                    cv2_name=module.distribution.name,
                    cv2_version=module.distribution.original.version,
                    numpy_version=m_numpy.distribution.original.version,
                )
                print(msg, file=sys.stderr)

        # cv2 4.9.0-4.10.0 conda-forge uses qt6-main
        if module.distribution.installer == "conda":
            if version[:2] >= (4, 9):
                source = Path(sys.base_prefix, "lib/qt6/plugins/platforms")
            else:
                source = Path(sys.base_prefix, "plugins/platforms")
            if source.is_dir():
                finder.include_files(
                    source, target_dir / "plugins" / "platforms"
                )
            source = Path(sys.base_prefix, "fonts")
            if source.is_dir():
                finder.include_files(source, target_dir / "fonts")
            qt_conf: Path = finder.cache_path / "qt.conf"
            lines = ["[Paths]", f"Prefix = {target_dir.as_posix()}"]
            with qt_conf.open(mode="w", encoding="utf_8", newline="") as file:
                file.write("\n".join(lines))
            finder.include_files(qt_conf, qt_conf.name)
            if IS_MACOS:
                finder.include_files(qt_conf, "Contents/Resources/qt.conf")
    else:
        name = "opencv_python"

    # msys2: cv2 4.6.0-4.9.0 is a extension module
    if IS_MINGW:
        finder.include_package("numpy")
        # msys2 files is on 'share' subdirectory
        source = Path(sys.base_prefix, "share/qt6/plugins/platforms")
        if source.is_dir():
            finder.include_files(source, target_dir / "plugins" / "platforms")
        source = Path(sys.base_prefix, "fonts")
        if not source.is_dir():
            source = Path(sys.base_prefix, "share/fonts")
        if source.is_dir():
            finder.include_files(source, target_dir / "fonts")
        qt_conf: Path = finder.cache_path / "qt.conf"
        lines = ["[Paths]", f"Prefix = {target_dir.as_posix()}"]
        with qt_conf.open(mode="w", encoding="utf_8", newline="") as file:
            file.write("\n".join(lines))
        finder.include_files(qt_conf, qt_conf.name)

    # conda-forge and msys2: cv2 4.6.0-4.9.0 is a extension module
    if module.path is None:
        return

    # Use optimized mode
    module.in_file_system = 2
    finder.exclude_module("cv2.config")
    finder.exclude_module("cv2.config-3")
    finder.exclude_module("cv2.load_config_py2")
    module.exclude_names.add("load_config_py2")
    finder.include_package("cv2")

    # Include config files and libraries
    # When opencv_contrib_python or opencv_contrib_python_headless is used
    # an optimization is possible, because cv2.abi3.so is changed and its
    # rpath points to it .libs directory
    source_config = finder.cache_path / "cv2-config.py"
    contrib = name.replace("opencv_python", "opencv_contrib_python")
    source_libs = source_dir.parent / f"{contrib}.libs"
    if not source_libs.exists():
        source_libs = source_dir.parent / f"{name}.libs"
    if source_libs.exists():
        # Linux wheels
        target_libs = f"lib/{source_libs.name}"
        for source in source_libs.iterdir():
            finder.lib_files[source] = f"{target_libs}/{source.name}"
        source_config.write_text(
            dedent(
                f"""\
                import os, sys
                BINARIES_PATHS = [
                    os.path.join(sys.frozen_dir, '{target_libs}')
                ] + BINARIES_PATHS
                """
            )
        )
    else:
        source_config.touch()

    # Include config-3 (Linux wheels) or create it for conda-forge
    finder.include_files(source_config, target_dir / "config.py")
    source_config = source_dir / "config-3.py"
    if not source_config.exists():
        # create config-3 for cv2 4.10.x conda-forge
        extension_dir = f"python-{PYTHON_VERSION}"
        finder.include_files(
            source_dir / extension_dir, target_dir / extension_dir
        )
        source_config = finder.cache_path / "cv2-config-3.py"
        source_config.touch()
        source_config.write_text(
            dedent(
                f"""\
                import os
                PYTHON_EXTENSIONS_PATHS = [
                    os.path.join(LOADER_DIR, '{extension_dir}')
                ] + PYTHON_EXTENSIONS_PATHS
                """
            )
        )
    finder.include_files(source_config, target_dir / "config-3.py")

    # Include data files
    data_dir = source_dir / "data"
    if data_dir.exists():
        for path in data_dir.glob("*.xml"):
            finder.include_files(path, target_dir / "data" / path.name)

    # Copy all binary files
    if IS_WINDOWS:
        for path in source_dir.glob("*.dll"):
            finder.include_files(path, target_dir / path.name)
        return

    if IS_MACOS:
        libs_dir = source_dir / ".dylibs"
        if libs_dir.exists():
            finder.include_files(libs_dir, target_dir / ".dylibs")
        return

    # Qt files distributed in wheels for Linux
    qt_files = source_dir / "qt"
    if qt_files.exists():
        finder.include_files(qt_files, target_dir / "qt")
