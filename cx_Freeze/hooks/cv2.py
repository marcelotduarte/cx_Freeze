"""A collection of functions which are triggered automatically by finder when
opencv-python package is included."""

import sys
from pathlib import Path

from ..finder import ModuleFinder
from ..module import Module

DARWIN = sys.platform == "darwin"
WIN32 = sys.platform == "win32"


def load_cv2(finder: ModuleFinder, module: Module) -> None:
    """Versions of cv2 (opencv-python) above 4.5.3 require additional
    configuration files.

    Additionally, on Linux the opencv_python.libs directory is not
    copied across for versions above 4.5.3."""
    finder.include_package("cv2")
    finder.include_package("numpy")
    module.update_distribution("opencv-python")

    target_dir = Path("lib", "cv2")
    if module.path is None:
        # conda-forge: cv2 is a extension module
        source = Path(sys.base_prefix, "plugins", "platforms")
        if source.is_dir():
            finder.include_files(source, target_dir / "plugins" / "platforms")
        source = Path(sys.base_prefix, "fonts")
        if source.is_dir():
            finder.include_files(source, target_dir / "fonts")
        # pylint: disable-next=protected-access
        source_qt_conf = module.distribution._cachedir.path / "qt.conf"
        with open(source_qt_conf, "w", encoding="utf-8") as configfile:
            configfile.write("[Paths]\n")
            configfile.write(f"Prefix = {target_dir.as_posix()}\n")
            if DARWIN:
                target_qt_conf = "Contents/Resources/qt.conf"
            else:
                target_qt_conf = source_qt_conf.name
            finder.include_files(source_qt_conf, target_qt_conf)
        return

    source_dir = module.path[0]
    for path in source_dir.glob("config*.py"):
        finder.include_files(path, target_dir / path.name)
    module.in_file_system = 1

    # Copy all files in site-packages/opencv_python.libs
    if WIN32:
        return
    if DARWIN:
        libs_name = "cv2/.dylibs"
    else:  # Linux and others
        libs_name = "opencv_python.libs"
    libs_dir = source_dir.parent / libs_name
    if libs_dir.exists():
        finder.include_files(libs_dir, target_dir.parent / libs_name)
