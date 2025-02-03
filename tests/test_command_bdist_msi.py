"""Tests for cx_Freeze.command.bdist_msi."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from generate_samples import create_package, run_command
from setuptools import Distribution

from cx_Freeze._compat import PLATFORM

bdist_msi = pytest.importorskip(
    "cx_Freeze.command.bdist_msi", reason="Windows tests"
).bdist_msi

if sys.platform != "win32":
    pytest.skip(reason="Windows tests", allow_module_level=True)

if sys.version_info[:2] >= (3, 13):
    pytest.skip(
        reason="bdist_msi is not supported on Python 3.13 yet.",
        allow_module_level=True,
    )

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "executables": ["hello.py"],
    "script_name": "setup.py",
}

TOP_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = TOP_DIR / "samples"


def test_bdist_msi_target_name() -> None:
    """Test the bdist_msi with extra target_name option."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_msi(dist)
    cmd.target_name = "mytest"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.0"


def test_bdist_msi_target_name_and_version() -> None:
    """Test the bdist_msi with extra target options."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_msi(dist)
    cmd.target_name = "mytest"
    cmd.target_version = "0.1"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.1"


@pytest.mark.datafiles(SAMPLES_DIR / "msi_binary_data")
def test_bdist_msi_default(datafiles: Path) -> None:
    """Test the msi_binary_data sample."""
    run_command(datafiles, "cxfreeze bdist_msi")
    platform = PLATFORM.replace("win-amd64", "win64")
    file_created = datafiles / "dist" / f"hello-0.1.2.3-{platform}.msi"
    assert file_created.is_file()


@pytest.mark.datafiles(SAMPLES_DIR / "msi_extensions")
def test_bdist_msi_target_name_with_extension(datafiles: Path) -> None:
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
def test_bdist_msi_target_name_with_extension_1(datafiles: Path) -> None:
    """Test the msi_summary_data sample."""
    msi_name = "output.1.msi"
    run_command(
        datafiles, f"python setup.py bdist_msi --target-name {msi_name}"
    )
    file_created = datafiles / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.datafiles(SAMPLES_DIR / "msi_license")
def test_bdist_msi_with_license(datafiles: Path) -> None:
    """Test the msi_license sample."""
    platform = PLATFORM.replace("win-amd64", "win64")
    msi_name = f"hello-0.1-{platform}.msi"
    run_command(datafiles, "python setup.py bdist_msi")
    file_created = datafiles / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.datafiles(SAMPLES_DIR / "advanced")
def test_bdist_msi_advanced(datafiles: Path) -> None:
    """Test the advanced sample."""
    msi_name = "output.msi"
    run_command(
        datafiles, f"python setup.py bdist_msi --target-name {msi_name}"
    )
    file_created = datafiles / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.datafiles(SAMPLES_DIR / "asmodule")
def test_bdist_msi_asmodule(datafiles: Path) -> None:
    """Test the asmodule sample."""
    msi_name = "output.msi"
    run_command(
        datafiles, f"python setup.py bdist_msi --target-name {msi_name}"
    )
    file_created = datafiles / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.datafiles(SAMPLES_DIR / "sqlite")
def test_bdist_msi_sqlite(datafiles: Path) -> None:
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
pyproject.toml
    [project]
    name = "hello"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"

    [[tool.cxfreeze.executables]]
    script = "hello.py"

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "unittest"]

    [tool.cxfreeze.bdist_msi]
    target_name = "output.msi"
"""


def test_bdist_msi_advanced2(tmp_path: Path) -> None:
    """Test the executables option."""
    create_package(tmp_path, SOURCE_HELLO)
    run_command(tmp_path, "cxfreeze bdist_msi")
    file_created = tmp_path / "dist" / "output.msi"
    assert file_created.is_file()
