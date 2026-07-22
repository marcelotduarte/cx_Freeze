"""Tests for hooks for qt."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, cast

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

if TYPE_CHECKING:
    from pathlib import Path

    from tests.conftest import TempPackage

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
    include-msvcr = true
    excludes = ["tkinter"]
    silent = true
"""


def find_duplicates_libs(build_lib_dir: Path) -> dict[str, list[str]]:
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
    ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="Qt does not support Python 3.14t",
    strict=True,
)
@pytest.mark.venv
@pytest.mark.parametrize("qt_impl", ["PyQt6", "PySide6", "PyQt5", "PySide2"])
def test_qt(tmp_package: TempPackage, qt_impl: str) -> None:
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
        if qt_impl in ("PyQt6", "PySide6") and IS_LINUX:
            from platform import libc_ver  # noqa: PLC0415

            version_raw = libc_ver()
            version = tuple(map(int, version_raw[1].split(".")))
            if version < (2, 28):
                pytest.skip(
                    f"{qt_impl} requires glibc>=2.28, "
                    f"found {version_raw[0]} {version_raw[1]}"
                )

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

    # Freeze the app and check if it is created
    tmp_package.create(SOURCE_QT % {"qt_mod": qt_impl})
    result_freeze = tmp_package.freeze()
    try:
        missing = cast(
            "list[str]",
            result_freeze.stdout.get_lines_after("Missing dependencies:"),
        )
    except ValueError:
        missing = None
    executable = tmp_package.executable("test_qt")
    assert executable.is_file()

    # Check for duplicate libs
    duplicate_libs = find_duplicates_libs(executable.parent / "lib")
    assert not duplicate_libs

    # xfail on Linux in the CI or docker or podman, because of missing xcb libs
    result = tmp_package.run(executable, timeout=TIMEOUT)
    if result.ret != 0 and IS_LINUX and missing:
        for i, m in enumerate(missing):
            missing[i] = m.replace("? ", "")
        missing.pop()
        missing.pop()
        pytest.xfail("Missing dependencies: " + ", ".join(missing))
    result.stdout.fnmatch_lines(["Hello from Qt!"])
