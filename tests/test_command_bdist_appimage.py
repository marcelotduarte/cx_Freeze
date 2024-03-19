"""Tests for cx_Freeze.command.bdist_appimage."""

from __future__ import annotations

import os
import platform
import sys
from pathlib import Path

import pytest
from generate_samples import run_command
from setuptools import Distribution

from cx_Freeze.exception import PlatformError

bdist_appimage = pytest.importorskip(
    "cx_Freeze.command.bdist_appimage", reason="Linux tests"
).bdist_appimage

if sys.platform != "linux":
    pytest.skip(reason="Linux tests", allow_module_level=True)

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "description": "cx_Freeze script to test bdist_appimage",
    "executables": ["hello.py"],
    "script_name": "setup.py",
}
SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"


def test_bdist_appimage_not_posix(monkeypatch) -> None:
    """Test the bdist_appimage fail if not on posix."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    monkeypatch.setattr("os.name", "nt")
    with pytest.raises(PlatformError, match="don't know how to create App"):
        cmd.finalize_options()


def test_bdist_appimage_target_name() -> None:
    """Test the bdist_appimage with extra target_name option."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    cmd.target_name = "mytest"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.0"


def test_bdist_appimage_target_name_and_version() -> None:
    """Test the bdist_appimage with extra target options."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    cmd.target_name = "mytest"
    cmd.target_version = "0.1"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.1"


def test_bdist_appimage_target_name_and_version_none() -> None:
    """Test the bdist_appimage with target options."""
    attrs = DIST_ATTRS.copy()
    del attrs["version"]
    dist = Distribution(attrs)
    cmd = bdist_appimage(dist)
    cmd.target_name = "mytest"
    cmd.finalize_options()  # version = None, target_version = None
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest"


@pytest.mark.datafiles(SAMPLES_DIR / "tkinter")
def test_bdist_appimage_target_name_with_extension(datafiles: Path) -> None:
    """Test the tkinter sample, with a specified target_name that includes an
    ".AppImage" extension.
    """
    name = "output.AppImage"

    # create bdist and dist to test coverage
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    cmd.finalize_options()
    cmd.ensure_finalized()
    cmd.mkpath(os.path.join(cmd.bdist_base, "AppDir"))
    cmd.mkpath(cmd.dist_dir)
    outfile = os.path.join(cmd.dist_dir, name)
    cmd.save_as_file("data", outfile, mode="rwx")

    run_command(
        datafiles, f"python setup.py bdist_appimage --target-name {name}"
    )
    file_created = Path(outfile)
    assert file_created.is_file()


@pytest.mark.datafiles(SAMPLES_DIR / "tkinter")
def test_bdist_appimage_skip_build(datafiles: Path) -> None:
    """Test the tkinter sample with bdist_appimage."""
    name = "test_tkinter"
    version = "0.3.2"
    arch = platform.machine()
    run_command(datafiles)
    run_command(datafiles, "python setup.py bdist_appimage --skip-build")

    file_created = datafiles / "dist" / f"{name}-{version}-{arch}.AppImage"
    assert file_created.is_file(), f"{name}-{version}-{arch}.AppImage"


@pytest.mark.datafiles(SAMPLES_DIR / "simple")
def test_bdist_appimage_simple(datafiles: Path) -> None:
    """Test the simple sample with bdist_appimage."""
    name = "hello"
    version = "0.1.2.3"
    arch = platform.machine()

    run_command(datafiles, "python setup.py bdist_appimage --quiet")

    file_created = datafiles / "dist" / f"{name}-{version}-{arch}.AppImage"
    assert file_created.is_file(), f"{name}-{version}-{arch}.AppImage"
