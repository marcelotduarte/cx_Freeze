"""Tests for hooks of pytz."""

from __future__ import annotations

import pytest

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


@pytest.mark.venv(scope="module")
@zip_packages
def test_pytz(tmp_package, zip_packages: bool) -> None:
    """Test if pytz hook is working correctly."""
    tmp_package.create_from_sample("pytz")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_pytz")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(
        ["UTC time: *", "Brazil time: *", "US Eastern time: *"]
    )
