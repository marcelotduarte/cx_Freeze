"""Test winmsvcr."""

from __future__ import annotations

import pytest

from cx_Freeze._compat import IS_MINGW, IS_WINDOWS

MSVC_EXPECTED = (
    # VC 2015 and 2017
    "concrt140.dll",
    "msvcp140.dll",
    "msvcp140_1.dll",
    "msvcp140_2.dll",
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

UCRT_EXPECTED = (
    "api-ms-win-*.dll",
    "ucrtbase.dll",
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
    from cx_Freeze.winmsvcr import MSVC_FILES, UCRT_FILES

    assert MSVC_EXPECTED == MSVC_FILES
    assert UCRT_EXPECTED == UCRT_FILES


@pytest.mark.skipif(not (IS_MINGW or IS_WINDOWS), reason="Windows tests")
@pytest.mark.parametrize(
    "extra_option",
    [
        "",
        "--include-msvcr",
        "--include-msvcr-version=15",
        "--include-msvcr-version=16",
        "--include-msvcr-version=17",
    ],
)
def test_build_exe_with(tmp_package, extra_option: str) -> None:
    """Test the simple sample with include_msvcr option."""
    tmp_package.create(SOURCE)
    if extra_option:
        with tmp_package.path.joinpath("command").open("a") as f:
            f.write(f" {extra_option}")
    output = tmp_package.run()

    executable = tmp_package.executable("hello")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    assert output.startswith("Hello from cx_Freeze")

    expected = [*MSVC_EXPECTED]
    if extra_option.endswith("15"):
        expected.extend(UCRT_EXPECTED)
    build_exe_dir = executable.parent
    names = [
        file.name.lower()
        for file in build_exe_dir.glob("*.dll")
        if any(filter(file.match, expected))
    ]
    # include-msvcr copies the files only on Windows, but not in MingW
    if IS_WINDOWS and extra_option:
        assert names != []
    else:
        assert not names
