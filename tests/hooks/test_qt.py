"""Tests for hooks for qt."""

from __future__ import annotations

import os
import sys

import pytest

from cx_Freeze._compat import (
    ABI_THREAD,
    IS_ARM_64,
    IS_CONDA,
    IS_LINUX,
    IS_MACOS,
    IS_MINGW,
    IS_WINDOWS,
)

TIMEOUT = 15

SOURCE_QT = """
test_qt.py
    from %(qt_mod)s.QtCore import QTimer
    from %(qt_mod)s.QtWidgets import QApplication, QLabel

    app = QApplication([])
    label = QLabel("Hello from Qt!")
    label.show()
    timer = QTimer()

    def quit():
        print(label.text())
        app.quit()

    timer.start(500)
    timer.timeout.connect(quit)
    if hasattr(app, "exec"):
        app.exec()
    else:
        app.exec_()

pyproject.toml
    [project]
    name = "test_qt"
    version = "0.1.2.3"
    dependencies = ["%(qt_mod)s"]

    [tool.cxfreeze]
    executables = ["test_qt.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


def find_duplicates_libs(build_lib_dir) -> dict[str, list[str]]:
    """Look for any duplicate libs files in the build lib dir."""
    if IS_MINGW or IS_WINDOWS:
        extension = "*.dll"
    elif IS_MACOS:
        extension = "*.dylib"
    else:
        extension = "*.so*"
    libs = {}
    for p in build_lib_dir.glob(f"**/{extension}"):
        if p.name not in libs:
            libs[p.name] = []
        libs[p.name].append(str(p.relative_to(build_lib_dir)))
    return {k: v for k, v in libs.items() if len(v) > 1}


@pytest.mark.xfail(
    sys.version_info[:2] >= (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="Qt does not support Python 3.13t/3.14t",
    strict=True,
)
@pytest.mark.venv
@pytest.mark.parametrize("qt_impl", ["PyQt6", "PySide6", "PyQt5", "PySide2"])
def test_qt(tmp_package, qt_impl) -> None:
    """Test if qt is working correctly."""
    if IS_CONDA:
        if qt_impl == "PyQt6":
            pytest.skip(f"{qt_impl} not supported in conda")
        if qt_impl == "PySide2" and sys.version_info[:2] >= (3, 13):
            pytest.skip("PySide2 does not support Python 3.13+ on conda")
    else:
        if qt_impl == "PySide2":
            if IS_MACOS:
                pytest.skip("PySide2 does not support macOS")
            if not IS_MINGW and sys.version_info[:2] >= (3, 11):
                pytest.skip("PySide2 does not support Python 3.11+")
        if (
            qt_impl in ("PyQt5", "PySide2")
            and (IS_LINUX or IS_WINDOWS)
            and IS_ARM_64
        ):
            pytest.skip(f"{qt_impl} not supported in arm64")

    tmp_package.map_package_to_conda.update(
        {
            "PyQt5": "pyqt=5",
            "PySide2": "pyside2",
            "PySide6": "pyside6",
        }
    )
    tmp_package.map_package_to_mingw.update(
        {
            "PyQt5": "python-pyqt5",
            "PyQt6": "python-pyqt6",
            "PySide2": "pyside2",
            "PySide6": "pyside6",
        }
    )
    tmp_package.create(SOURCE_QT % {"qt_mod": qt_impl})
    tmp_package.freeze()

    # Test frozen app
    executable = tmp_package.executable("test_qt")
    assert executable.is_file()
    # Do not test in Linux using CI yet because of missing xcb libs
    # but we can compare duplicate libs
    if not (IS_LINUX and os.environ.get("CI")):
        result = tmp_package.run(executable, timeout=TIMEOUT)
        result.stdout.fnmatch_lines(["Hello from Qt!"])

    # Check for duplicate libs
    duplicate_libs = find_duplicates_libs(executable.parent / "lib")
    assert not duplicate_libs
