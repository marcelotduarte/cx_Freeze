"""Tests for some cx_Freeze.hooks."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import ABI_THREAD

SOURCE = """
test_argon2.py
    import argon2
    from importlib.metadata import distribution, version

    print("Hello from cx_Freeze")
    print(argon2.__name__, version("argon2-cffi"))
command
    cxfreeze --script test_argon2.py build_exe
"""


@pytest.mark.skipif(
    sys.version_info[:2] >= (3, 13) and ABI_THREAD != "",
    reason="argon2-cffi does not support Python 3.13t",
)
def test_argon2(tmp_package) -> None:
    """Test if argon2-cffi is working correctly."""
    tmp_package.create(SOURCE)
    tmp_package.install("argon2-cffi")
    output = tmp_package.run()
    executable = tmp_package.executable("test_argon2")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    assert output.splitlines()[0] == "Hello from cx_Freeze"
    assert output.splitlines()[1].startswith("argon2")
