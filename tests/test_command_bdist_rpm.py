"""Tests for cx_Freeze.command.bdist_rpm."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from sysconfig import get_platform

import pytest

from cx_Freeze.sandbox import run_setup

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.skipif(sys.platform != "linux", reason="Linux tests")
@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "bcrypt")
def test_bdist_rpm(datafiles: Path):
    """Test the bcrypt sample with bdist_rpm."""
    if not shutil.which("rpmbuild"):
        pytest.xfail("rpmbuild not installed")

    package = "bcrypt"
    version = "0.3"
    arch = get_platform().split("-", 1)[1]
    dist_created = datafiles / "dist"

    run_setup(datafiles / "setup.py", ["bdist_rpm"])

    base_name = f"test_{package}-{version}"

    file_created = dist_created / f"{base_name}-1.src.rpm"
    assert file_created.is_file()

    file_created = dist_created / f"{base_name}-1.{arch}.rpm"
    assert file_created.is_file()

    file_created = dist_created / f"{base_name}.tar.gz"
    assert file_created.is_file()
