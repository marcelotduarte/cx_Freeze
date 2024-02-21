"""Tests for cx_Freeze.command.bdist_msi."""

from __future__ import annotations

from pathlib import Path
from sysconfig import get_platform

import pytest
from generate_samples import create_package, run_command
from setuptools import Distribution

from cx_Freeze import Executable

bdist_msi = pytest.importorskip(
    "cx_Freeze.command.bdist_msi", reason="Windows tests"
).BdistMSI

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "executables": [Executable("hello.py")],
    "script_name": "setup.py",
}

TOP_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = TOP_DIR / "samples"


def test_bdist_msi_target_name():
    """Test the bdist_msi with extra target_name option."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_msi(dist)
    cmd.target_name = "mytest"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.0"


def test_bdist_msi_target_name_and_version():
    """Test the bdist_msi with extra target options."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_msi(dist)
    cmd.target_name = "mytest"
    cmd.target_version = "0.1"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.1"


@pytest.mark.datafiles(SAMPLES_DIR / "msi_binary_data")
def test_bdist_msi_default(datafiles: Path):
    """Test the msi_binary_data sample."""
    run_command(datafiles, "python setup.py bdist_msi")
    platform = get_platform().replace("win-amd64", "win64")
    file_created = datafiles / "dist" / f"hello-0.1.2.3-{platform}.msi"
    assert file_created.is_file()


@pytest.mark.datafiles(SAMPLES_DIR / "msi_extensions")
def test_bdist_msi_target_name_with_extension(datafiles: Path):
    """Test the msi_extensions sample, with a specified target_name that
    includes an ".msi" extension.
    """
    msi_name = "output.msi"
    run_command(
        datafiles, f"python setup.py bdist_msi --target-name {msi_name}"
    )
    file_created = datafiles / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.datafiles(SAMPLES_DIR / "msi_summary_data")
def test_bdist_msi_target_name_with_extension_1(datafiles: Path):
    """Test the msi_summary_data sample."""
    msi_name = "output.1.msi"
    run_command(
        datafiles, f"python setup.py bdist_msi --target-name {msi_name}"
    )
    file_created = datafiles / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.datafiles(SAMPLES_DIR / "advanced")
def test_bdist_msi_advanced(datafiles: Path):
    """Test the advanced sample."""
    msi_name = "output.msi"
    run_command(
        datafiles, f"python setup.py bdist_msi --target-name {msi_name}"
    )
    file_created = datafiles / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.datafiles(SAMPLES_DIR / "asmodule")
def test_bdist_msi_asmodule(datafiles: Path):
    """Test the asmodule sample."""
    msi_name = "output.msi"
    run_command(
        datafiles, f"python setup.py bdist_msi --target-name {msi_name}"
    )
    file_created = datafiles / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.datafiles(SAMPLES_DIR / "sqlite")
def test_bdist_msi_sqlite(datafiles: Path):
    """Test the sqlite sample."""
    msi_name = "output.msi"
    run_command(
        datafiles, f"python setup.py bdist_msi --target-name {msi_name}"
    )
    file_created = datafiles / "dist" / msi_name
    assert file_created.is_file()


SOURCE_HELLO = """
hello.py
    import pkg.hi
    print("Hello from cx_Freeze")
pkg/hi.py
    print("Hi!")
setup.py
    from cx_Freeze import Executable, setup

    setup(
        name="hello",
        version="0.1.2.3",
        description="Sample cx_Freeze script",
        executables=[Executable("hello.py")],
    )
"""


def test_bdist_msi_advanced2(tmp_path: Path):
    """Test the executables option."""
    create_package(tmp_path, SOURCE_HELLO)
    msi_name = "output.msi"
    run_command(
        tmp_path, f"python setup.py bdist_msi --target-name {msi_name}"
    )
    file_created = tmp_path / "dist" / msi_name
    assert file_created.is_file()
