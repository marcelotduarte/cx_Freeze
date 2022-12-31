"""Tests for cx_Freeze.command.build."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from sysconfig import get_platform, get_python_version

from cx_Freeze.sandbox import run_setup

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"


def test_build(fix_main_samples_path: Path):
    """Test the simple sample."""

    setup_path = fix_main_samples_path / "simple"
    dist_created = setup_path / BUILD_EXE_DIR
    dist_already_exists = dist_created.exists()

    run_setup(setup_path / "setup.py", ["build"])

    suffix = ".exe" if sys.platform == "win32" else ""
    file_created = dist_created / f"hello{suffix}"
    assert file_created.is_file()
    file_created.unlink()

    if not dist_already_exists:
        shutil.rmtree(dist_created, ignore_errors=True)
