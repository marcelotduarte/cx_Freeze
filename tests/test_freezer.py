"""Tests for cx_Freeze.freezer."""

from __future__ import annotations

import sys
import sysconfig
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn

import pytest

from cx_Freeze import Freezer
from cx_Freeze._compat import (
    ABI_THREAD,
    IS_CONDA,
    IS_MACOS,
    IS_MINGW,
    IS_UCRT,
    IS_WINDOWS,
    PYTHON_VERSION,
)
from cx_Freeze.exception import OptionError

if TYPE_CHECKING:
    from collections.abc import Callable

    from .conftest import TempPackage

ENABLE_SHARED = bool(sysconfig.get_config_var("Py_ENABLE_SHARED"))

SOURCE = """
hello.py
    print("Hello from cx_Freeze")
"""


def test_freezer_target_dir_empty(tmp_package: TempPackage) -> None:
    """Test freezer target_dir empty."""
    tmp_package.create(SOURCE)
    freezer = Freezer(executables=["hello.py"])
    expected_target_dir = tmp_package.executable("hello").parent
    assert freezer.target_dir == expected_target_dir, (
        f"Expected target_dir: {expected_target_dir}, "
        f"Actual target_dir: {freezer.target_dir}"
    )


def test_freezer_target_dir_dist(tmp_package: TempPackage) -> None:
    """Test freezer target_dir='dist'."""
    tmp_package.create(SOURCE)
    freezer = Freezer(executables=["hello.py"], target_dir="dist")
    expected_target_dir = tmp_package.executable_in_dist("hello").parent
    assert freezer.target_dir == expected_target_dir, (
        f"Expected target_dir: {expected_target_dir}, "
        f"Actual target_dir: {freezer.target_dir}"
    )


def test_freezer_target_dir_utf8(tmp_package: TempPackage) -> None:
    """Test freezer target_dir with a name in utf_8."""
    tmp_package.create(SOURCE)
    expected_target_dir = tmp_package.path / "ação"
    freezer = Freezer(executables=["hello.py"], target_dir=expected_target_dir)
    assert freezer.target_dir == expected_target_dir, (
        f"Expected target_dir: {expected_target_dir}, "
        f"Actual target_dir: {freezer.target_dir}"
    )


def test_freezer_target_dir_in_path(tmp_package: TempPackage) -> None:
    """Test freezer target_dir in path."""
    tmp_package.create(SOURCE)
    target_dir = tmp_package.executable("hello").parent
    target_dir.mkdir(parents=True)
    msg = "the build_exe directory cannot be used as search path"
    with pytest.raises(OptionError, match=msg):
        Freezer(executables=["hello.py"], path=[*sys.path, target_dir])


def test_freezer_target_dir_locked(tmp_package: TempPackage) -> None:
    """Test freezer target_dir locked."""

    def t_rmtree(
        path: str,
        _ignore_errors: bool = False,
        _onerror: Callable | None = None,
    ) -> NoReturn:
        msg = f"cannot clean {path}"
        raise OSError(msg)

    tmp_package.monkeypatch.setattr("shutil.rmtree", t_rmtree)

    tmp_package.create(SOURCE)
    target_dir = tmp_package.executable("hello").parent
    target_dir.mkdir(parents=True)
    msg = "the build_exe directory cannot be cleaned"
    with pytest.raises(OptionError, match=msg):
        Freezer(executables=["hello.py"], target_dir=target_dir)


def test_freezer_default_bin_includes(tmp_package: TempPackage) -> None:
    """Test freezer.default_bin_includes."""
    tmp_package.create(SOURCE)

    freezer = Freezer(executables=["hello.py"])
    py_version = f"{PYTHON_VERSION}{ABI_THREAD}"
    if IS_MINGW:
        expected = f"libpython{py_version}.dll"
    elif IS_WINDOWS:
        expected = f"python{py_version.replace('.', '')}.dll"
    elif IS_CONDA:  # macOS or Linux
        if IS_MACOS:
            expected = f"libpython{py_version}.dylib"
        else:
            expected = f"libpython{py_version}.so*"
    elif IS_MACOS:
        expected = f"Python{ABI_THREAD.upper()}"
    elif ENABLE_SHARED:  # Linux
        expected = f"libpython{py_version}.so*"
    else:
        assert freezer.default_bin_includes == []
        return
    names = []
    for path in map(Path, freezer.default_bin_path_includes):
        names += [
            file
            for file in map(Path, freezer.default_bin_includes)
            if file.match(path.joinpath(expected).as_posix())
        ]
    assert names != []


