"""Tests for cx_Freeze.hooks._av_."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import (
    ABI_THREAD,
    IS_ARM_64,
    IS_CONDA,
    IS_LINUX,
    IS_MACOS,
    IS_MINGW,
    IS_WINDOWS,
)

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_AV = """
test_av.py
    import av

    print("Hello from cx_Freeze")
    print("av version", av.__version__)
pyproject.toml
    [project]
    name = "test_av"
    version = "0.1.2.3"

    [tool.cxfreeze]
    executables = ["test_av.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.skipif(
    IS_CONDA and (IS_LINUX or (IS_ARM_64 and IS_MACOS)),
    reason="av (pyAV) is too slow in conda-forge (Linux and OSX_ARM64)",
)
@pytest.mark.xfail(
    IS_MINGW,
    raises=ModuleNotFoundError,
    reason="av (pyAV) not supported in mingw",
    strict=True,
)
@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="av (pyAV) not supported in windows arm64",
    strict=True,
)
@pytest.mark.xfail(
    sys.version_info[:2] >= (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="av (pyAV) does not support Python 3.13t",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_av(tmp_package, zip_packages: bool) -> None:
    """Test if av hook is working correctly."""
    tmp_package.create(SOURCE_TEST_AV)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.install("av")
    output = tmp_package.run()
    executable = tmp_package.executable("test_av")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    lines = output.splitlines()
    assert lines[0] == "Hello from cx_Freeze"
    assert lines[1].startswith("av version")
