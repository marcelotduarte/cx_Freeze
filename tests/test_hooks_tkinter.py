"""Tests for cx_Freeze.hooks.tkinter."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX, IS_MACOS

if TYPE_CHECKING:
    from pathlib import Path

try:
    import tkinter as tk  # noqa: F401
except ImportError:
    pytest.skip(reason="Tkinter must be installed", allow_module_level=True)

SOURCE = """
test_tk.py
    import tkinter

    root = tkinter.Tk(useTk=False)
    print(root.tk.exprstring("$tcl_library"))
pyproject.toml
    [project]
    name = "hello"
    version = "0.1.2.3"

    [tool.cxfreeze]
    executables = ["test_tk.py"]
command
    cxfreeze build_exe
"""


def test_tkinter(tmp_path: Path) -> None:
    """Test if tkinter hook is working correctly."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path)
    executable = tmp_path / BUILD_EXE_DIR / f"test_tk{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    # Compare the start of the returned path, version independent.
    # This is necessary when the OS has an older tcl/tk version than the
    # version contained in the cx_Freeze wheels.
    expected = os.path.normpath(executable.parent / "share/tcl")
    assert output.splitlines()[0].startswith(expected)


@pytest.mark.skipif(not IS_MACOS, reason="macOS test")
def test_tkinter_bdist_mac(tmp_path: Path) -> None:
    """Test if tkinter hook is working correctly using bdist_mac."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path, "cxfreeze bdist_mac")
    name = "hello"
    version = "0.1.2.3"
    bundle_name = f"{name}-{version}"
    build_app_dir = tmp_path / "build" / f"{bundle_name}.app"
    executable = build_app_dir / f"Contents/MacOS/test_tk{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    # Compare the start of the returned path, version independent.
    # This is necessary when the OS has an older tcl/tk version than the
    # version contained in the cx_Freeze wheels.
    expected = os.path.normpath(build_app_dir / "Contents/Resources/share/tcl")
    assert output.splitlines()[0].startswith(expected)
