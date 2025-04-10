"""Tests for cx_Freeze.command.bdist_appimage."""

from __future__ import annotations

import os
import platform
import sys
from pathlib import Path

import pytest
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


def test_bdist_appimage_target_name_with_extension(tmp_package) -> None:
    """Test the tkinter sample, with a specified target_name that includes an
    ".AppImage" extension.
    """
    name = "output.AppImage"

    # create bdist and dist to test coverage
    tmp_package.create_from_sample("tkinter")
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    cmd.finalize_options()
    cmd.ensure_finalized()
    cmd.mkpath(os.path.join(cmd.bdist_base, "AppDir"))
    cmd.mkpath(cmd.dist_dir)
    outfile = os.path.join(cmd.dist_dir, name)
    cmd.save_as_file("data", outfile, mode="rwx")

    tmp_package.run(f"python setup.py bdist_appimage --target-name {name}")
    file_created = Path(outfile)
    assert file_created.is_file()


def test_bdist_appimage_skip_build(tmp_package) -> None:
    """Test the tkinter sample with bdist_appimage."""
    name = "test_tkinter"
    version = "0.3.2"
    arch = platform.machine()

    tmp_package.create_from_sample("tkinter")
    tmp_package.run()
    tmp_package.run("python setup.py bdist_appimage --skip-build")

    file_created = (
        tmp_package.path / "dist" / f"{name}-{version}-{arch}.AppImage"
    )
    assert file_created.is_file(), f"{name}-{version}-{arch}.AppImage"


def test_bdist_appimage_simple(tmp_package) -> None:
    """Test the simple sample with bdist_appimage."""
    name = "hello"
    version = "0.1.2.3"
    arch = platform.machine()

    tmp_package.create_from_sample("simple")
    tmp_package.run("python setup.py bdist_appimage --quiet")

    file_created = (
        tmp_package.path / "dist" / f"{name}-{version}-{arch}.AppImage"
    )
    assert file_created.is_file(), f"{name}-{version}-{arch}.AppImage"
