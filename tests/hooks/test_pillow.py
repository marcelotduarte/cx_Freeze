"""Tests for cx_Freeze.hooks of pillow."""

from __future__ import annotations

import sys

import pytest

TIMEOUT = 10

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


@pytest.mark.venv
@zip_packages
def test_pillow(tmp_package, zip_packages: bool) -> None:
    """Test if pillow hook is working correctly."""
    tmp_package.create_from_sample("pillow")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    if sys.version_info[:2] < (3, 12):
        package = "pillow<10"
    elif sys.version_info[:2] == (3, 12):
        package = "pillow<10.2"
    else:
        package = "pillow"
    tmp_package.install(package)
    output = tmp_package.run()
    executable = tmp_package.executable("test_pillow")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=TIMEOUT)
    lines = output.splitlines()
    assert lines[0].startswith("Hello from cx_Freeze")
    assert lines[1] == "OK"
    assert len(lines) == 2
