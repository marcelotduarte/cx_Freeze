"""Tests for cx_Freeze.command.bdist_deb."""
from __future__ import annotations

import sys
from pathlib import Path
from subprocess import run

import pytest
from setuptools import Distribution

from cx_Freeze.command.bdist_deb import BdistDEB as bdist_deb
from cx_Freeze.exception import PlatformError

if sys.platform != "linux":
    pytest.skip(reason="Linux tests", allow_module_level=True)

FIXTURE_DIR = Path(__file__).resolve().parent

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "description": "cx_Freeze script to test bdist_deb",
    "executables": [],
    "script_name": "setup.py",
    "author": "Marcelo Duarte",
    "author_email": "marcelotduarte@users.noreply.github.com",
    "url": "https://github.com/marcelotduarte/cx_Freeze/",
}


def test_bdist_deb_not_posix(monkeypatch):
    """Test the bdist_deb fail if not on posix."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_deb(dist)
    monkeypatch.setattr("os.name", "nt")
    with pytest.raises(PlatformError, match="don't know how to create DEB"):
        cmd.finalize_options()


def test_bdist_deb_not_alien(monkeypatch):
    """Test the bdist_deb uses alien."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_deb(dist)
    monkeypatch.setattr("shutil.which", lambda _cmd: None)
    with pytest.raises(PlatformError, match="failed to find 'alien'"):
        cmd.finalize_options()


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "simple")
def test_bdist_deb_simple(datafiles: Path):
    """Test the simple sample with bdist_deb."""
    name = "hello"
    version = "0.1.2.3"
    dist_created = datafiles / "dist"

    process = run(
        [sys.executable, "setup.py", "bdist_deb"],
        text=True,
        capture_output=True,
        check=False,
        cwd=datafiles,
    )
    print(process.stdout)
    if process.returncode != 0:
        if "failed to find 'alien'" in process.stderr:
            pytest.xfail("alien not installed")
        else:
            pytest.fail(process.stderr)

    pattern = f"{name}_{version}-?_*.deb"
    file_created = next(dist_created.glob(pattern))
    assert file_created.is_file(), pattern


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "sqlite")
def test_bdist_deb(datafiles: Path):
    """Test the sqlite sample with bdist_deb."""
    name = "test_sqlite3"
    version = "0.5"
    dist_created = datafiles / "dist2"

    process = run(
        [sys.executable, "setup.py", "bdist_deb", "--dist-dir", dist_created],
        text=True,
        capture_output=True,
        check=False,
        cwd=datafiles,
    )
    print(process.stdout)
    if process.returncode != 0:
        if "failed to find 'alien'" in process.stderr:
            pytest.xfail("alien not installed")
        else:
            pytest.fail(process.stderr)

    pattern = f"{name.replace('_', '-')}_{version}-?_*.deb"
    file_created = next(dist_created.glob(pattern))
    assert file_created.is_file(), pattern
