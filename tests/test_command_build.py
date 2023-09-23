"""Tests for cx_Freeze.command.build."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from subprocess import check_output
from sysconfig import get_platform, get_python_version

import pytest

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"
FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "simple")
def test_build(datafiles: Path):
    """Test the simple sample."""
    output = check_output(
        [sys.executable, "setup.py", "build"],
        text=True,
        cwd=os.fspath(datafiles),
    )
    print(output)
    suffix = ".exe" if sys.platform == "win32" else ""
    file_created = datafiles / BUILD_EXE_DIR / f"hello{suffix}"
    assert file_created.is_file()
