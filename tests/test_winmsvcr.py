"""Test winmsvcr."""

from __future__ import annotations

import sys
from pathlib import Path
from sysconfig import get_platform, get_python_version

import pytest
from generate_samples import run_command

from cx_Freeze.winmsvcr import FILES

EXPECTED = (
    "api-ms-win-*.dll",
    # VC 2015 and 2017
    "concrt140.dll",
    "msvcp140_1.dll",
    "msvcp140_2.dll",
    "msvcp140.dll",
    "ucrtbase.dll",
    "vcamp140.dll",
    "vccorlib140.dll",
    "vcomp140.dll",
    "vcruntime140.dll",
    # VS 2019
    "msvcp140_atomic_wait.dll",
    "msvcp140_codecvt_ids.dll",
    "vcruntime140_1.dll",
    # VS 2022
    "vcruntime140_threads.dll",
)

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"
BUILD_EXE_CMD = "python setup.py build_exe --silent --excludes=tkinter"
IS_WINDOWS = sys.platform == "win32"
SUFFIX = ".exe" if IS_WINDOWS else ""


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
def test_files() -> None:
    """Test winmsvcr.FILES."""
    assert EXPECTED == FILES


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
@pytest.mark.parametrize("include_msvcr", [False, True], ids=["no", "yes"])
@pytest.mark.datafiles(SAMPLES_DIR / "sqlite")
def test_build_exe_with_include_msvcr(
    datafiles: Path, include_msvcr: bool
) -> None:
    """Test the simple sample with include_msvcr option."""
    command = BUILD_EXE_CMD
    if include_msvcr:
        command += " --include-msvcr"
    output = run_command(datafiles, command)

    build_exe_dir = datafiles / BUILD_EXE_DIR

    executable = build_exe_dir / f"test_sqlite3{SUFFIX}"
    assert executable.is_file()
    output = run_command(datafiles, executable, timeout=10)
    assert output.startswith("dump.sql created")

    names = [
        file.name.lower()
        for file in build_exe_dir.glob("*.dll")
        if any(filter(file.match, EXPECTED))
    ]
    if include_msvcr:
        assert names != []
    else:
        assert names == []
