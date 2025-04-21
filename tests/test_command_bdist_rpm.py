"""Tests for cx_Freeze.command.bdist_rpm."""

from __future__ import annotations

import platform
import sys
from shutil import which
from subprocess import run

import pytest
from setuptools import Distribution

from cx_Freeze._compat import IS_LINUX
from cx_Freeze.command.bdist_rpm import bdist_rpm
from cx_Freeze.exception import PlatformError

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "description": "cx_Freeze script to test bdist_rpm",
    "executables": ["hello.py"],
    "script_name": "setup.py",
    "author": "Marcelo Duarte",
    "author_email": "marcelotduarte@users.noreply.github.com",
    "url": "https://github.com/marcelotduarte/cx_Freeze/",
}


@pytest.mark.skipif(IS_LINUX, reason="Test not on Linux platform")
def test_bdist_rpm_not_posix() -> None:
    """Test the bdist_rpm fail if not on Linux."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_rpm(dist)
    with pytest.raises(
        PlatformError, match="bdist_rpm is supported only on Linux"
    ):
        cmd.finalize_options()


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_rpm_not_rpmbuild(monkeypatch) -> None:
    """Test the bdist_rpm uses rpmbuild."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_rpm(dist)
    monkeypatch.setattr("shutil.which", lambda _cmd: None)
    with pytest.raises(PlatformError, match="failed to find rpmbuild"):
        cmd.finalize_options()


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
@pytest.mark.parametrize("options", [{"spec_only": True}], ids=["spec_only"])
def test_bdist_rpm_options(options) -> None:
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


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
@pytest.mark.parametrize("options", [{"spec_only": True}], ids=["spec_only"])
def test_bdist_rpm_options_run(tmp_package, options) -> None:
    """Test the bdist_rpm with options."""
    tmp_package.create_from_sample("simple")
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


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_rpm_simple(tmp_package) -> None:
    """Test the simple sample with bdist_rpm."""
    name = "hello"
    version = "0.1.2.3"
    arch = platform.machine()
    dist_created = tmp_package.path / "dist"

    tmp_package.create_from_sample("simple")
    process = run(
        [sys.executable, "setup.py", "bdist_rpm", "--quiet"],
        text=True,
        capture_output=True,
        check=False,
        cwd=tmp_package.path,
    )
    if process.returncode != 0:
        if "failed to find rpmbuild" in process.stderr:
            pytest.xfail("rpmbuild not installed")
        else:
            pytest.fail(process.stderr)

    base_name = f"{name}-{version}"
    file_created = dist_created / f"{base_name}-1.{arch}.rpm"
    assert file_created.is_file(), f"{base_name}-1.{arch}.rpm"


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_rpm_simple_pyproject(tmp_package) -> None:
    """Test the simple_pyproject sample with bdist_rpm."""
    name = "hello"
    version = "0.1.2.3"
    arch = platform.machine()
    dist_created = tmp_package.path / "dist"

    tmp_package.create_from_sample("simple_pyproject")
    cxfreeze = which("cxfreeze")
    process = run(
        [cxfreeze, "bdist_rpm", "--quiet"],
        text=True,
        capture_output=True,
        check=False,
        cwd=tmp_package.path,
    )
    if process.returncode != 0:
        if "failed to find rpmbuild" in process.stderr:
            pytest.xfail("rpmbuild not installed")
        else:
            pytest.fail(process.stderr)

    base_name = f"{name}-{version}"
    file_created = dist_created / f"{base_name}-1.{arch}.rpm"
    assert file_created.is_file(), f"{base_name}-1.{arch}.rpm"


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_bdist_rpm(tmp_package) -> None:
    """Test the sqlite sample with bdist_rpm."""
    name = "test_sqlite3"
    version = "0.5"
    arch = platform.machine()
    dist_created = tmp_package.path / "dist"

    tmp_package.create_from_sample("sqlite")
    process = run(
        [sys.executable, "setup.py", "bdist_rpm"],
        text=True,
        capture_output=True,
        check=False,
        cwd=tmp_package.path,
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
