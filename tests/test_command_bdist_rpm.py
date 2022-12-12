"""Tests for cx_Freeze.command.bdist_rpm."""

from __future__ import annotations

import sys
from pathlib import Path
from sysconfig import get_platform

import pytest

from cx_Freeze.sandbox import run_setup


@pytest.mark.skipif(sys.platform != "linux", reason="Linux tests")
def test_bdist_rpm(fix_main_samples_path: Path):
    """Test the bcrypt sample with bdist_rpm."""

    package = "bcrypt"
    version = "0.3"
    arch = get_platform().split("-", 1)[1]
    setup_path = fix_main_samples_path / package
    dist_created = setup_path / "dist"
    dist_already_exists = dist_created.exists()

    run_setup(setup_path / "setup.py", ["bdist_rpm"])

    base_name = f"test_{package}-{version}"

    file_created = dist_created / f"{base_name}-1.src.rpm"
    assert file_created.is_file()
    file_created.unlink()

    file_created = dist_created / f"{base_name}-1.{arch}.rpm"
    assert file_created.is_file()
    file_created.unlink()

    file_created = dist_created / f"{base_name}.tar.gz"
    assert file_created.is_file()
    file_created.unlink()

    if not dist_already_exists:
        dist_created.rmdir()
