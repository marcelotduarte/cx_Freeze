"""Tests for hooks of winrt (pywinrt)."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import ABI_THREAD, IS_CONDA, IS_MINGW

TIMEOUT = 15

if sys.platform != "win32":
    pytest.skip(reason="Windows tests", allow_module_level=True)

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


SOURCE_WINRT = """
test.py
    from winrt.windows.foundation import Uri

    # Test importing winrt submodule
    print("winrt.windows.foundation imported successfully")

    # Test Uri class from foundation
    test_uri = Uri("https://github.com/marcelotduarte/cx_Freeze")
    print(f"Uri domain: {test_uri.domain}")
    print(f"Uri scheme: {test_uri.scheme_name}")

    print("Test completed successfully")

pyproject.toml
    [project]
    name = "test_winrt"
    version = "0.1.0"
    dependencies = ["winrt.windows.foundation"]

    [tool.cxfreeze]
    executables = ["test.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.xfail(
    IS_MINGW,
    raises=ModuleNotFoundError,
    reason="pywinrt not supported in mingw",
    strict=True,
)
@pytest.mark.xfail(
    IS_CONDA,
    raises=ModuleNotFoundError,
    reason="pywinrt not supported in conda",
    strict=True,
)
@pytest.mark.xfail(
    ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="pywinrt does not support Python 3.13t/3.14t",
    strict=True,
)
@pytest.mark.venv(scope="module")
@zip_packages
def test_winrt(tmp_package, zip_packages: bool) -> None:
    """Test if winrt hook is working correctly."""
    tmp_package.create(SOURCE_WINRT)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(
        [
            "winrt.windows.foundation imported successfully",
            "Uri domain: github.com",
            "Uri scheme: https",
            "Test completed successfully",
        ]
    )
