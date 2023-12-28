"""Test executables keyword (and Executable class)."""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from subprocess import check_output
from sysconfig import get_platform, get_python_version

import pytest
from generate_samples import create_package
from setuptools import Distribution

from cx_Freeze import Executable
from cx_Freeze.exception import OptionError, SetupError

FIXTURE_DIR = Path(__file__).resolve().parent
PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"
IS_WINDOWS = sys.platform == "win32"
SUFFIX = ".exe" if IS_WINDOWS else ""

SOURCE_PYPROJECT = """
test_simple1.py
    print("Hello from cx_Freeze")
pyproject.toml
    [project]
    name = "hello"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"

    [tool.distutils.build_exe]
    excludes = ["tkinter", "unittest"]
setup.py
    from cx_Freeze import setup

    setup(executables=["test_simple1.py"])
"""

SOURCE_SETUP = """
test_simple1.py
    print("Hello from cx_Freeze")
setup.py
    from cx_Freeze import Executable, setup

    executables = [
        "test_simple1.py",
        {"script": "test_simple1.py", "target_name": "test_simple2"},
        Executable("test_simple1.py", target_name="test_simple3"),
    ]

    setup(
        name="hello",
        version="0.1.2.3",
        description="Sample cx_Freeze script",
        executables=executables,
    )
"""

SOURCE_SETUP_CFG = """
test_simple1.py
    print("Hello from cx_Freeze")
setup.cfg
    [metadata]
    name = hello
    version = 0.1.2.3
    description = Sample cx_Freeze script

    [build_exe]
    excludes = tkinter,unittest
setup.py
    from cx_Freeze import setup

    setup(executables=["test_simple1.py"])
"""


@pytest.mark.parametrize(
    ("source", "number_of_executables"),
    [
        (SOURCE_PYPROJECT, 1),
        (SOURCE_SETUP, 3),
        (SOURCE_SETUP_CFG, 1),
    ],
    ids=["pyproject", "setup_py", "setup_cfg"],
)
def test_executables(tmp_path: Path, source: str, number_of_executables: int):
    """Test the executables option."""
    create_package(tmp_path, source)
    output = check_output(
        [sys.executable, "setup.py", "build_exe", "--silent"],
        text=True,
        cwd=os.fspath(tmp_path),
    )
    print(output)

    for i in range(1, number_of_executables):
        file_created = tmp_path / BUILD_EXE_DIR / f"test_simple{i}{SUFFIX}"
        assert file_created.is_file(), f"file not found: {file_created}"

        output = check_output([os.fspath(file_created)], text=True, timeout=10)
        assert output.startswith("Hello from cx_Freeze")


@pytest.mark.parametrize(
    ("option", "value", "result"),
    [
        ("base", None, "console-"),
        ("base", "console", "console-"),
        ("base", "gui", "Win32GUI-" if IS_WINDOWS else "console-"),
        ("base", "service", "Win32Service-" if IS_WINDOWS else "console-"),
        ("init_script", None, "console.py"),
        ("init_script", "console", "console.py"),
        ("target_name", None, f"test{SUFFIX}"),
        ("target_name", "test1", f"test1{SUFFIX}"),
        ("target_name", "test-0.1", f"test-0.1{SUFFIX}"),
        ("target_name", "test.exe", "test.exe"),
        ("icon", "icon", "icon.ico" if IS_WINDOWS else "icon.svg"),
    ],
)
def test_valid(option, value, result):
    """Test valid values to use in Executable class."""
    executable = Executable("test.py", **{option: value})
    returned = getattr(executable, option)
    if isinstance(returned, Path):
        returned = returned.name
    assert returned.startswith(result), returned


@pytest.mark.parametrize(
    ("class_to_test", "kwargs", "exception", "match"),
    [
        (
            Distribution,
            {"attrs": {"executables": "hello.py", "script_name": "setup.py"}},
            SetupError,
            "'executables' must be a list of Executable",
        ),
        (
            Executable,
            {"script": "test.py", "base": "foo"},
            OptionError,
            "no base named ",
        ),
        (
            Executable,
            {"script": "test.py", "init_script": "foo"},
            OptionError,
            "no init_script named ",
        ),
        (
            Executable,
            {"script": "test.py", "target_name": "foo/bar"},
            OptionError,
            "target_name cannot contain the path, only the filename: ",
        ),
        (
            Executable,
            {"script": "test.py", "target_name": "0test"},
            OptionError,
            "target_name is invalid: ",
        ),
    ],
    ids=[
        "executables-invalid",
        "executable-invalid-base",
        "executable-invalid-init_script",
        "executable-invalid-target_name",
        "executable-invalid-target_name-isidentifier",
    ],
)
def test_invalid(class_to_test, kwargs, exception, match):
    """Test invalid values to use in Distribution and Executable classes."""
    with pytest.raises(exception, match=match):
        class_to_test(**kwargs)


SOURCE_VALID_ICON = """
test_icon.py
    print("Hello from cx_Freeze")
setup.py
    from cx_Freeze import setup

    setup(
        name="hello",
        version="0.1.2.3",
        description="Sample cx_Freeze script",
        executables=[{"script": "test_icon.py", "icon": "icon"}],
    )
"""


def test_valid_icon(tmp_path: Path):
    """Test the icon sample with bdist_appimage."""
    create_package(tmp_path, SOURCE_VALID_ICON)
    for src in FIXTURE_DIR.parent.joinpath("cx_Freeze/icons").glob("py.*"):
        shutil.copyfile(src, tmp_path.joinpath("icon").with_suffix(src.suffix))

    output = check_output(
        [sys.executable, "setup.py", "build_exe"],
        text=True,
        cwd=os.fspath(tmp_path),
    )
    assert "WARNING: Icon file not found" not in output, "icon file not found"

    file_created = tmp_path / BUILD_EXE_DIR / f"test_icon{SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = check_output([os.fspath(file_created)], text=True, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


SOURCE_INVALID_ICON = """
test_icon.py
    print("Hello from cx_Freeze")
setup.py
    from cx_Freeze import setup

    setup(
        name="hello",
        version="0.1.2.3",
        description="Sample cx_Freeze script",
        executables=[{"script": "test_icon.py", "icon": "icon.png"}],
    )
"""


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
def test_invalid_icon(tmp_path: Path):
    """Test the icon sample with bdist_appimage."""
    create_package(tmp_path, SOURCE_INVALID_ICON)
    shutil.copyfile(
        FIXTURE_DIR.parent / "cx_Freeze/icons/py.png", tmp_path / "icon.png"
    )

    output = check_output(
        [sys.executable, "setup.py", "build_exe"],
        text=True,
        cwd=os.fspath(tmp_path),
    )
    assert "WARNING: Icon file not found" not in output, "icon file not found"
    # it is expected the folowing warning if the icon is invalid
    assert "WARNING: Icon filename 'icon.png' has invalid type." in output
