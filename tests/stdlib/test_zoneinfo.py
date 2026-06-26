"""Tests for hooks of stdlib zoneinfo."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from cx_Freeze._compat import IS_WINDOWS

if TYPE_CHECKING:
    from tests.conftest import TempPackage

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


@pytest.mark.venv(install_dependencies=False)
@pytest.mark.skipif(IS_WINDOWS, reason="Windows doesn't have system timezone")
@zip_packages
def test_zoneinfo(tmp_package: TempPackage, zip_packages: bool) -> None:
    """Test if zoneinfo hook with system timezone is working correctly."""
    tmp_package.create_from_sample("tz")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    result = tmp_package.freeze()

    executable = tmp_package.executable("test_tz")
    assert executable.is_file()
    result = tmp_package.run(executable)
    if result.stderr.lines:
        python_result = tmp_package.run("python test_tz.py")
        if python_result.stderr.lines:
            pytest.xfail("system timezone is broken")
    result.stdout.fnmatch_lines(
        [
            "TZPATH: *",
            "Available timezones: *",
            "UTC time: *",
            "Brazil time: *",
            "US Eastern time: *",
        ]
    )


@pytest.mark.venv
@zip_packages
def test_zoneinfo_and_tzdata(
    tmp_package: TempPackage, zip_packages: bool
) -> None:
    """Test if zoneinfo and tzdata hook is working correctly."""
    tmp_package.create_from_sample("tz")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    result = tmp_package.freeze()

    executable = tmp_package.executable("test_tz")
    assert executable.is_file()
    result = tmp_package.run(executable)
    result.stdout.fnmatch_lines(
        [
            "TZPATH: *",
            "Available timezones: *",
            "UTC time: *",
            "Brazil time: *",
            "US Eastern time: *",
        ]
    )
