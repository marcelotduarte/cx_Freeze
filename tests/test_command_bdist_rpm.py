"""Tests for cx_Freeze.command.bdist_rpm."""
from __future__ import annotations

import platform
import sys
from pathlib import Path
from subprocess import run

import pytest
from setuptools import Distribution

from cx_Freeze.command.bdist_rpm import BdistRPM as bdist_rpm
from cx_Freeze.exception import PlatformError

if sys.platform != "linux":
    pytest.skip(reason="Linux tests", allow_module_level=True)

FIXTURE_DIR = Path(__file__).resolve().parent

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "description": "cx_Freeze script to test bdist_rpm",
    "executables": [],
    "script_name": "setup.py",
    "author": "Marcelo Duarte",
    "author_email": "marcelotduarte@users.noreply.github.com",
    "url": "https://github.com/marcelotduarte/cx_Freeze/",
}


def test_bdist_rpm_not_posix(monkeypatch):
    """Test the bdist_rpm fail if not on posix."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_rpm(dist)
    monkeypatch.setattr("os.name", "nt")
    with pytest.raises(PlatformError, match="don't know how to create RPM"):
        cmd.finalize_options()


def test_bdist_rpm_not_rpmbuild(monkeypatch):
    """Test the bdist_rpm uses rpmbuild."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_rpm(dist)
    monkeypatch.setattr("shutil.which", lambda _cmd: None)
    with pytest.raises(PlatformError, match="failed to find rpmbuild"):
        cmd.finalize_options()


@pytest.mark.parametrize("options", [({"spec_only": True})], ids=["spec_only"])
def test_bdist_rpm_options(options):
    """Test the bdist_rpm with options."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_rpm(dist, **options)
    try:
        cmd.ensure_finalized()
    except PlatformError as exc:
        if "failed to find rpmbuild" in exc.args[0]:
            pytest.xfail("rpmbuild not installed")
        else:
            pytest.fail(exc.args[0])


@pytest.mark.parametrize("options", [({"spec_only": True})], ids=["spec_only"])
@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "simple")
def test_bdist_rpm_options_run(datafiles: Path, monkeypatch, options):
    """Test the bdist_rpm with options."""
    monkeypatch.chdir(datafiles)
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_rpm(dist, **options, debug=1)
    try:
        cmd.ensure_finalized()
    except PlatformError as exc:
        if "failed to find rpmbuild" in exc.args[0]:
            pytest.xfail("rpmbuild not installed")
        else:
            pytest.fail(exc.args[0])
    cmd.run()


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "simple")
def test_bdist_rpm_simple(datafiles: Path):
    """Test the simple sample with bdist_rpm."""
    name = "hello"
    version = "0.1.2.3"
    arch = platform.machine()
    dist_created = datafiles / "dist"

    process = run(
        [sys.executable, "setup.py", "bdist_rpm", "--quiet"],
        text=True,
        capture_output=True,
        check=False,
        cwd=datafiles,
    )
    print(process.stdout)
    if process.returncode != 0:
        if "failed to find rpmbuild" in process.stderr:
            pytest.xfail("rpmbuild not installed")
        else:
            pytest.fail(process.stderr)

    base_name = f"{name}-{version}"
    file_created = dist_created / f"{base_name}-1.{arch}.rpm"
    assert file_created.is_file(), f"{base_name}-1.{arch}.rpm"


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "sqlite")
def test_bdist_rpm(datafiles: Path):
    """Test the sqlite sample with bdist_rpm."""
    name = "test_sqlite3"
    version = "0.5"
    arch = platform.machine()
    dist_created = datafiles / "dist"

    process = run(
        [sys.executable, "setup.py", "bdist_rpm"],
        text=True,
        capture_output=True,
        check=False,
        cwd=datafiles,
    )
    print(process.stdout)
    if process.returncode != 0:
        if "failed to find rpmbuild" in process.stderr:
            pytest.xfail("rpmbuild not installed")
        else:
            pytest.fail(process.stderr)

    base_name = f"{name}-{version}"
    file_created = dist_created / f"{base_name}-1.{arch}.rpm"
    assert file_created.is_file(), f"{base_name}-1.{arch}.rpm"
