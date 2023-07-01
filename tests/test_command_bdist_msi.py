"""Tests for cx_Freeze.command.bdist_msi."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from subprocess import check_output
from sysconfig import get_platform

import pytest
from setuptools import Distribution

if sys.platform == "win32":
    from cx_Freeze.command.bdist_msi import BdistMSI

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "executables": [],
    "script_name": "setup.py",
}
FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "msi_binary_data")
def test_bdist_msi(datafiles: Path):
    """Test the msi_binary_data sample."""
    output = check_output(
        [sys.executable, "setup.py", "bdist_msi"],
        text=True,
        cwd=os.fspath(datafiles),
    )
    print(output)
    platform = get_platform().replace("win-amd64", "win64")
    file_created = datafiles / "dist" / f"hello-0.1-{platform}.msi"
    assert file_created.is_file()


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
@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "msi_binary_data")
def test_bdist_msi_target_name_with_extension(datafiles: Path):
    """Test the msi_binary_data sample, with a specified target_name that
    includes an ".msi" extension.
    """
    msi_name = "output.msi"
    output = check_output(
        [sys.executable, "setup.py", "bdist_msi", "--target-name", msi_name],
        text=True,
        cwd=os.fspath(datafiles),
    )
    print(output)
    file_created = datafiles / "dist" / msi_name
    assert file_created.is_file()