def test_freezer_populate_zip_options_invalid_values(
    tmp_package: TempPackage,
) -> None:
    """Test freezer _populate_zip_options invalid values."""
    tmp_package.create(SOURCE)

    # zip_include_packages and zip_exclude_packages are "*"
    msg = "all packages cannot be included and excluded "
    with pytest.raises(OptionError, match=msg):
        Freezer(
            executables=["hello.py"],
            zip_include_packages=["*"],
            zip_exclude_packages=["*"],
        )

    # zip_include_packages and zip_exclude_packages has the same package
    with pytest.raises(OptionError, match="package 'tkinter' cannot be both"):
        Freezer(
            executables=["hello.py"],
            zip_include_packages=["tkinter"],
            zip_exclude_packages=["tkinter"],
        )
    msg = "packages 'tkinter, unittest' cannot be both"
    with pytest.raises(OptionError, match=msg):
        Freezer(
            executables=["hello.py"],
            zip_include_packages=["tkinter", "unittest"],
            zip_exclude_packages=["tkinter", "unittest", "codeop"],
        )


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        pytest.param(
            {"compress": None}, {"compress": True}, id="compress=none"
        ),
        pytest.param(
            {"compress": False}, {"compress": False}, id="compress=false"
        ),
        pytest.param(
            {"compress": True}, {"compress": True}, id="compress=true"
        ),
        pytest.param(
            {"excludes": ["tkinter", "unittest"]},
            {"excludes": ["tkinter", "unittest"]},
            id="excludes=['tkinter','unittest']",
        ),
        pytest.param(
            {"include_msvcr": None},
            {"include_msvcr": False},
            id="include_msvcr=none",
        ),
        pytest.param(
            {"include_msvcr": False},
            {"include_msvcr": False},
            id="include_msvcr=false",
        ),
        pytest.param(
            {"include_msvcr": True},
            {"include_msvcr": IS_UCRT},
            id="include_msvcr=true",
        ),
        pytest.param(
            {"replace_paths": [("*", "")]},
            {"replace_paths": [("*", "")]},
            id="replace_paths=*",
        ),
        pytest.param(
            {"replace_paths": ["*="]},
            {"replace_paths": ["*="]},
            id="replace_paths=[*=]",
        ),
        # optimize values
        pytest.param(
            {"optimize": None}, {"optimize": 0}, id="optimize=none->0"
        ),
        pytest.param({"optimize": 0}, {"optimize": 0}, id="optimize=0->0"),
        pytest.param({"optimize": 1}, {"optimize": 1}, id="optimize=1->1"),
        pytest.param({"optimize": 2}, {"optimize": 2}, id="optimize=2->2"),
        # silent values
        pytest.param({"silent": None}, {"silent": 0}, id="silent=none->0"),
        pytest.param({"silent": False}, {"silent": 0}, id="silent=false->0"),
        pytest.param({"silent": True}, {"silent": 1}, id="silent=true->1"),
        pytest.param({"silent": 0}, {"silent": 0}, id="silent=0->0"),
        pytest.param({"silent": 1}, {"silent": 1}, id="silent=1->1"),
        pytest.param({"silent": 2}, {"silent": 2}, id="silent=2->2"),
        pytest.param({"silent": "3"}, {"silent": 3}, id="silent=3->3"),
        # test _populate_zip_options
        pytest.param(
            {"zip_include_packages": None, "zip_exclude_packages": None},
            {
                "zip_include_packages": [],
                "zip_exclude_packages": ["*"],
                "zip_include_all_packages": False,
            },
            id="zip_include_packages/zip_exclude_packages=none/none",
        ),
        pytest.param(
            {"zip_include_packages": ["*"], "zip_exclude_packages": None},
            {
                "zip_include_packages": ["*"],
                "zip_exclude_packages": [],
                "zip_include_all_packages": True,
            },
            id="zip_include_package=*",
        ),
        pytest.param(
            {"zip_include_packages": None, "zip_exclude_packages": ["*"]},
            {
                "zip_include_packages": [],
                "zip_exclude_packages": ["*"],
                "zip_include_all_packages": False,
            },
            id="zip_exclude_packages=*",
        ),
        pytest.param(  # zip_*_packages are namespace packages
            {
                "zip_include_packages": ["namespace.test"],
                "zip_exclude_packages": ["zope.event", "zope.interface"],
            },
            {
                "zip_include_packages": ["namespace"],
                "zip_exclude_packages": ["zope"],
                "zip_include_all_packages": False,
            },
            id="zip_include_packages/zip_exclude_packages=namespace/namespace",
        ),
    ],
)
def test_freezer_options(
    tmp_package: TempPackage, kwargs: dict[str, Any], expected: dict[str, Any]
) -> None:
    """Test freezer options."""
    tmp_package.create(SOURCE)

    freezer = Freezer(executables=["hello.py"], **kwargs)
    for option, value in expected.items():
        assert getattr(freezer, option) == value


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        pytest.param(
            {"zip_filename": None},
            {"zip_filename": "library.zip"},  # default compress is True
            id="zip_filename_none",
        ),
        pytest.param(
            {"zip_filename": "test"},
            {"zip_filename": "test.zip"},
            id="zip_filename_test",
        ),
        pytest.param(
            {"zip_filename": "test.zip"},
            {"zip_filename": "test.zip"},
            id="zip_filename_test_zip",
        ),
        pytest.param(
            {"zip_filename": "test.zip", "target_dir": "ação"},
            {"zip_filename": "test.zip"},
            id="zip_filename_test_zip_target_dir_utf_8_portuguese",
        ),
        pytest.param(
            {"zip_filename": "test.zip", "target_dir": "行動"},
            {"zip_filename": "test.zip"},
            id="zip_filename_test_zip_target_dir_utf_8_chinese",
        ),
        pytest.param(
            {"compress": True},
            {"compress": True, "zip_filename": "library.zip"},
            id="zip_filename_none_compress_true",
        ),
        pytest.param(
            {"compress": False},
            {"compress": False, "zip_filename": None},
            id="zip_filename_none_compress_false",
        ),
        pytest.param(
            {"compress": False, "zip_filename": "library.zip"},
            {"compress": False, "zip_filename": "library.zip"},
            id="zip_filename_name_compress_false",
        ),
    ],
)
def test_freezer_zip_filename(
    tmp_package: TempPackage, kwargs: dict[str, Any], expected: dict[str, Any]
) -> None:
    """Test freezer zip_filename option."""
    tmp_package.create(SOURCE)

    freezer = Freezer(
        executables=["hello.py"], include_msvcr=True, silent=True, **kwargs
    )
    target_dir = freezer.target_dir

    freezer.freeze()
    for option, value in expected.items():
        if option == "zip_filename":
            if value:
                assert freezer.zip_filename is not None
                assert freezer.zip_filename == target_dir / "lib" / value
                assert freezer.zip_filename.is_file()
            else:
                assert not (target_dir / "lib" / "library.zip").is_file()
        else:
            assert getattr(freezer, option) == value

    executable = target_dir / tmp_package.executable("hello").name
    assert executable.is_file()

    result = tmp_package.run(executable)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")


