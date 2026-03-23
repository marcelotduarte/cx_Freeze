"""Tests for hooks of charset_normalizer."""

from __future__ import annotations

import pytest

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_CHARSET_NORMALIZER = """
test_charset_normalizer.py
    import charset_normalizer

    print("Hello from cx_Freeze")
    print("charset_normalizer version", charset_normalizer.__version__)
pyproject.toml
    [project]
    name = "test_charset_normalizer"
    version = "0.1.2.3"
    dependencies = [
        "charset_normalizer<3.0;python_version < '3.12'",
        "charset_normalizer>=3.0;python_version >= '3.12'",
    ]

    [tool.cxfreeze]
    executables = ["test_charset_normalizer.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.venv
@zip_packages
def test_charset_normalizer(tmp_package, zip_packages: bool) -> None:
    """Test if charset_normalizer hook is working correctly."""
    tmp_package.create(SOURCE_TEST_CHARSET_NORMALIZER)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_charset_normalizer")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(
        ["Hello from cx_Freeze", "charset_normalizer version *"]
    )
