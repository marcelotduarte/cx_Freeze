"""Tests for cx_Freeze.command.bdist_deb."""

from __future__ import annotations

import sys
from shutil import which
from subprocess import run
from typing import TYPE_CHECKING

import pytest
from setuptools import Distribution

from cx_Freeze._compat import IS_LINUX
from cx_Freeze.command.bdist_deb import bdist_deb
from cx_Freeze.exception import PlatformError

if TYPE_CHECKING:
    from pathlib import Path

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "description": "cx_Freeze script to test bdist_deb",
    "executables": ["hello.py"],
    "script_name": "setup.py",
    "author": "Marcelo Duarte",
    "author_email": "marcelotduarte@users.noreply.github.com",
    "url": "https://github.com/marcelotduarte/cx_Freeze/",
}


@pytest.mark.skipif(IS_LINUX, reason="Test not on Linux platform")
def test_bdist_deb_not_posix() -> None:
    """Test the bdist_deb fail if not on Linux."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_deb(dist)
    with pytest.raises(
        PlatformError, match="bdist_deb is supported only on Linux"
    ):
        cmd.finalize_options()


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_deb_not_alien(monkeypatch) -> None:
    """Test the bdist_deb uses alien."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_deb(dist)
    monkeypatch.setattr("shutil.which", lambda cmd: cmd != "alien")
    with pytest.raises(PlatformError, match="failed to find 'alien'"):
        cmd.finalize_options()


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_deb_not_fakeroot(monkeypatch) -> None:
    """Test the bdist_deb uses fakeroot."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_deb(dist)
    monkeypatch.setattr("os.getuid", lambda: 1000)
    monkeypatch.setattr("shutil.which", lambda cmd: cmd != "fakeroot")
    with pytest.raises(PlatformError, match="failed to find 'fakeroot'"):
        cmd.finalize_options()


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_deb_dry_run(monkeypatch, tmp_path: Path) -> None:
    """Test the bdist_deb dry_run."""
    monkeypatch.chdir(tmp_path)
    attrs = DIST_ATTRS.copy()
    attrs["dry_run"] = True
    dist = Distribution(attrs)
    cmd = bdist_deb(dist)
    monkeypatch.setattr("os.getuid", lambda: 1000)
    monkeypatch.setattr(
        "shutil.which", lambda cmd: cmd != "alien" or cmd != "fakeroot"
    )
    cmd.finalize_options()
    cmd.run()


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_deb_simple(tmp_package) -> None:
    """Test the simple sample with bdist_deb."""
    name = "hello"
    version = "0.1.2.3"
    dist_created = tmp_package.path / "dist"

    tmp_package.create_from_sample("simple")
    process = run(
        [sys.executable, "setup.py", "bdist_deb"],
        text=True,
        capture_output=True,
        check=False,
        cwd=tmp_package.path,
    )
    if process.returncode != 0:
        msg = process.stderr
        if "failed to find 'alien'" in msg:
            pytest.xfail("alien not installed")
        elif "Unpacking of '" in msg and "' failed at" in msg:
            pytest.xfail("cpio 2.13 bug")
        else:
            pytest.fail(process.stderr)

    pattern = f"{name}_{version}-?_*.deb"
    file_created = next(dist_created.glob(pattern), None)
    assert file_created, pattern
    assert file_created.is_file(), pattern


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_deb_simple_pyproject(tmp_package) -> None:
    """Test the simple_pyproject sample with bdist_deb."""
    name = "hello"
    version = "0.1.2.3"
    dist_created = tmp_package.path / "dist"

    tmp_package.create_from_sample("simple_pyproject")
    cxfreeze = which("cxfreeze")
    process = run(
        [cxfreeze, "bdist_deb"],
        text=True,
        capture_output=True,
        check=False,
        cwd=tmp_package.path,
    )
    if process.returncode != 0:
        msg = process.stderr
        if "failed to find 'alien'" in msg:
            pytest.xfail("alien not installed")
        elif "Unpacking of '" in msg and "' failed at" in msg:
            pytest.xfail("cpio 2.13 bug")
        else:
            pytest.fail(process.stderr)

    pattern = f"{name}_{version}-?_*.deb"
    file_created = next(dist_created.glob(pattern), None)
    assert file_created, pattern
    assert file_created.is_file(), pattern


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_deb(tmp_package) -> None:
    """Test the sqlite sample with bdist_deb."""
    name = "test_sqlite3"
    version = "0.5"
    dist_created = tmp_package.path / "dist2"

    tmp_package.create_from_sample("sqlite")
    process = run(
        [sys.executable, "setup.py", "bdist_deb", "--dist-dir", dist_created],
        text=True,
        capture_output=True,
        check=False,
        cwd=tmp_package.path,
    )
    if process.returncode != 0:
        msg = process.stderr
        if "failed to find 'alien'" in msg:
            pytest.xfail("alien not installed")
        elif "Unpacking of '" in msg and "' failed at" in msg:
            pytest.xfail("cpio 2.13 bug")
        else:
            pytest.fail(process.stderr)

    pattern = f"{name.replace('_', '-')}_{version}-?_*.deb"
    file_created = next(dist_created.glob(pattern), None)
    assert file_created, pattern
    assert file_created.is_file(), pattern
