"""Tests for some cx_Freeze.hooks."""

from __future__ import annotations

import sys

import pytest

if sys.platform != "win32":
    pytest.skip(reason="Windows tests", allow_module_level=True)

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


@pytest.mark.venv
@zip_packages
def test_win32com(tmp_package, zip_packages: bool) -> None:
    """Test that the win32com is working correctly."""
    command = "cxfreeze --script test_win32com.py --excludes=tkinter,unittest"
    if zip_packages:
        command += " --zip-include-packages=* --zip-exclude-packages="
    command += " --include-msvcr --silent"

    tmp_package.create_from_sample("win32com")
    # pywin32 must be installed on venv
    tmp_package.install("pywin32", isolated=False)
    output = tmp_package.run(command)
    executable = tmp_package.executable("test_win32com")
    assert executable.is_file()

    output = tmp_package.run(executable, timeout=10)
    lines = output.splitlines()
    assert lines[0].startswith("Sent and received 'Hello from cx_Freeze'")
    assert lines[-1].startswith("Everything seemed to work!")
    assert len(lines) == 5, lines


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

    [tool.cxfreeze]
    executables = ["test.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.venv
@zip_packages
def test_win32com_shell(tmp_package, zip_packages: bool) -> None:
    """Test if zoneinfo hook is working correctly."""
    tmp_package.create(SOURCE_WIN32COM_SHELL)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    # pywin32 must be installed on venv
    tmp_package.install("pywin32", isolated=False)
    output = tmp_package.run()
    executable = tmp_package.executable("test")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    print(output)
    lines = output.splitlines()
    assert lines[0].startswith("<PyIShellLink at")
