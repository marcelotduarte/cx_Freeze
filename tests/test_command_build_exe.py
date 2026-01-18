"""Tests for cx_Freeze.command.build_exe."""

from __future__ import annotations

import os

import pytest
from setuptools import Distribution

from cx_Freeze._compat import BUILD_EXE_DIR, IS_UCRT
from cx_Freeze.command.build_exe import build_exe
from cx_Freeze.exception import SetupError

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "executables": ["hello.py"],
    "script_name": "setup.py",
}


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        pytest.param(
            {"build_exe": None},
            {"build_exe": os.path.normpath(BUILD_EXE_DIR)},
            id="build-exe=none",
        ),
        pytest.param(
            {"build_exe": "dist"}, {"build_exe": "dist"}, id="build-exe=dist"
        ),
        pytest.param(
            {"excludes": "tkinter,unittest"},
            {"excludes": ["tkinter", "unittest"]},
            id="excludes='tkinter,unittest'",
        ),
        pytest.param(
            {"excludes": ["tkinter", "unittest"]},
            {"excludes": ["tkinter", "unittest"]},
            id="excludes=['tkinter','unittest']",
        ),
        pytest.param(
            {"include_msvcr": None},
            {"include_msvcr": False},
            id="include-msvcr=none",
        ),
        pytest.param(
            {"include_msvcr": False},
            {"include_msvcr": False},
            id="include-msvcr=false",
        ),
        pytest.param(
            {"include_msvcr": True},
            {"include_msvcr": IS_UCRT},
            id="include-msvcr=true",
        ),
        pytest.param(
            {"include_msvcr_version": "15"},
            {"include_msvcr": IS_UCRT, "include_msvcr_version": "15"},
            id="include-msvcr-version=15",
        ),
        pytest.param(
            {"include_msvcr_version": "16"},
            {"include_msvcr": IS_UCRT, "include_msvcr_version": "16"},
            id="include-msvcr-version=16",
        ),
        pytest.param(
            {"include_msvcr_version": "17"},
            {"include_msvcr": IS_UCRT, "include_msvcr_version": "17"},
            id="include-msvcr-version=17",
        ),
        pytest.param(
            {"replace_paths": [("*", "")]},
            {"replace_paths": [("*", "")]},
            id="replace_paths=*",
        ),
        pytest.param(
            {"replace_paths": "*="},
            {"replace_paths": ["*="]},
            id="replace_paths=*=",
        ),
        pytest.param(
            {"replace_paths": ["*="]},
            {"replace_paths": ["*="]},
            id="replace_paths=[*=]",
        ),
        pytest.param({"silent": None}, {"silent": 0}, id="silent=none->0"),
        pytest.param({"silent": False}, {"silent": 0}, id="silent=false->0"),
        pytest.param({"silent": True}, {"silent": 1}, id="silent=true->1"),
        pytest.param(
            {"silent_level": None}, {"silent": 0}, id="silent-level=none->0"
        ),
        pytest.param(
            {"silent_level": 0}, {"silent": 0}, id="silent-level=0->0"
        ),
        pytest.param(
            {"silent_level": 1}, {"silent": 1}, id="silent-level=1->1"
        ),
        pytest.param(
            {"silent_level": 2}, {"silent": 2}, id="silent-level=2->2"
        ),
        pytest.param(
            {"silent_level": "3"}, {"silent": 3}, id="silent-level=3->3"
        ),
        pytest.param(
            {"zip_include_packages": None, "zip_exclude_packages": None},
            {"zip_include_packages": [], "zip_exclude_packages": []},
            id="zip_include_packages/zip_exclude_packages=none/none",
        ),
        pytest.param(
            {"zip_include_packages": ["*"], "zip_exclude_packages": None},
            {"zip_include_packages": ["*"], "zip_exclude_packages": []},
            id="zip_include_package=[*]",
        ),
        pytest.param(
            {"zip_include_packages": None, "zip_exclude_packages": ["*"]},
            {"zip_include_packages": [], "zip_exclude_packages": ["*"]},
            id="zip_exclude_packages=*",
        ),
        pytest.param(  # zip_*_packages are namespace packages
            {
                "zip_include_packages": ["namespace.test"],
                "zip_exclude_packages": ["zope.event", "zope.interface"],
            },
            {
                "zip_include_packages": ["namespace.test"],
                "zip_exclude_packages": ["zope.event", "zope.interface"],
            },
            id="zip_include_packages/zip_exclude_packages=namespace/namespace",
        ),
        pytest.param(
            {"zip_include_packages": "*", "zip_exclude_packages": []},
            {"zip_include_packages": ["*"], "zip_exclude_packages": []},
            id="zip_include_package=*",
        ),
        pytest.param(
            {"zip_filename": None},
            {"zip_filename": "library.zip"},
            id="zip_filename=none",
        ),
        pytest.param(
            {"zip_filename": "test"},
            {"zip_filename": "test.zip"},
            id="zip_filename=test",
        ),
        pytest.param(
            {"zip_filename": "test.zip"},
            {"zip_filename": "test.zip"},
            id="zip_filename=test.zip",
        ),
        pytest.param(
            {},
            {"no_compress": False, "zip_filename": "library.zip"},
            id="zip_filename=",
        ),
        pytest.param(
            {"no_compress": None},
            {"no_compress": False, "zip_filename": "library.zip"},
            id="zip_filename=",
        ),
        pytest.param(
            {"no_compress": False},
            {"no_compress": False, "zip_filename": "library.zip"},
            id="no_compress=false",
        ),
        pytest.param(
            {"no_compress": True},
            {"no_compress": True, "zip_filename": None},
            id="no_compress=true",
        ),
    ],
)
def test_build_exe_finalize_options(
    kwargs: dict[str, ...], expected: dict[str, ...]
) -> None:
    """Test the build_exe finalize_options."""
    dist = Distribution(DIST_ATTRS)
    cmd = build_exe(dist, **kwargs)
    cmd.finalize_options()
    for option, value in expected.items():
        assert getattr(cmd, option) == value


