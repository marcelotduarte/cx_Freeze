"""Test executables keyword (and Executable class)."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest
from generate_samples import create_package, run_command
from setuptools import Distribution

from cx_Freeze import Executable
from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX, IS_MINGW, IS_WINDOWS
from cx_Freeze.exception import OptionError, SetupError

TOP_DIR = Path(__file__).resolve().parent.parent

SOURCE_SETUP_TOML = """
test_1.py
    print("Hello from cx_Freeze")
pyproject.toml
    [project]
    name = "hello"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"

    [[tool.cxfreeze.executables]]
    script = "test_1.py"

    [[tool.cxfreeze.executables]]
    script = "test_1.py"
    target_name = "test_2"

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "unittest"]
    silent = true
command
    cxfreeze build_exe --excludes=tkinter
"""

SOURCE_SETUP_PY = """
test_1.py
    print("Hello from cx_Freeze")
setup.py
    from cx_Freeze import Executable, setup

    executables = [
        "test_1.py",
        {"script": "test_1.py", "target_name": "test_2"},
        Executable("test_1.py", target_name="test_3"),
    ]

    setup(
        name="hello",
        version="0.1.2.3",
        description="Sample cx_Freeze script",
        executables=executables,
    )
command
    python setup.py build_exe --excludes=tkinter,unittest --silent
"""

SOURCE_SETUP_CFG = """
test_1.py
    print("Hello from cx_Freeze")
setup.cfg
    [metadata]
    name = hello
    version = 0.1.2.3
    description = Sample cx_Freeze script

    [build_exe]
    excludes = tkinter,unittest
    silent = true
command
    cxfreeze test_1.py
"""

SOURCE_SETUP_MIX = """
test_1.py
    print("Hello from cx_Freeze")
pyproject.toml
    [project]
    name = "hello"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"

    [[tool.cxfreeze.executables]]
    script = "test_1.py"
    target_name = "test_2"

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "unittest"]
    silent = true
setup.py
    from cx_Freeze import setup

    setup(executables=["test_1.py"])
command
    python setup.py build
"""

SOURCE_ADV_SETUP_TOML = """
test_1.py
    from modules.testfreeze_1 import func1
    print("Hello from cx_Freeze #1")
    func1()
test_2.py
    from modules.testfreeze_2 import func2
    print("Hello from cx_Freeze #2")
    func2()
test_3.py
    def say_hello():
        print("Hello from cx_Freeze #3")
    if __name__ == "__main__":
        say_hello()
modules/testfreeze_1.py
    def func1():
        print("Test freeze module #1")
modules/testfreeze_2.py
    def func2():
        print("Test freeze module #2")
pyproject.toml
    [project]
    name = "advanced"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"

    [[tool.cxfreeze.executables]]
    script = "test_1.py"

    [[tool.cxfreeze.executables]]
    script = "test_2.py"

    [[tool.cxfreeze.executables]]
    script = "test_3.py"

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "unittest"]
    silent = true
command
    cxfreeze build
"""

SOURCE_ADV_SETUP_PY = """
test_1.py
    from modules.testfreeze_1 import func1
    print("Hello from cx_Freeze #1")
    func1()
test_2.py
    from modules.testfreeze_2 import func2
    print("Hello from cx_Freeze #2")
    func2()
test_3.py
    def say_hello():
        print("Hello from cx_Freeze #3")
    if __name__ == "__main__":
        say_hello()
modules/testfreeze_1.py
    def func1():
        print("Test freeze module #1")
modules/testfreeze_2.py
    def func2():
        print("Test freeze module #2")
setup.py
    from cx_Freeze import Executable, setup

    executables = ["test_1.py", "test_2.py", "test_3.py"]

    setup(
        name="advanced",
        version="0.1.2.3",
        description="Sample cx_Freeze script",
        executables=executables,
    )
command
    python setup.py build_exe --excludes=tkinter,unittest --silent
