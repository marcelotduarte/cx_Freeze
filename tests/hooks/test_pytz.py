"""Tests for cx_Freeze.hooks._pytz_."""

from __future__ import annotations

import pytest

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


@zip_packages
def test_pytz(tmp_package, zip_packages: bool) -> None:
    """Test if pytz hook is working correctly."""
    tmp_package.create_from_sample("pytz")
    tmp_package.install("pytz")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    output = tmp_package.run()

    executable = tmp_package.executable("test_pytz")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    lines = output.splitlines()
    assert lines[0].startswith("UTC")
    assert lines[1].startswith("Brazil")
    assert lines[2].startswith("US")
