"""Test winmsvcr."""

from __future__ import annotations

import pytest

from cx_Freeze._compat import IS_CONDA, IS_MACOS, IS_MINGW, IS_WINDOWS
from cx_Freeze.winmsvcr_repack import copy_msvcr_files

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
@pytest.mark.parametrize("value", [False, True, "15", "16", "17"])
def test_build_with_include_msvcr(tmp_package, value: bool | str) -> None:
    """Test the simple sample with include_msvcr option."""
    if isinstance(value, str):
        extra_option = f"include_msvcr_version = {value!r}"
    elif isinstance(value, bool) and value:
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
    if isinstance(value, str) and value == "15":
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


# Test only on Windows and Linux (not conda on Linux)
@pytest.mark.skipif(IS_CONDA and not IS_WINDOWS, reason="Windows tests")
@pytest.mark.skipif(IS_MACOS, reason="Windows tests")
@pytest.mark.skipif(IS_MINGW, reason="Disabled in MinGW")
@pytest.mark.parametrize(
    ("version", "platform", "no_cache"),
    [
        ("15", "win32", False),
        ("15", "win-amd64", False),
        ("15", "win-arm64", False),
        ("16", "win32", False),
        ("16", "win-amd64", False),
        ("16", "win-arm64", False),
        ("17", "win32", False),
        ("17", "win-amd64", True),  # just one no_cache is enough
        ("17", "win-arm64", False),
    ],
)
def test_versions(
    tmp_package, version: int, platform: str, no_cache: bool
) -> None:
    """Test the downloads of all versions of msvcr."""
    if not (IS_MINGW or IS_WINDOWS):
        tmp_package.install(["cabarchive", "striprtf"])

    copy_msvcr_files(tmp_package.path, platform, version, no_cache=no_cache)
    expected = [*MSVC_EXPECTED]
    if version == "15":
        expected.extend(UCRT_EXPECTED)
    names = [
        file.name.lower()
        for file in tmp_package.path.glob("*.dll")
        if any(filter(file.match, expected))
    ]
    assert names != []


@pytest.mark.skipif(IS_CONDA and not IS_WINDOWS, reason="Windows tests")
@pytest.mark.skipif(IS_MACOS, reason="Windows tests")
@pytest.mark.parametrize(
    ("version", "platform", "expected_exception", "expected_match"),
    [
        (17, "win-amd64", RuntimeError, "Version is not expected"),
        ("18", "win-amd64", RuntimeError, "Version is not expected"),
        ("17", "", RuntimeError, "Architecture not supported"),
        ("17", "win64", RuntimeError, "Architecture not supported"),
    ],
)
def test_invalid(
    tmp_package, version, platform, expected_exception, expected_match
) -> None:
    """Test invalid values to use with copy_msvcr_files function."""
    if not (IS_MINGW or IS_WINDOWS):
        tmp_package.install(["cabarchive", "striprtf"])

    with pytest.raises(expected_exception, match=expected_match):
        copy_msvcr_files(tmp_package.path, platform, version)


@pytest.mark.skipif(IS_CONDA and not IS_WINDOWS, reason="Windows tests")
@pytest.mark.skipif(IS_MACOS, reason="Windows tests")
@pytest.mark.skipif(IS_MINGW, reason="Disabled in MinGW")
def test_repack_main(tmp_package) -> None:
    """Test the cx_Freeze.winmsvcr_repack __main_ entry point with args."""
    from cx_Freeze.winmsvcr_repack import main_test

    if not (IS_MINGW or IS_WINDOWS):
        tmp_package.install(["cabarchive", "striprtf"])

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


@pytest.mark.skipif(IS_CONDA and not IS_WINDOWS, reason="Windows tests")
@pytest.mark.skipif(IS_MACOS, reason="Windows tests")
@pytest.mark.skipif(IS_MINGW, reason="Disabled in MinGW")
def test_repack_main_no_option(tmp_package) -> None:
    """Test the cx_Freeze.winmsvcr_repack __main_ entry point without args."""
    from cx_Freeze.winmsvcr_repack import main_test

    if not (IS_MINGW or IS_WINDOWS):
        tmp_package.install(["cabarchive", "striprtf"])

    main_test(args=[])
    names = [
        file.name.lower()
        for file in tmp_package.path.glob("dist/*.dll")
        if any(filter(file.match, MSVC_EXPECTED))
    ]
    assert names != []
