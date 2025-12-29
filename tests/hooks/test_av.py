"""Tests for hooks of av (pyAV)."""

from __future__ import annotations

import pytest

from cx_Freeze._compat import (
    IS_ARM_64,
    IS_CONDA,
    IS_LINUX,
    IS_MACOS,
    IS_MINGW,
    IS_UCRT,
    IS_WINDOWS,
)

TIMEOUT_ULTRA_VERY_SLOW = 240 if IS_CONDA else 120

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
    dependencies = ["av"]

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
    IS_MINGW and not IS_UCRT,
    raises=ModuleNotFoundError,
    reason="av (pyAV) supported only in mingw linked to ucrt",
    strict=True,
)
@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="av (pyAV) does not support Windows arm64",
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
    tmp_package.freeze()
    executable = tmp_package.executable("test_av")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT_ULTRA_VERY_SLOW)
    result.stdout.fnmatch_lines(["Hello from cx_Freeze", "av version *"])
