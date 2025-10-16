"""Tests for hooks of win32com (pywin32)."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import ABI_THREAD

TIMEOUT = 15

if sys.platform != "win32":
    pytest.skip(reason="Windows tests", allow_module_level=True)

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


@pytest.mark.xfail(
    ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="pywin32 does not support Python 3.13t/3.14t",
    strict=True,
)
@pytest.mark.venv(scope="module")
@zip_packages
def test_win32com(tmp_package, zip_packages: bool) -> None:
    """Test if win32com hook is working correctly."""
    tmp_package.create_from_sample("win32com")
    command = "cxfreeze --script test_win32com.py --excludes=tkinter,unittest"
    if zip_packages:
        command += " --zip-include-packages=* --zip-exclude-packages="
    command += " --include-msvcr --silent"
    tmp_package.install("pywin32")
    tmp_package.freeze(command)

    executable = tmp_package.executable("test_win32com")
    assert executable.is_file()

    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(
        [
            "Sent and received 'Hello from cx_Freeze'",
            "Sent and received b'Here is a null*'",
            "Sent and received 'Here is a null*'",
            "Sent and received 'test-*'",
            "Everything seemed to work!",
        ]
    )


SOURCE_WIN32COM_SHELL = """
test.py
    from win32com.shell import shell
    import pythoncom
    shortcut = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink, None,
            pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink
    )
    print(shortcut)
pyproject.toml
    [project]
    name = "test"
    version = "0.1.2.3"
    dependencies = ["pywin32"]

    [tool.cxfreeze]
    executables = ["test.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.xfail(
    ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="pywin32 does not support Python 3.13t/3.14t",
    strict=True,
)
@pytest.mark.venv(scope="module")
@zip_packages
def test_win32com_shell(tmp_package, zip_packages: bool) -> None:
    """Test if win32com hook is working correctly."""
    tmp_package.create(SOURCE_WIN32COM_SHELL)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines("<PyIShellLink at*")
