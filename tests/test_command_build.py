"""Tests for cx_Freeze.command.build."""
from __future__ import annotations

import sys
from pathlib import Path
from sysconfig import get_platform, get_python_version

import pytest
from generate_samples import run_command

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"
IS_WINDOWS = sys.platform == "win32"
SUFFIX = ".exe" if IS_WINDOWS else ""


@pytest.mark.datafiles(SAMPLES_DIR / "simple")
def test_build(datafiles: Path):
    """Test the simple sample."""
    run_command(datafiles)
    file_created = datafiles / BUILD_EXE_DIR / f"hello{SUFFIX}"
    assert file_created.is_file()
