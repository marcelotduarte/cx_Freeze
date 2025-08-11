"""Tests for hooks for qt."""

from __future__ import annotations

import pytest

from cx_Freeze._compat import IS_CONDA, IS_MACOS, IS_MINGW, IS_WINDOWS

TIMEOUT = 10

QT_IMPLS = []
for qt_impl in ("PyQt6", "PySide6", "PyQt5", "PySide2"):
    try:
        __import__(qt_impl)
        QT_IMPLS.append(qt_impl)
    except ImportError:
        pass


SOURCE_QT = """
test_qt.py
    from %(qt_mod)s.QtCore import QTimer
    from %(qt_mod)s.QtWidgets import QApplication, QLabel

    app = QApplication([])
    label = QLabel('Hello from Qt!')
    label.show()
    timer = QTimer()

    def quit():
        print(label.text())
        app.quit()

    timer.start(500)
    timer.timeout.connect(quit)
    app.exec()

pyproject.toml
    [project]
    name = "test_qt"
    version = "0.1.2.3"
    dependencies = ["%(qt_dep)s"]

    [tool.cxfreeze]
    executables = ["test_qt.py"]

    [tool.cxfreeze.build_exe]
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


@pytest.mark.venv
@pytest.mark.skipif(not QT_IMPLS, reason="No Qt libraries installed")
@pytest.mark.parametrize("qt_impl", QT_IMPLS)
def test_qt(tmp_package, qt_impl) -> None:
    """Test if anyio is working correctly."""
    tmp_package.create(
        SOURCE_QT
        % {
            "qt_mod": qt_impl,
            "qt_dep": qt_impl.lower().rstrip("456") if IS_CONDA else qt_impl,
        }
    )
    tmp_package.freeze()

    # Test frozen app
    executable = tmp_package.executable("test_qt")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(["Hello from Qt!"])

    # Check for duplicate libs
    duplicate_libs = find_duplicates_libs(executable.parent / "lib")
    assert not duplicate_libs
