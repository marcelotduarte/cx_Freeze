"""Test executables keyword (and Executable class)."""

from __future__ import annotations

import shutil
import sys
from importlib.resources import files
from pathlib import Path

import pytest
from setuptools import Distribution

from cx_Freeze import Executable
from cx_Freeze._compat import EXE_SUFFIX, IS_MINGW, IS_WINDOWS, SOABI
from cx_Freeze.exception import OptionError, SetupError

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
    cxfreeze build_exe
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
    cxfreeze --script test_1.py
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
    from cx_Freeze import setup

    options = {
        "build_exe": {
            "excludes": ["tkinter", "unittest"],
            "include_path": ["."],
            "silent": True
        }
    }

    setup(
        name="advanced",
        version="0.1.2.3",
        description="Sample cx_Freeze script",
        options=options,
        executables=["test_1.py", "test_2.py", "test_3.py"],
    )
command
    python setup.py build_exe
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
    tmp_package, source: str, number_of_executables: int
) -> None:
    """Test the executables option."""
    tmp_package.create(source)
    output = tmp_package.run()

    for i in range(1, number_of_executables):
        file_created = tmp_package.executable(f"test_{i}")
        assert file_created.is_file(), f"file not found: {file_created}"

        output = tmp_package.run(file_created, timeout=10)
        assert output.startswith("Hello from cx_Freeze")


TEST_VALID_PARAMETERS = [
    ("base", "console", f"console-{SOABI}{EXE_SUFFIX}"),
    pytest.param(
        "base",
        "absolutepath",
        f"console_test{EXE_SUFFIX}",
        id="base-absolutepath-console_test",
    ),
    pytest.param(
        "init_script", None, "console.py", id="init_script-none-console.py"
    ),
    ("init_script", "console", "console.py"),
    pytest.param(
        "init_script",
        "absolutepath",
        "console_test.py",
        id="init_script-absolutepath-console_test.py",
    ),
    pytest.param(
        "target_name", None, f"test{EXE_SUFFIX}", id="target_name-none-test"
    ),
    ("target_name", "test1", f"test1{EXE_SUFFIX}"),
    ("target_name", "12345", f"12345{EXE_SUFFIX}"),
    ("target_name", "test-0.1", f"test-0.1{EXE_SUFFIX}"),
    ("target_name", "test.exe", "test.exe"),
    pytest.param(
        "icon",
        "icon",
        ("icon.ico", "icon.icns", "icon.png", "icon.svg"),
        id="icon-icon-multiple",
    ),
]
if sys.version_info[:2] < (3, 13):
    TEST_VALID_PARAMETERS += [
        pytest.param(
            "base",
            None,
            f"console_legacy-{SOABI}{EXE_SUFFIX}",
            id="base-none-console_legacy-",
        ),
        ("base", "console_legacy", f"console_legacy-{SOABI}{EXE_SUFFIX}"),
    ]
else:
    TEST_VALID_PARAMETERS += [
        pytest.param(
            "base",
            None,
            f"console-{SOABI}{EXE_SUFFIX}",
            id="base-none-console-",
        ),
    ]
if IS_WINDOWS or IS_MINGW:
    TEST_VALID_PARAMETERS += [
        ("base", "gui", f"gui-{SOABI}{EXE_SUFFIX}"),
        ("base", "service", f"service-{SOABI}{EXE_SUFFIX}"),
        ("base", "Win32GUI", f"Win32GUI-{SOABI}{EXE_SUFFIX}"),
        ("base", "Win32Service", f"Win32Service-{SOABI}{EXE_SUFFIX}"),
    ]
else:
    TEST_VALID_PARAMETERS += [
        ("base", "gui", f"console-{SOABI}{EXE_SUFFIX}"),
        ("base", "service", f"console-{SOABI}{EXE_SUFFIX}"),
    ]


