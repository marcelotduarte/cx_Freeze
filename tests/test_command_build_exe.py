"""Tests for cx_Freeze.command.build_exe."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from sysconfig import get_platform, get_python_version

import pytest

from cx_Freeze.sandbox import run_setup

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"
FIXTURE_DIR = Path(__file__).resolve().parent

OUTPUT1 = "Hello from cx_Freeze Advanced #1\nTest freeze module #1\n"
OUTPUT2 = "Hello from cx_Freeze Advanced #2\nTest freeze module #2\n"


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "advanced")
def test_build_exe_advanced(datafiles: Path):
    """Test the advanced sample."""
    run_setup(
        datafiles / "setup.py", ["build_exe", "--silent", "--excludes=tkinter"]
    )
    suffix = ".exe" if sys.platform == "win32" else ""

    executable = datafiles / BUILD_EXE_DIR / f"advanced_1{suffix}"
    assert executable.is_file()
    output = subprocess.check_output(
        [os.fspath(executable)], text=True, timeout=10
    )
    assert output == OUTPUT1

    executable = datafiles / BUILD_EXE_DIR / f"advanced_2{suffix}"
    assert executable.is_file()
    output = subprocess.check_output(
        [os.fspath(executable)], text=True, timeout=10
    )
    assert output == OUTPUT2


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "asmodule")
def test_build_exe_asmodule(datafiles: Path):
    """Test the asmodule sample."""
    run_setup(
        datafiles / "setup.py", ["build_exe", "--silent", "--excludes=tkinter"]
    )
    suffix = ".exe" if sys.platform == "win32" else ""
    executable = datafiles / BUILD_EXE_DIR / f"asmodule{suffix}"
    assert executable.is_file()
    output = subprocess.check_output(
        [os.fspath(executable)], text=True, timeout=10
    )
    assert output.startswith("Hello from cx_Freeze")


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "simple")
def test_build_exe_simple(datafiles: Path):
    """Test the simple sample."""
    run_setup(
        datafiles / "setup.py", ["build_exe", "--silent", "--excludes=tkinter"]
    )
    suffix = ".exe" if sys.platform == "win32" else ""
    executable = datafiles / BUILD_EXE_DIR / f"hello{suffix}"
    assert executable.is_file()
    output = subprocess.check_output(
        [os.fspath(executable)], text=True, timeout=10
    )
    assert output.startswith("Hello from cx_Freeze")


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "sqlite")
def test_build_exe_sqlite(datafiles: Path):
    """Test the sqlite sample."""
    run_setup(
        datafiles / "setup.py", ["build_exe", "--silent", "--excludes=tkinter"]
    )
    suffix = ".exe" if sys.platform == "win32" else ""
    executable = datafiles / BUILD_EXE_DIR / f"test_sqlite3{suffix}"
    assert executable.is_file()
    output = subprocess.check_output(
        [os.fspath(executable)], text=True, timeout=10
    )
    assert output.startswith("dump.sql created")
