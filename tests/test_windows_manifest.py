"""Tests for some cx_Freeze.hooks."""

from __future__ import annotations

import ctypes
import sys
from importlib.metadata import PackageNotFoundError, distribution
from typing import TYPE_CHECKING

import pytest

from cx_Freeze._compat import (
    ABI_THREAD,
    IS_CONDA,
    IS_MINGW,
    IS_WINDOWS,
)
from cx_Freeze.dep_parser import PEParser

if TYPE_CHECKING:
    from .conftest import TempPackage

SOURCE = """
test_manifest.py
    import sys

    winver = sys.getwindowsversion()
    print(f"Windows version: {winver.major}.{winver.minor}")
pyproject.toml
    [project]
    name = "test_manifest"
    version = "0.1.2.3"
    description = "Sample for test with cx_Freeze"

    [[tool.cxfreeze.executables]]
    script = "test_manifest.py"

    [[tool.cxfreeze.executables]]
    script = "test_manifest.py"
    manifest = "simple.manifest"
    target-name = "test_simple_manifest"

    [[tool.cxfreeze.executables]]
    script = "test_manifest.py"
    uac-admin = true
    target-name = "test_uac_admin"

    [[tool.cxfreeze.executables]]
    script = "test_manifest.py"
    uac-admin = true
    uac-uiaccess = true
    target-name = "test_uac_uiaccess"

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
simple.manifest
    <?xml version='1.0' encoding='UTF-8' standalone='yes'?>
    <assembly xmlns='urn:schemas-microsoft-com:asm.v1' manifestVersion='1.0'>
      <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
        <security>
          <requestedPrivileges>
            <requestedExecutionLevel level='asInvoker' uiAccess='false' />
          </requestedPrivileges>
        </security>
      </trustInfo>
    </assembly>
"""


@pytest.mark.skipif(not (IS_MINGW or IS_WINDOWS), reason="Windows tests")
def test_manifest(tmp_package: TempPackage) -> None:
    """With the correct manifest, windows version return 10.0 in Windows 10."""
    tmp_package.create(SOURCE)
    tmp_package.freeze()
    executable = tmp_package.executable("test_manifest")
    assert executable.is_file()
    result = tmp_package.run(executable)
    winver = sys.getwindowsversion()  # ty: ignore[unresolved-attribute]
    expected = f"Windows version: {winver.major}.{winver.minor}"
    result.stdout.fnmatch_lines(expected)


LIEF_VERSIONS = []
if IS_WINDOWS:
    if IS_CONDA:
        LIEF_VERSIONS.append("installed")
    elif ABI_THREAD == "":  # lief doesn't support free-threaded yet
        if sys.version_info[:2] <= (3, 13):
            LIEF_VERSIONS.append("0.16.0")
            LIEF_VERSIONS.append("0.16.6")
        LIEF_VERSIONS.append("0.17.0")
        LIEF_VERSIONS.append("0.17.6")
elif IS_MINGW:
    LIEF_VERSIONS.append("installed")


@pytest.mark.skipif(not (IS_MINGW or IS_WINDOWS), reason="Windows tests")
@pytest.mark.parametrize("lief_version", [*LIEF_VERSIONS, "disabled"])
def test_simple_manifest(tmp_package: TempPackage, lief_version: str) -> None:
    """Tests a simple manifest, without "supportedOS Id".

    The returned windows version is the compatible version for Windows 8.1,
    ie, 6.2.
    """
    tmp_package.create(SOURCE)
    if lief_version == "disabled":
        tmp_package.monkeypatch.setenv("CX_FREEZE_BIND", "imagehlp")
    elif lief_version == "installed":
        try:
            distribution("lief")
        except PackageNotFoundError:
            print("WARNING: LIEF is not installed")
            lief_version = "disabled"
    else:
        tmp_package.install(f"lief=={lief_version}")
    tmp_package.freeze()
    executable = tmp_package.executable("test_simple_manifest")
    assert executable.is_file()
    result = tmp_package.run(executable)
    if lief_version == "disabled":
        expected = "Windows version: 10.0"
    else:
        expected = "Windows version: 6.2"
    result.stdout.fnmatch_lines(expected)

    parser = PEParser([], [], 0, {})
    manifest = parser.read_manifest(executable)
    if lief_version == "disabled":
        assert manifest is None
    else:
        simple = tmp_package.path / "simple.manifest"
        assert manifest == simple.read_bytes().decode()


@pytest.mark.skipif(not (IS_MINGW or IS_WINDOWS), reason="Windows tests")
@pytest.mark.parametrize("lief_version", LIEF_VERSIONS)
def test_uac_admin(tmp_package: TempPackage, lief_version: str) -> None:
    """With the uac_admin, should return WinError 740 - requires elevation."""
    if ctypes.windll.shell32.IsUserAnAdmin():  # ty: ignore[unresolved-attribute]
        pytest.xfail(reason="User is admin")

    tmp_package.create(SOURCE)
    if lief_version != "installed":
        tmp_package.install(f"lief=={lief_version}")
    tmp_package.freeze()
    executable = tmp_package.executable("test_uac_admin")
    assert executable.is_file()
    with pytest.raises(OSError, match=r"[WinError 740]"):
        tmp_package.run(executable)


@pytest.mark.skipif(not (IS_MINGW or IS_WINDOWS), reason="Windows tests")
@pytest.mark.parametrize("lief_version", LIEF_VERSIONS)
def test_uac_uiaccess(tmp_package: TempPackage, lief_version: str) -> None:
    """With the uac_uiaccess, should return WinError 740."""
    if ctypes.windll.shell32.IsUserAnAdmin():  # ty: ignore[unresolved-attribute]
        pytest.xfail(reason="User is admin")

    tmp_package.create(SOURCE)
    if lief_version != "installed":
        tmp_package.install(f"lief=={lief_version}")
    tmp_package.freeze()
    executable = tmp_package.executable("test_uac_uiaccess")
    assert executable.is_file()
    with pytest.raises(OSError, match=r"[WinError 740]"):
        tmp_package.run(executable)