"""


@pytest.mark.parametrize(
    ("source", "number_of_executables"),
    [
        (SOURCE_SETUP_TOML, 2),
        (SOURCE_SETUP_PY, 3),
        (SOURCE_SETUP_CFG, 1),
        (SOURCE_SETUP_MIX, 2),
        (SOURCE_ADV_SETUP_TOML, 3),
        (SOURCE_ADV_SETUP_PY, 3),
    ],
    ids=[
        "setup_toml",
        "setup_py",
        "setup_cfg",
        "setup_mix",
        "setup_adv_toml",
        "setup_adv_py",
    ],
)
def test_executables(
    tmp_path: Path, source: str, number_of_executables: int
) -> None:
    """Test the executables option."""
    create_package(tmp_path, source)
    output = run_command(tmp_path)

    for i in range(1, number_of_executables):
        file_created = tmp_path / BUILD_EXE_DIR / f"test_{i}{EXE_SUFFIX}"
        assert file_created.is_file(), f"file not found: {file_created}"

        output = run_command(tmp_path, file_created, timeout=10)
        assert output.startswith("Hello from cx_Freeze")


@pytest.mark.parametrize(
    ("option", "value", "result"),
    [
        ("base", None, "console-"),
        ("base", "console", "console-"),
        (
            "base",
            "gui",
            "Win32GUI-" if (IS_WINDOWS or IS_MINGW) else "console-",
        ),
        (
            "base",
            "service",
            "Win32Service-" if (IS_WINDOWS or IS_MINGW) else "console-",
        ),
        ("init_script", None, "console.py"),
        ("init_script", "console", "console.py"),
        ("target_name", None, f"test{EXE_SUFFIX}"),
        ("target_name", "test1", f"test1{EXE_SUFFIX}"),
        ("target_name", "test-0.1", f"test-0.1{EXE_SUFFIX}"),
        ("target_name", "test.exe", "test.exe"),
        ("icon", "icon", ("icon.ico", "icon.icns", "icon.png", "icon.svg")),
    ],
)
def test_valid(option, value, result) -> None:
    """Test valid values to use in Executable class."""
    executable = Executable("test.py", **{option: value})
    returned = getattr(executable, option)
    if isinstance(returned, Path):
        returned = returned.name
    assert returned.startswith(result), returned


@pytest.mark.parametrize(
    ("class_to_test", "kwargs", "expected_exception", "expected_match"),
    [
        (
            Distribution,
            {"attrs": {"executables": [], "script_name": "setup.py"}},
            SetupError,
            "'executables' must be a list of Executable",
        ),
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
        "executables-invalid-empty",
        "executables-invalid-string",
        "executable-invalid-base",
        "executable-invalid-init_script",
        "executable-invalid-target_name",
        "executable-invalid-target_name-isidentifier",
    ],
)
def test_invalid(
    class_to_test, kwargs, expected_exception, expected_match
) -> None:
    """Test invalid values to use in Distribution and Executable classes."""
    with pytest.raises(expected_exception, match=expected_match):
        class_to_test(**kwargs)


SOURCE_VALID_ICON = """
test_icon.py
    print("Hello from cx_Freeze")
pyproject.toml
    [project]
    name = "hello"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"

    [[tool.cxfreeze.executables]]
    script = "test_icon.py"
    icon = "icon"

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "unittest"]
command
    cxfreeze build
"""


def test_valid_icon(tmp_path: Path) -> None:
    """Test with valid icon in any OS."""
    create_package(tmp_path, SOURCE_VALID_ICON)
    # copy valid icons
    for src in TOP_DIR.joinpath("cx_Freeze/icons").glob("py.*"):
        shutil.copyfile(src, tmp_path.joinpath("icon").with_suffix(src.suffix))
    output = run_command(tmp_path)
    assert "WARNING: Icon file not found" not in output, "icon file not found"

    file_created = tmp_path / BUILD_EXE_DIR / f"test_icon{EXE_SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_not_found_icon(tmp_path: Path) -> None:
    """Test with not found icon in any OS."""
    # same test as before, without icons
    create_package(tmp_path, SOURCE_VALID_ICON)
    output = run_command(tmp_path)
    print(output)
    assert "WARNING: Icon file not found" in output, "icon file not found"


SOURCE_INVALID_ICON = """
test_icon.py
    print("Hello from cx_Freeze")
pyproject.toml
    [project]
    name = "hello"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"

    [[tool.cxfreeze.executables]]
    script = "test_icon.py"
    icon = "icon.png"

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "unittest"]
command
    cxfreeze build
"""


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
def test_invalid_icon(tmp_path: Path) -> None:
    """Test with invalid icon in Windows."""
    create_package(tmp_path, SOURCE_INVALID_ICON)
    shutil.copyfile(TOP_DIR / "cx_Freeze/icons/py.png", tmp_path / "icon.png")
    output = run_command(tmp_path)
    assert "WARNING: Icon file not found" not in output, "icon file not found"
    # it is expected the folowing warning if the icon is invalid
    assert "WARNING: Icon filename 'icon.png' has invalid type." in output


SOURCE_RENAME = """
test_0.py
    print("Hello from cx_Freeze")
pyproject.toml
    [project]
    name = "hello"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"

    [[tool.cxfreeze.executables]]
    script = "test_0.py"

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "unittest"]
command
    cxfreeze build
"""


def test_executable_rename(tmp_path: Path) -> None:
    """Test if the executable can be renamed."""
    create_package(tmp_path, SOURCE_RENAME)
    output = run_command(tmp_path)
    file_created = tmp_path / BUILD_EXE_DIR / f"test_0{EXE_SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")

    file_renamed = file_created.rename(
        file_created.parent / "test_zero{EXE_SUFFIX}"
    )
    output = run_command(tmp_path, file_renamed, timeout=10)
    assert output.startswith("Hello from cx_Freeze")
