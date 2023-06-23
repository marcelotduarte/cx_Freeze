"""Tests for cx_Freeze.command.build_exe."""

from __future__ import annotations

import sys
from pathlib import Path
from sysconfig import get_platform, get_python_version

import pytest

from cx_Freeze.sandbox import run_setup

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"
FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "simple")
def test_build_exe(datafiles: Path):
    """Test the simple sample."""
    run_setup(datafiles / "setup.py", ["build_exe", "--silent"])
    suffix = ".exe" if sys.platform == "win32" else ""
    file_created = datafiles / BUILD_EXE_DIR / f"hello{suffix}"
    assert file_created.is_file()