SOURCE_WITH_EXTRA_FILES = """
hello.py
    import module
    module.show()
module/__init__.py
    def show() -> None:
        print("Hello from cx_Freeze")
module/__init__.pyc
module/hello.pyi
    def show() -> None:
        ...
module/hello.pyx
    # pyx
module/hello.pxd
    # pxd
module/py.typed
"""


def test_freezer_copy_package_data(tmp_package: TempPackage) -> None:
    """Test freezer._copy_package_data."""
    tmp_package.create(SOURCE_WITH_EXTRA_FILES)

    freezer = Freezer(
        executables=["hello.py"],
        include_msvcr=True,
        path=[tmp_package.path, *sys.path],
        silent=True,
    )
    freezer.freeze()

    executable = tmp_package.executable("hello")
    assert executable.is_file()
    result = tmp_package.run(executable)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")

    ignore_patterns = [
        "*.c",
        "*.cpp",
        "*.pxd",
        "*.pxi",
        "*.py",
        # "*.pyc", # this pattern is not copied by _copy_package_data itself.
        "*.pyi",
        "*.pyo",
        "*.pyx",
        "__pycache__",
        "py.typed",
    ]
    if not IS_MACOS:
        ignore_patterns.append(".DS_store")
    names = [
        file.name
        for file in freezer.target_dir.joinpath("lib").rglob("*")
        if any(filter(file.match, ignore_patterns))
    ]
    assert names == []


