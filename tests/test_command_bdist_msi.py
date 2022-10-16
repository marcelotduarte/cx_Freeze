"""Tests for cx_Freeze.command.bdist_msi."""
import os
import sys
from sysconfig import get_platform

import pytest

from cx_Freeze.dist import Distribution
from cx_Freeze.sandbox import run_setup

if sys.platform == "win32":
    from cx_Freeze.command.bdist_msi import BdistMSI


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
@pytest.mark.skipif(
    sys.version_info < (3, 7, 4), reason="requires python 3.7.4 or higher"
)
def test_bdist_msi(fix_main_samples_path):
    """Test the msi_binary_data sample."""

    setup_path = fix_main_samples_path / "msi_binary_data"
    run_setup(setup_path / "setup.py", ["bdist_msi"])

    platform = get_platform().replace("win-amd64", "win64")
    dist_created = setup_path / "dist"
    file_created = dist_created / f"hello-0.1-{platform}.msi"
    assert file_created.is_file()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
def test_bdist_msi_target_name():
    """Test the bdist_msi with extra target_name option."""

    dist = Distribution(
        {"name": "foo", "version": "0.0", "script_name": "setup.py"}
    )
    cmd = BdistMSI(dist)
    cmd.target_name = "mytest"
    cmd.finalize_options()
    cmd.ensure_finalized()

    assert cmd.fullname == "mytest-0.0"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
def test_bdist_msi_target_name_and_version():
    """Test the bdist_msi with extra target options."""

    dist = Distribution(
        {"name": "foo", "version": "0.0", "script_name": "setup.py"}
    )
    cmd = BdistMSI(dist)
    cmd.target_name = "mytest"
    cmd.target_version = "0.1"
    cmd.finalize_options()
    cmd.ensure_finalized()

    assert cmd.fullname == "mytest-0.1"

@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
@pytest.mark.skipif(
    sys.version_info < (3, 7, 4), reason="requires python 3.7.4 or higher"
)
def test_bdist_msi_target_name_with_extension(fix_main_samples_path):
    """Test the msi_binary_data sample, with a specified target_name that
    includes an ".msi" extension."""

    msi_name = "output.msi"
    setup_path = fix_main_samples_path / "msi_binary_data"
    run_setup(setup_path / "setup.py", ["bdist_msi", "--target-name", msi_name])

    dist_created = setup_path / "dist"
    file_created = dist_created / msi_name
    assert file_created.is_file()
    os.remove(file_created)



