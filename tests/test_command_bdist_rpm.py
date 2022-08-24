"""Tests for cx_Freeze.command.bdist_rpm."""

import sys
from sysconfig import get_platform

import pytest

from cx_Freeze.sandbox import run_setup


@pytest.mark.skipif(sys.platform != "linux", reason="Linux tests")
def test_bdist_rpm(fix_main_samples_path):
    """Test the bcrypt sample with bdist_rpm."""

    package = "bcrypt"
    version = "0.3"
    arch = get_platform().split("-", 1)[1]
    setup_path = fix_main_samples_path / package

    run_setup(setup_path / "setup.py", ["bdist_rpm"])

    dist_created = setup_path / "dist"
    base_name = f"test_{package}-{version}"

    assert dist_created.joinpath(f"{base_name}-1.src.rpm").is_file()
    assert dist_created.joinpath(f"{base_name}-1.{arch}.rpm").is_file()
    assert dist_created.joinpath(f"{base_name}.tar.gz").is_file()
