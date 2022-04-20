"""Test bdist_rpm is working correctly."""

import sys
from sysconfig import get_platform

import pytest

from cx_Freeze.sandbox import run_setup


@pytest.mark.skipif(sys.platform != "linux", reason="Linux tests")
def test_bdist_rpm(fix_main_samples_path):
    """Test the bcrypt sample with bdist_rpm."""

    setup_path = fix_main_samples_path / "bcrypt"
    run_setup(setup_path / "setup.py", ["bdist_rpm"])

    dist_created = setup_path / "dist"
    arch = get_platform().split("-", 1)[1]

    assert dist_created.joinpath("test_bcrypt-0.3-1.src.rpm").is_file()
    assert dist_created.joinpath(f"test_bcrypt-0.3-1.{arch}.rpm").is_file()
    assert dist_created.joinpath("test_bcrypt-0.3.tar.gz").is_file()
