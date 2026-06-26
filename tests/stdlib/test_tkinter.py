"""Tests for hooks of stdlib tkinter."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

from cx_Freeze._compat import IS_MACOS

if TYPE_CHECKING:
    from tests.conftest import TempPackage

TIMEOUT = 15

if IS_MACOS:
    mac_extra_test = pytest.mark.parametrize(
        "mac_extra_test", [False, True], ids=["", "mac_extra_test"]
    )
else:
    mac_extra_test = pytest.mark.parametrize(
        "mac_extra_test", [False], ids=[""]
    )
zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


SOURCE_TEST_TK = """
test_tk.py
    import tkinter

    root = tkinter.Tk(useTk=False)
    print(root.tk.exprstring("$tcl_library"))
pyproject.toml
    [project]
    name = "test_tk"
    version = "0.1.2.3"

    [tool.cxfreeze]
    executables = ["test_tk.py"]

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["unittest"]
    silent = true
"""


@mac_extra_test
@zip_packages
def test_tkinter(
    tmp_package: TempPackage, zip_packages: bool, mac_extra_test: bool
) -> None:
    """Test if tkinter hook is working correctly."""
    pytest.importorskip("tkinter", reason="Depends on extra package: tkinter")

    tmp_package.create(SOURCE_TEST_TK)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    if mac_extra_test:
        tmp_package.freeze("cxfreeze bdist_mac")
        name = "test_tk"
        version = "0.1.2.3"
        bundle_name = f"{name}-{version}"
        build_app_dir = tmp_package.path / "build" / f"{bundle_name}.app"
        executable = build_app_dir / "Contents/MacOS/test_tk"
        expected = os.path.normpath(
            build_app_dir / "Contents/Resources/share/tcl"
        )
    else:
        tmp_package.freeze()
        executable = tmp_package.executable("test_tk")
        expected = os.path.normpath(executable.parent / "share/tcl")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    # Compare the start of the returned path, version independent.
    # This is necessary when the OS has an older tcl/tk version than the
    # version contained in the cx_Freeze wheels.
    result.stdout.fnmatch_lines(f"{expected}*")
