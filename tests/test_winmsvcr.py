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
pyproject.toml
    [project]
    name = "hello"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"

    [[tool.cxfreeze.executables]]
    script = "hello.py"

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "unittest"]
    silent = true
    {extra_option}
"""


@pytest.mark.skipif(not IS_WINDOWS, reason="Windows tests")
def test_files() -> None:
    """Test MSVC files."""
    from cx_Freeze.winmsvcr import MSVC_FILES, UCRT_FILES

    assert MSVC_EXPECTED == MSVC_FILES
    assert UCRT_EXPECTED == UCRT_FILES


@pytest.mark.skipif(not (IS_MINGW or IS_WINDOWS), reason="Windows tests")
@pytest.mark.parametrize(
    "include_msvcr",
    [False, True, 15, 16, 17],
)
def test_build_exe_with(tmp_package, include_msvcr: bool | int | None) -> None:
    """Test the simple sample with include_msvcr option."""
    if isinstance(include_msvcr, int):
        extra_option = f"include_msvcr_version = {include_msvcr}"
    elif include_msvcr:
        extra_option = "include_msvcr = true"
    else:
        extra_option = ""
    tmp_package.create(SOURCE.format(extra_option=extra_option))
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


@pytest.mark.parametrize(
    ("platform", "version"),
    [
        ("win32", "15"),
        ("win-amd64", "15"),
        ("win-arm64", "15"),
        ("win32", "16"),
        ("win-amd64", "16"),
        ("win-arm64", "16"),
        ("win32", "17"),
        ("win-amd64", "17"),
        ("win-arm64", "17"),
    ],
)
def test_versions(tmp_package, platform: str, version: int) -> None:
    """Test the downloads of all versions of msvcr."""
    from cx_Freeze.winmsvcr_repack import copy_msvcr_files

    if not (IS_MINGW or IS_WINDOWS):
        tmp_package.install("cabarchive")
        tmp_package.install("striprtf")

    copy_msvcr_files(tmp_package.path, platform, version)
    expected = [*MSVC_EXPECTED]
    if version == "15":
        expected.extend(UCRT_EXPECTED)
    names = [
        file.name.lower()
        for file in tmp_package.path.glob("*.dll")
        if any(filter(file.match, expected))
    ]
    assert names != []


def test_nocache(tmp_package) -> None:
    """Test the downloads of all versions of msvcr."""
    from cx_Freeze.winmsvcr_repack import copy_msvcr_files

    if not (IS_MINGW or IS_WINDOWS):
        tmp_package.install("cabarchive")
        tmp_package.install("striprtf")

    copy_msvcr_files(tmp_package.path, "win-amd64", "17", no_cache=True)
    names = [
        file.name.lower()
        for file in tmp_package.path.glob("*.dll")
        if any(filter(file.match, MSVC_EXPECTED))
    ]
    assert names != []


def test_repack_main(tmp_package) -> None:
    """Test the cx_Freeze.winmsvcr_repack __main_ entry point."""
    from cx_Freeze.winmsvcr_repack import main_test

    if not (IS_MINGW or IS_WINDOWS):
        tmp_package.install("cabarchive")
        tmp_package.install("striprtf")

    main_test(
        args=[
            f"--target-dir={tmp_package.path}",
            "--target-platform=win-amd64",
            "--version=17",
        ]
    )
    names = [
        file.name.lower()
        for file in tmp_package.path.glob("*.dll")
        if any(filter(file.match, MSVC_EXPECTED))
    ]
    assert names != []


def test_repack_main_no_option(tmp_package) -> None:
    """Test argparse error exception."""
    from cx_Freeze.winmsvcr_repack import main_test

    if not (IS_MINGW or IS_WINDOWS):
        tmp_package.install("cabarchive")
        tmp_package.install("striprtf")

    main_test(args=[])
    names = [
        file.name.lower()
        for file in tmp_package.path.glob("dist/*.dll")
        if any(filter(file.match, MSVC_EXPECTED))
    ]
    assert names != []
