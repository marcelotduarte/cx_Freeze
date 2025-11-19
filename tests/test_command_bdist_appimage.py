"""Tests for cx_Freeze.command.bdist_appimage."""

from __future__ import annotations

import os
import platform
from pathlib import Path

import pytest
from filelock import FileLock
from setuptools import Distribution

from cx_Freeze._compat import IS_LINUX
from cx_Freeze.command.bdist_appimage import bdist_appimage
from cx_Freeze.exception import PlatformError

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "description": "cx_Freeze script to test bdist_appimage",
    "executables": ["hello.py"],
    "script_name": "setup.py",
}


@pytest.mark.skipif(IS_LINUX, reason="Test not on Linux platform")
def test_bdist_appimage_not_posix() -> None:
    """Test the bdist_appimage fail if not on Linux."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    msg = "bdist_appimage is only supported on Linux"
    with pytest.raises(PlatformError, match=msg):
        cmd.finalize_options()


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_appimage_download_appimagetool() -> None:
    """Test the bdist_appimage, force the download."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    cmd.finalize_options()
    appimagetool = cmd.appimagetool
    # remove
    if os.path.exists(appimagetool):
        with FileLock(appimagetool + ".lock"):
            os.unlink(appimagetool)
    # force the download
    cmd2 = bdist_appimage(dist)
    cmd2.finalize_options()
    cmd2.ensure_finalized()
    assert os.path.exists(cmd2.appimagetool)
    assert cmd2.fullname == "foo-0.0"


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_appimage_download_runtime(tmp_path) -> None:
    """Test bdist_appimage for "offline" builds."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    # use locally installed appimagetool and runtime
    cmd.appimagetool = str(tmp_path / "appimagetool.AppImage")
    cmd.runtime_file = str(tmp_path / "type2_runtime")
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert os.path.exists(cmd.appimagetool)
    assert os.path.exists(cmd.runtime_file)
    assert cmd.fullname == "foo-0.0"


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_appimage_target_name() -> None:
    """Test the bdist_appimage with extra target_name option."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    cmd.target_name = "mytest"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.0"


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_appimage_target_name_and_version() -> None:
    """Test the bdist_appimage with extra target options."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_appimage(dist)
    cmd.target_name = "mytest"
    cmd.target_version = "0.1"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.1"


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_appimage_target_name_and_name_none() -> None:
    """Test the bdist_appimage with target options."""
    attrs = DIST_ATTRS.copy()
    del attrs["name"]
    attrs["executables"].append("other.py")
    dist = Distribution(attrs)
    cmd = bdist_appimage(dist)
    cmd.finalize_options()  # name = None, target_name = first script name
    cmd.ensure_finalized()
    assert cmd.fullname == "hello-0.0"


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
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


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
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

    tmp_package.freeze(f"python setup.py bdist_appimage --target-name {name}")
    file_created = Path(outfile)
    assert file_created.is_file()


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_appimage_skip_build(tmp_package) -> None:
    """Test the tkinter sample with bdist_appimage."""
    name = "test_tkinter"
    version = "0.3.2"
    arch = platform.machine()

    tmp_package.create_from_sample("tkinter")
    tmp_package.freeze()
    tmp_package.freeze("python setup.py bdist_appimage --skip-build")

    app = tmp_package.path / "dist" / f"{name}-{version}-{arch}.AppImage"
    assert app.is_file(), f"{name}-{version}-{arch}.AppImage"


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_appimage_implicit_skip_build(tmp_package) -> None:
    """Test the simple sample with build_exe then a bdist_appimage.

    This forces a implicit skip_build.
    """
    name = "hello"
    version = "0.1.2.3"
    arch = platform.machine()
    updateinformation = f"zsync|{name}-*-{arch}.AppImage.zsync"

    tmp_package.create_from_sample("simple")
    tmp_package.freeze(
        "python setup.py build_exe --silent bdist_appimage"
        f" --updateinformation={updateinformation}"
    )

    app = tmp_package.path / "dist" / f"{name}-{version}-{arch}.AppImage"
    assert app.is_file(), f"{name}-{version}-{arch}.AppImage"

    result = tmp_package.run(app, timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")

    result = tmp_package.run(f"{app} --appimage-updateinformation", timeout=10)
    result.stdout.fnmatch_lines(updateinformation)

    zsync_created = app.parent / f"{app.name}.zsync"
    assert zsync_created.is_file(), f"file not found: {zsync_created}"


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_appimage_simple(tmp_package) -> None:
    """Test the simple sample with bdist_appimage."""
    name = "simple"
    version = "0.1.2.3"
    arch = platform.machine()

    tmp_package.create_from_sample("simple")
    tmp_package.freeze(
        "python setup.py -v bdist_appimage"
        " --updateinformation=guess "
        f" --target-name={name} --target-version={version}"
    )

    app = tmp_package.path / "dist" / f"{name}-{version}-{arch}.AppImage"
    assert app.is_file(), f"file not found: {app}"

    result = tmp_package.run(app, timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")

    result = tmp_package.run(f"{app} --appimage-extract-and-run", timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")

    if os.getenv("GITHUB_REPOSITORY"):
        zsync_created = app.parent / f"{app.name}.zsync"
        assert zsync_created.is_file(), f"file not found: {zsync_created}"
