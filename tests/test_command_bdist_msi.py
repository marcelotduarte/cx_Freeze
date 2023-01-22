"""Tests for cx_Freeze.command.bdist_msi."""

from __future__ import annotations

import sys
from pathlib import Path
from sysconfig import get_platform

import pytest
from setuptools import Distribution

from cx_Freeze.sandbox import run_setup

if sys.platform == "win32":
    from cx_Freeze.command.bdist_msi import BdistMSI

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "executables": [],
    "script_name": "setup.py",
}


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
def test_bdist_msi(fix_main_samples_path: Path):
    """Test the msi_binary_data sample."""

    setup_path = fix_main_samples_path / "msi_binary_data"
    dist_created = setup_path / "dist"
    dist_already_exists = dist_created.exists()

    run_setup(setup_path / "setup.py", ["bdist_msi"])

    platform = get_platform().replace("win-amd64", "win64")
    file_created = dist_created / f"hello-0.1-{platform}.msi"
    assert file_created.is_file()
    file_created.unlink()

    if not dist_already_exists:
        dist_created.rmdir()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
def test_bdist_msi_target_name():
    """Test the bdist_msi with extra target_name option."""

    dist = Distribution(DIST_ATTRS)
    cmd = BdistMSI(dist)
    cmd.target_name = "mytest"
    cmd.finalize_options()
    cmd.ensure_finalized()

    assert cmd.fullname == "mytest-0.0"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
def test_bdist_msi_target_name_and_version():
    """Test the bdist_msi with extra target options."""

    dist = Distribution(DIST_ATTRS)
    cmd = BdistMSI(dist)
    cmd.target_name = "mytest"
    cmd.target_version = "0.1"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.1"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
def test_bdist_msi_target_name_with_extension(fix_main_samples_path: Path):
    """Test the msi_binary_data sample, with a specified target_name that
    includes an ".msi" extension."""

    msi_name = "output.msi"
    setup_path = fix_main_samples_path / "msi_binary_data"
    dist_created = setup_path / "dist"
    dist_already_exists = dist_created.exists()

    run_setup(
        setup_path / "setup.py", ["bdist_msi", "--target-name", msi_name]
    )

    file_created = dist_created / msi_name
    assert file_created.is_file()
    file_created.unlink()

    if not dist_already_exists:
        dist_created.rmdir()
