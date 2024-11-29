"""Test winmsvcr."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX, IS_MINGW, IS_WINDOWS

if TYPE_CHECKING:
    from pathlib import Path

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

SOURCE = """
hello.py
    print("Hello from cx_Freeze")
command
    cxfreeze --script hello.py build_exe --silent --excludes=tkinter
"""


@pytest.mark.skipif(not IS_WINDOWS, reason="Windows tests")
def test_files() -> None:
    """Test MSVC files."""
    from cx_Freeze.winmsvcr import FILES

    assert EXPECTED == FILES


@pytest.mark.skipif(not (IS_MINGW or IS_WINDOWS), reason="Windows tests")
@pytest.mark.parametrize("include_msvcr", [False, True], ids=["no", "yes"])
def test_build_exe_with_include_msvcr(
    tmp_path: Path, include_msvcr: bool
) -> None:
    """Test the simple sample with include_msvcr option."""
    create_package(tmp_path, SOURCE)
    if include_msvcr:
        with tmp_path.joinpath("command").open("a") as f:
            f.write(" --include-msvcr")
    output = run_command(tmp_path)

    build_exe_dir = tmp_path / BUILD_EXE_DIR
    executable = build_exe_dir / f"hello{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    assert output.startswith("Hello from cx_Freeze")

    names = [
        file.name.lower()
        for file in build_exe_dir.glob("*.dll")
        if any(filter(file.match, EXPECTED))
    ]
    # include-msvcr copies the files only on Windows, but not in MingW
    if IS_WINDOWS and include_msvcr:
        assert names != []
    else:
        assert not names