@pytest.mark.parametrize(
    ("kwargs", "expected_exception", "expected_match"),
    [
        pytest.param(
            {"build_exe": "build"},
            SetupError,
            "build_exe option cannot be the same as build_base directory",
            id="build-exe=build",
        ),
    ],
)
def test_build_exe_finalize_options_raises(
    kwargs: dict[str, ...], expected_exception, expected_match: str
) -> None:
    """Test the build_exe finalize_options that raises an exception."""
    dist = Distribution(DIST_ATTRS)
    cmd = build_exe(dist, **kwargs)
    with pytest.raises(expected_exception, match=expected_match):
        cmd.finalize_options()


@pytest.mark.parametrize(
    ("build_args", "expected"),
    [
        pytest.param(
            [],
            {"build_exe": os.path.normpath(BUILD_EXE_DIR)},
            id="--build-exe(notused)",
        ),
        pytest.param(
            ["--build-exe="],
            {"build_exe": os.path.normpath(BUILD_EXE_DIR)},
            id="--build-exe=",
        ),
        pytest.param(
            ["--build-exe=dist"], {"build_exe": "dist"}, id="--build-exe=dist"
        ),
        pytest.param(["--excludes="], {"excludes": []}, id="--excludes="),
        pytest.param(
            ["--excludes=tkinter,unittest"],
            {"excludes": ["tkinter", "unittest"]},
            id="--excludes=tkinter,unittest",
        ),
        pytest.param(["--includes="], {"includes": []}, id="--includes="),
        pytest.param(
            ["--includes=tkinter,unittest"],
            {"includes": ["tkinter", "unittest"]},
            id="--includes=tkinter,unittest",
        ),
        pytest.param(["--packages="], {"packages": []}, id="--packages="),
        pytest.param(
            ["--packages=tkinter,unittest"],
            {"packages": ["tkinter", "unittest"]},
            id="--packages=tkinter,unittest",
        ),
        pytest.param(
            ["--replace-paths=*="],
            {"replace_paths": ["*="]},
            id="--replace-paths=*=",
        ),
        pytest.param(
            ["--bin-excludes="], {"bin_excludes": []}, id="--bin-excludes="
        ),
        pytest.param(
            ["--bin-includes="], {"bin_includes": []}, id="--bin-includes="
        ),
        pytest.param(
            ["--bin-path-excludes="],
            {"bin_path_excludes": []},
            id="--bin-path-excludes=",
        ),
        pytest.param(
            ["--bin-path-includes="],
            {"bin_path_includes": []},
            id="--bin-path-includes=",
        ),
        pytest.param(
            ["--include-files="], {"include_files": []}, id="--include-files="
        ),
        pytest.param(
            ["--zip-includes="], {"zip_includes": []}, id="--zip-includes="
        ),
        pytest.param(
            [],
            {"zip_include_packages": [], "zip_exclude_packages": ["*"]},
            id="--zip-include-packages/--zip-exclude-packages(notused)",
        ),
        pytest.param(
            ["--zip-include-packages=", "--zip-exclude-packages="],
            {"zip_include_packages": [], "zip_exclude_packages": []},
            id="--zip-include-packages=/--zip-exclude-packages=",
        ),
        pytest.param(
            ["--zip-include-packages=*", "--zip-exclude-packages="],
            {"zip_include_packages": ["*"], "zip_exclude_packages": []},
            id="--zip-include-package=*/--zip-exclude-packages=",
        ),
        pytest.param(
            ["--zip-include-packages=", "--zip-exclude-packages=*"],
            {"zip_include_packages": [], "zip_exclude_packages": ["*"]},
            id="--zip-include-packages=/--zip-exclude-packages=*",
        ),
        pytest.param(  # zip_*_packages are namespace packages
            [
                "--zip-include-packages=namespace.test",
                "--zip-exclude-packages=zope.event,zope.interface",
            ],
            {
                "zip_include_packages": ["namespace.test"],
                "zip_exclude_packages": ["zope.event", "zope.interface"],
            },
            id="--zip-include-packages/--zip-exclude-packages=namespace/namespace",
        ),
        pytest.param(
            ["--zip-filename="],
            {"zip_filename": "library.zip"},
            id="--zip-filename=",
        ),
        pytest.param(
            ["--zip-filename=test"],
            {"zip_filename": "test.zip"},
            id="--zip-filename=test",
        ),
        pytest.param(
            ["--zip-filename=test.zip"],
            {"zip_filename": "test.zip"},
            id="--zip-filename=test.zip",
        ),
        pytest.param(
            [],
            {"no_compress": False, "zip_filename": "library.zip"},
            id="--no-compress(notused),--zip-filename(notused)",
        ),
        pytest.param(
            ["--no-compress"],
            {"no_compress": True, "zip_filename": None},
            id="--no-compress",
        ),
        pytest.param([], {"optimize": 0}, id="--optimize(notused)"),
        pytest.param(["--optimize=0"], {"optimize": 0}, id="--optimize=0"),
        pytest.param(["--optimize=1"], {"optimize": 1}, id="--optimize=1"),
        pytest.param(["--optimize=2"], {"optimize": 2}, id="--optimize=2"),
        pytest.param(["-O0"], {"optimize": 0}, id="--optimize(-O0"),
        pytest.param(["-O1"], {"optimize": 1}, id="--optimize(-O1"),
        pytest.param(["-O2"], {"optimize": 2}, id="--optimize(-O2"),
        pytest.param([], {"silent": 0}, id="--silent(notused)"),
        pytest.param(["--silent"], {"silent": 1}, id="--silent"),
        pytest.param(
            ["--silent-level=0"], {"silent": 0}, id="--silent-level=0->0"
        ),
        pytest.param(
            ["--silent-level=1"], {"silent": 1}, id="--silent-level=1->1"
        ),
        pytest.param(
            ["--silent-level=2"], {"silent": 2}, id="--silent-level=2->2"
        ),
        pytest.param(
            ["--silent-level=3"], {"silent": 3}, id="--silent-level=3->3"
        ),
        pytest.param(
            [], {"include_msvcr": False}, id="--include-msvcr(notused)"
        ),
        pytest.param(
            ["--include-msvcr"],
            {"include_msvcr": IS_UCRT},
            id="--include-msvcr",
        ),
        pytest.param(
            ["--include-msvcr-version=15"],
            {"include_msvcr": IS_UCRT, "include_msvcr_version": "15"},
            id="--include-msvcr-version=15",
        ),
        pytest.param(
            ["--include-msvcr-version=16"],
            {"include_msvcr": IS_UCRT, "include_msvcr_version": "16"},
            id="--include-msvcr-version=16",
        ),
        pytest.param(
            ["--include-msvcr-version=17"],
            {"include_msvcr": IS_UCRT, "include_msvcr_version": "17"},
            id="--include-msvcr-version=17",
        ),
    ],
)
def test_build_exe_script_args(
    build_args: list[str], expected: dict[str, ...]
) -> None:
    """Test the build_exe with command line parameters."""
    attrs = DIST_ATTRS.copy()
    attrs["script_args"] = ["build_exe", *build_args]
    dist = Distribution(attrs)
    dist.parse_command_line()
    dist.dump_option_dicts()
    cmd_obj = dist.get_command_obj("build_exe")
    cmd_obj.ensure_finalized()
    for option, value in expected.items():
        assert getattr(cmd_obj, option) == value


