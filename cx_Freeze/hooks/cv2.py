"""A collection of functions which are triggered automatically by finder when
opencv-python package is included.
"""

from __future__ import annotations

import sys
from pathlib import Path

from .._compat import IS_MACOS, IS_MINGW, IS_MINGW64, IS_WINDOWS
from ..common import TemporaryPath
from ..finder import ModuleFinder
from ..module import Module

temp_path = TemporaryPath()


def load_cv2(finder: ModuleFinder, module: Module) -> None:
    """Versions of cv2 (opencv-python) above 4.5.3 require additional
    configuration files.

    Additionally, on Linux the opencv_python.libs directory is not
    copied across for versions above 4.5.3.
    """
    finder.include_package("numpy")
    if module.distribution is None:
        module.update_distribution("opencv-python")

    source_dir = module.file.parent
    target_dir = Path("lib", "cv2")

    # conda-forge and msys2: cv2 4.6.0 is a extension module
    if module.path is None:
        # msys2 files is on 'share' subdirectory
        if IS_MINGW:
            if IS_MINGW64:
                source = Path(sys.base_prefix, "share/qt6/plugins/platforms")
            else:
                source = Path(sys.base_prefix, "share/qt5/plugins/platforms")
        else:
            source = Path(sys.base_prefix, "plugins/platforms")
        if source.is_dir():
            finder.include_files(source, target_dir / "plugins" / "platforms")
        source = Path(sys.base_prefix, "fonts")
        if not source.is_dir():
            source = Path(sys.base_prefix, "share/fonts")
        if source.is_dir():
            finder.include_files(source, target_dir / "fonts")
        qt_conf: Path = temp_path.path / "qt.conf"
        lines = ["[Paths]", f"Prefix = {target_dir.as_posix()}"]
        with qt_conf.open(mode="w", encoding="utf_8", newline="") as file:
            file.write("\n".join(lines))
        finder.include_files(qt_conf, qt_conf.name)
        if IS_MACOS:
            finder.include_files(qt_conf, "Contents/Resources/qt.conf")
        return

    # Use optmized mode
    module.in_file_system = 2
    finder.include_package("cv2")
    for path in source_dir.glob("config*.py"):
        finder.include_files(path, target_dir / path.name)
    data_dir = source_dir / "data"
    if data_dir.exists():
        finder.include_files(data_dir, target_dir / "data")

    # Copy all binary files
    if IS_WINDOWS:
        return

    if IS_MACOS:
        libs_dir = source_dir / ".dylibs"
        if libs_dir.exists():
            finder.include_files(libs_dir, "lib/cv2/.dylibs")
        return

    # Linux and others
    libs_name = "opencv_python.libs"
    libs_dir = source_dir.parent / libs_name
    if libs_dir.exists():
        finder.include_files(libs_dir, target_dir.parent / libs_name)
    qt_files = source_dir / "qt"
    if qt_files.exists():
        finder.include_files(qt_files, target_dir / "qt")