SOURCE_2 = """
namespacepack/firstchildpack/__init__.py
namespacepack/firstchildpack/main.py
    from namespacepack.firstchildpack.utils import name

    def main():
        print(f"Hello, {name()}!")

    if __name__ == "__main__":
        main()
namespacepack/firstchildpack/utils/__init__.py
    def name():
        return "firstchildpack"
namespacepack/firstchildpack/utils/basic/readme.txt
    readme
namespacepack/firstchildpack/configs/conf.yaml
    test_key: "firstchildpack"
namespacepack/firstchildpack/models/model.txt
    Some model of firstchildpack
namespacepack/secondchildpack/__init__.py
namespacepack/secondchildpack/main.py
    from namespacepack.secondchildpack.utils import name

    def main():
        print(f"Hello, {name()}!")

    if __name__ == "__main__":
        main()
namespacepack/secondchildpack/utils.py
    def name():
        return "secondchildpack"
namespacepack/secondchildpack/configs/conf.yaml
    test_key: "secondchildpack"
namespacepack/secondchildpack/models/model.txt
    Some model of secondchildpack
regularpack/__init__.py
regularpack/main.py
    from regularpack.utils import name

    def main():
        print(f"Hello, {name()}!")

    if __name__ == "__main__":
        main()
regularpack/utils.py
    def name():
        return "regularpack"
regularpack/configs/conf.yaml
    test_key: "regularpack"
regularpack/models/model.txt
    Some model of regularpack
"""


def test_freezer_excludes(tmp_package: TempPackage) -> None:
    """Test the freeze excludes option."""
    tmp_package.create(SOURCE_2)

    freezer = Freezer(
        executables=[
            {
                "script": "regularpack/main.py",
                "target_name": "regularpack",
            },
            {
                "script": "namespacepack/firstchildpack/main.py",
                "target_name": "firstchildpack",
            },
            {
                "script": "namespacepack/secondchildpack/main.py",
                "target_name": "secondchildpack",
            },
        ],
        excludes=[
            "regularpack.configs",
            "regularpack.models",
            "namespacepack.firstchildpack.configs",
            "namespacepack.firstchildpack.models",
            "namespacepack.firstchildpack.utils.basic",
            "namespacepack.secondchildpack.configs",
            "namespacepack.secondchildpack.models",
        ],
        include_msvcr=True,
        packages=[
            "regularpack",
            "namespacepack.firstchildpack",
            "namespacepack.secondchildpack",
        ],
        path=[tmp_package.path, *sys.path],
        silent=True,
    )
    freezer.freeze()

    for fullname in (
        "regularpack",
        "namespacepack.firstchildpack",
        "namespacepack.secondchildpack",
    ):
        name = fullname.split(".")[-1]
        executable = tmp_package.executable(name)
        assert executable.is_file()

        result = tmp_package.run(executable)
        result.stdout.fnmatch_lines(f"Hello, {name}!")

        pkg_dir = executable.parent / "lib" / fullname.replace(".", "/")
        print(f"\n-->{fullname}")
        filelist = [fn for fn in pkg_dir.rglob("*") if fn.is_file()]
        for fn in filelist:
            print(fn)
        assert len(filelist) == 3
