"""Tests for cx_Freeze.command.bdist_msi."""

import sys
from sysconfig import get_platform

import pytest

from cx_Freeze.sandbox import run_setup


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
