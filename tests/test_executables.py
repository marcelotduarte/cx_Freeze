"""Test executables keyword (and Executable class)."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from subprocess import check_output
from sysconfig import get_platform, get_python_version

import pytest
from generate_samples import create_package
from setuptools import Distribution

from cx_Freeze.exception import SetupError

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"

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
    suffix = ".exe" if sys.platform == "win32" else ""

    for i in range(1, number_of_executables):
        file_created = tmp_path / BUILD_EXE_DIR / f"test_simple{i}{suffix}"
        assert file_created.is_file(), f"file not found: {file_created}"

        output = check_output([os.fspath(file_created)], text=True, timeout=10)
        assert output.startswith("Hello from cx_Freeze")


def test_executables_invalid_value():
    """Test the executables option with invalid value."""
    with pytest.raises(
        SetupError, match="'executables' must be a list of Executable"
    ):
        Distribution(
            {
                "name": "foo",
                "version": "0.0",
                "executables": "hello.py",
                "script_name": "setup.py",
            }
        )