def test_build_exe_asmodule(tmp_package) -> None:
    """Test the asmodule sample."""
    tmp_package.create_from_sample("asmodule")
    tmp_package.freeze(
        "python setup.py build_exe"
        " --excludes=tkinter,unittest --include-msvcr --silent"
    )

    executable = tmp_package.executable("asmodule")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")


SOURCE_ADV = """\
test1.py
    import importlib.metadata
    import foobar.baz

    print("version", importlib.metadata.version("foobar"))
test2.py
    __import__("second")
pyproject.toml
    [project]
    name = "foobar"
    version = "0.0.1"
    description = "Sample cx_Freeze script"

    [[tool.cxfreeze.executables]]
    script = "test1.py"

    [[tool.cxfreeze.executables]]
    script = "test2.py"

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "unittest"]
    include_msvcr = true
    include_path = "extra"
    silent = true
foobar/__init__.py
    print("This is foobar")
foobar/baz.py
    print("This is foobar.baz")
extra/second.py
    print("This is second")
"""


@pytest.mark.parametrize(
    "zip_packages",
    [None, False, True],
    ids=["", "zip_exclude_packages", "zip_include_packages"],
)
def test_build_exe_advanced(tmp_package, zip_packages: bool | None) -> None:
    """Test an advanced sample."""
    tmp_package.create(SOURCE_ADV)
    pyproject = tmp_package.path / "pyproject.toml"
    buf = pyproject.read_bytes().decode().splitlines()
    if zip_packages is False:
        buf += ['zip_exclude_packages = "*"', 'zip_include_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    elif zip_packages is True:
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test1")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=10)
    result.stdout.fnmatch_lines(
        ["This is foobar", "This is foobar.baz", "version 0.0.1"]
    )

    executable = tmp_package.executable("test2")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=10)
    result.stdout.fnmatch_lines(["This is second"])


def test_egg_info(tmp_package) -> None:
    """Test version update."""
    tmp_package.create(SOURCE_ADV)
    # update the version in the pyproject
    pyproject = tmp_package.path / "pyproject.toml"
    buf = pyproject.read_bytes().replace(b"0.0.1", b"0.0.2")
    pyproject.write_bytes(buf)
    tmp_package.freeze()

    executable = tmp_package.executable("test1")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=10)
    result.stdout.fnmatch_lines(
        ["This is foobar", "This is foobar.baz", "version 0.0.2"]
    )

    # new update
    pyproject.write_bytes(buf.replace(b"0.0.2", b"0.0.3"))
    tmp_package.freeze("cxfreeze build_exe")

    executable = tmp_package.executable("test1")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=10)
    result.stdout.fnmatch_lines(
        ["This is foobar", "This is foobar.baz", "version 0.0.3"]
    )
