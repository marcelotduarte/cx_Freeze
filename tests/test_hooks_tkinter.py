"""Tests for cx_Freeze.hooks.tkinter."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX, IS_MACOS

if TYPE_CHECKING:
    from pathlib import Path

tkinter = pytest.importorskip("tkinter", reason="Tkinter must be installed")

SOURCE = """
test_tkinter.py
    import tkinter

    root = tkinter.Tk(useTk=False)
    print(root.tk.exprstring("$tcl_library"))
command
    cxfreeze --script test_tkinter.py build_exe --silent
"""


def test_tkinter(tmp_path: Path) -> None:
    """Test if tkinter hook is working correctly."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path)
    executable = tmp_path / BUILD_EXE_DIR / f"test_tkinter{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    expected = executable.parent.joinpath(f"share/tcl{tkinter.TclVersion}")
    assert output.splitlines()[0] == os.path.normpath(expected)


@pytest.mark.skipif(not IS_MACOS, reason="macOS test")
def test_tkinter_bdist_mac(tmp_path: Path) -> None:
    """Test if tkinter hook is working correctly using bdist_mac."""
    create_package(tmp_path, SOURCE)
    output = run_command(
        tmp_path, "cxfreeze --script test_tkinter.py bdist_mac"
    )
    build_app_dir = next(tmp_path.joinpath("build").glob("*.app"))
    executable = build_app_dir / f"test_tkinter{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    expected = executable.parent.joinpath(f"share/tcl{tkinter.TclVersion}")
    assert output.splitlines()[0] == os.path.normpath(expected)