@pytest.mark.parametrize(("option", "value", "result"), TEST_VALID_PARAMETERS)
def test_valid(tmp_package, option, value, result) -> None:
    """Test valid values to use in Executable class."""
    if value == "absolutepath":
        src_dir = files("cx_Freeze").resolve()
        if option == "base":
            value = tmp_package.path / f"console_test{EXE_SUFFIX}"
            shutil.copyfile(
                src_dir / f"bases/console-{SOABI}{EXE_SUFFIX}", value
            )
        elif option == "init_script":
            value = tmp_package.path / "console_test.py"
            shutil.copyfile(src_dir / "initscripts/console.py", value)

    executable = Executable("test.py", **{option: value})
    returned = getattr(executable, option)
    if isinstance(value, Path) and value.is_absolute():
        assert returned == value
    if isinstance(returned, Path):
        returned = returned.name
    if isinstance(result, tuple):  # valid icon names
        assert returned.startswith(result), returned
        return
    assert returned == result, returned


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
    ],
    ids=[
        "executables-invalid-empty",
        "executables-invalid-string",
        "executable-invalid-base",
        "executable-invalid-init_script",
        "executable-invalid-target_name-with-path",
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
    silent = false
"""


def test_valid_icon(tmp_package) -> None:
    """Test with valid icon in any OS."""
    tmp_package.create(SOURCE_VALID_ICON)
    # copy valid icons: cp $SRC/cx_Freeze/icons/py.* $DST/icon.*
    src_dir = files("cx_Freeze").resolve()
    for src in src_dir.joinpath("icons").glob("py.*"):
        shutil.copyfile(
            src, tmp_package.path.joinpath("icon").with_suffix(src.suffix)
        )
    output = tmp_package.run()
    assert "WARNING: Icon file not found" not in output, "icon file not found"

    file_created = tmp_package.executable("test_icon")
    assert file_created.is_file(), f"file not found: {file_created}"

    output = tmp_package.run(file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_not_found_icon(tmp_package) -> None:
    """Test with not found icon in any OS."""
    # same test as before, without icons
    tmp_package.create(SOURCE_VALID_ICON)
    output = tmp_package.run()
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
    silent = false
"""


@pytest.mark.skipif(not (IS_MINGW or IS_WINDOWS), reason="Windows tests")
def test_invalid_icon(tmp_package) -> None:
    """Test with invalid icon in Windows."""
    tmp_package.create(SOURCE_INVALID_ICON)
    # use an invalid icon: cp $SRC/cx_Freeze/icons/py.png $DST/icon.png
    src_dir = files("cx_Freeze").resolve()
    shutil.copyfile(src_dir / "icons/py.png", tmp_package.path / "icon.png")
    output = tmp_package.run()
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
    silent = true
"""


def test_executable_rename(tmp_package) -> None:
    """Test if the executable can be renamed."""
    tmp_package.create(SOURCE_RENAME)
    output = tmp_package.run()
    file_created = tmp_package.executable("test_0")
    assert file_created.is_file(), f"file not found: {file_created}"

    output = tmp_package.run(file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")

    file_renamed = file_created.rename(file_created.parent / "test_zero")
    output = tmp_package.run(file_renamed, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


SOURCE_NAMESPACE = """\
main.py
    import importlib.util
    import namespace.package

    def is_namespace_package(package_name: str) -> bool:
        spec = importlib.util.find_spec(package_name)
        return spec.origin is None

    if __name__ == "__main__":
        print("'namespace' is namespace package: ",
              is_namespace_package('namespace'))
        print("'namespace.package' is namespace package: ",
              is_namespace_package('namespace.package'))
namespace/package/__init__.py
    print("Hello from cx_Freeze")
command
    cxfreeze --script main.py --target-name test --silent
"""

SOURCE_NESTED_NAMESPACE = """\
main.py
    import importlib.util
    import namespace.package.one
    import namespace.package.two

    def is_namespace_package(package_name: str) -> bool:
        spec = importlib.util.find_spec(package_name)
        return spec.origin is None

    if __name__ == "__main__":
        print("'namespace' is namespace package: ",
              is_namespace_package('namespace'))
        print("'namespace.package' is namespace package: ",
              is_namespace_package('namespace.package'))
        print("'namespace.package.one' is namespace package: ",
              is_namespace_package('namespace.package.one'))
        print("'namespace.package.two' is namespace package: ",
              is_namespace_package('namespace.package.two'))
namespace/package/one.py
    print("Hello from cx_Freeze - module one")
namespace/package/two.py
    print("Hello from cx_Freeze - module two")
command
    cxfreeze --script main.py --target-name test --silent
"""


@pytest.mark.parametrize(
    ("source", "hello", "namespace", "package_or_module", "zip_packages"),
    [
        (SOURCE_NAMESPACE, 1, 1, 1, False),
        (SOURCE_NAMESPACE, 1, 0, 2, True),
        (SOURCE_NESTED_NAMESPACE, 2, 2, 2, False),
        (SOURCE_NESTED_NAMESPACE, 2, 0, 4, True),
    ],
    ids=[
        "namespace_package",
        "namespace_package_zip_packages",
        "nested_namespace_package",
        "nested_namespace_package_zip_packages",
    ],
)
def test_executable_namespace(
    tmp_package,
    source: str,
    hello: int,
    namespace: int,
    package_or_module: int,
    zip_packages: bool,
) -> None:
    """Test executable with namespace package."""
    tmp_package.create(source)
    if zip_packages:
        with tmp_package.path.joinpath("command").open("a") as f:
            f.write(" --zip-include-packages=* --zip-exclude-packages=")
    output = tmp_package.run()

    file_created = tmp_package.executable("test")
    assert file_created.is_file(), f"file not found: {file_created}"

    output = tmp_package.run(file_created, timeout=10)
    lines = output.splitlines()
    start = 0
    stop = hello
    for i in range(start, stop):
        assert lines[i].startswith("Hello from cx_Freeze")
    start += hello
    stop += namespace
    for i in range(start, stop):
        assert lines[i].endswith("True")
    start += namespace
    stop += package_or_module
    for i in range(start, stop):
        assert lines[i].endswith("False")
