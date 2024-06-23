"""Tests for cx_Freeze.freezer."""

from __future__ import annotations

import sys
from sysconfig import get_config_vars
from typing import TYPE_CHECKING, Any, NoReturn

import pytest
from generate_samples import create_package, run_command

from cx_Freeze import Executable, Freezer
from cx_Freeze._compat import (
    BUILD_EXE_DIR,
    EXE_SUFFIX,
    IS_MACOS,
    IS_MINGW,
    IS_WINDOWS,
    PYTHON_VERSION,
)
from cx_Freeze.exception import OptionError

if TYPE_CHECKING:
    from pathlib import Path

SOURCE = """
hello.py
    print("Hello from cx_Freeze")
"""


def test_freezer_target_dir_empty(tmp_path: Path, monkeypatch) -> None:
    """Test freezer target_dir empty."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    freezer = Freezer(executables=[Executable("hello.py")])
    target_dir = tmp_path / BUILD_EXE_DIR
    assert freezer.target_dir == target_dir


def test_freezer_target_dir_dist(tmp_path: Path, monkeypatch) -> None:
    """Test freezer target_dir='dist'."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    freezer = Freezer(executables=[Executable("hello.py")], target_dir="dist")
    target_dir = tmp_path / "dist"
    assert freezer.target_dir == target_dir


def test_freezer_target_dir_utf8(tmp_path: Path, monkeypatch) -> None:
    """Test freezer target_dir with a name in utf_8."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    target_dir = tmp_path / "ação"
    freezer = Freezer(
        executables=[Executable("hello.py")], target_dir=target_dir
    )
    assert freezer.target_dir == target_dir


def test_freezer_target_dir_in_path(tmp_path: Path, monkeypatch) -> None:
    """Test freezer target_dir in path."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    target_dir = tmp_path / BUILD_EXE_DIR
    target_dir.mkdir(parents=True)
    with pytest.raises(
        OptionError,
        match="the build_exe directory cannot be used as search path",
    ):
        Freezer(
            executables=[Executable("hello.py")], path=[*sys.path, target_dir]
        )


def test_freezer_target_dir_locked(tmp_path: Path, monkeypatch) -> None:
    """Test freezer target_dir locked."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    def t_rmtree(path, _ignore_errors=False, _onerror=None) -> NoReturn:
        msg = f"cannot clean {path}"
        raise OSError(msg)

    monkeypatch.setattr("shutil.rmtree", t_rmtree)

    target_dir = tmp_path / BUILD_EXE_DIR
    target_dir.mkdir(parents=True)
    with pytest.raises(
        OptionError, match="the build_exe directory cannot be cleaned"
    ):
        Freezer(executables=[Executable("hello.py")], target_dir=target_dir)


def test_freezer_default_bin_includes(tmp_path: Path, monkeypatch) -> None:
    """Test freezer _default_bin_includes."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    freezer = Freezer(executables=[Executable("hello.py")])
    if IS_MACOS:
        if sys.version_info[:2] <= (3, 10):
            expected = f"libpython{PYTHON_VERSION}.dylib"
        else:
            expected = f"Python.framework/Versions/{PYTHON_VERSION}/Python"
    elif IS_WINDOWS:
        expected = f"python{PYTHON_VERSION.replace('.','')}.dll"
    elif IS_MINGW:
        expected = f"libpython{PYTHON_VERSION}.dll"
    else:
        expected = f"libpython{PYTHON_VERSION}.so"
    assert expected in freezer.bin_includes


def test_freezer_default_bin_includes_emulated(
    tmp_path: Path, monkeypatch
) -> None:
    """Test freezer _default_bin_includes in conda/mingw environments."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    def t_get_config_var(name) -> dict[str, Any]:
        if name == "INSTSONAME":
            # emulate conda and/or mingw
            soname = f"libpython{PYTHON_VERSION}.a"
            if IS_MINGW or IS_WINDOWS:  # emulate mingw
                soname = soname.replace(".a", ".dll.a")
            return soname
        return get_config_vars().get(name)

    monkeypatch.setattr("sysconfig.get_config_var", t_get_config_var)

    freezer = Freezer(executables=[Executable("hello.py")])
    if IS_MACOS:
        expected = f"libpython{PYTHON_VERSION}.dylib"
    elif IS_MINGW or IS_WINDOWS:
        expected = f"libpython{PYTHON_VERSION}.dll"
    else:
        expected = f"libpython{PYTHON_VERSION}.so"
    assert expected in freezer.bin_includes


def test_freezer_populate_zip_options_invalid_values(
    tmp_path: Path, monkeypatch
) -> None:
    """Test freezer _populate_zip_options invalid values."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    # zip_include_packages and zip_exclude_packages are "*"
    with pytest.raises(
        OptionError, match="all packages cannot be included and excluded "
    ):
        Freezer(
            executables=[Executable("hello.py")],
            zip_include_packages=["*"],
            zip_exclude_packages=["*"],
        )

    # zip_include_packages and zip_exclude_packages has the same package
    with pytest.raises(OptionError, match="package 'tkinter' cannot be both"):
        Freezer(
            executables=[Executable("hello.py")],
            zip_include_packages=["tkinter"],
            zip_exclude_packages=["tkinter"],
        )
    with pytest.raises(
        OptionError, match="packages 'tkinter, unittest' cannot be both"
    ):
        Freezer(
            executables=[Executable("hello.py")],
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
            marks=pytest.mark.skipif(not IS_WINDOWS, reason="Windows tests"),
        ),
        pytest.param(
            {"include_msvcr": False},
            {"include_msvcr": False},
            id="include_msvcr=false",
            marks=pytest.mark.skipif(not IS_WINDOWS, reason="Windows tests"),
        ),
        pytest.param(
            {"include_msvcr": True},
            {"include_msvcr": True},
            id="include_msvcr=true",
            marks=pytest.mark.skipif(not IS_WINDOWS, reason="Windows tests"),
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
                "zip_include_packages": set(),
                "zip_exclude_packages": set("*"),
                "zip_include_all_packages": False,
            },
            id="zip_include_packages/zip_exclude_packages=none/none",
        ),
        pytest.param(
            {"zip_include_packages": ["*"], "zip_exclude_packages": None},
            {
                "zip_include_packages": set("*"),
                "zip_exclude_packages": set(),
                "zip_include_all_packages": True,
            },
            id="zip_include_package=*",
        ),
        pytest.param(
            {"zip_include_packages": None, "zip_exclude_packages": ["*"]},
            {
                "zip_include_packages": set(),
                "zip_exclude_packages": set("*"),
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
                "zip_include_packages": {"namespace"},
                "zip_exclude_packages": {"zope"},
                "zip_include_all_packages": False,
            },
            id="zip_include_packages/zip_exclude_packages=namespace/namespace",
        ),
    ],
)
def test_freezer_options(
    tmp_path: Path,
    monkeypatch,
    kwargs: dict[str, ...],
    expected: dict[str, ...],
) -> None:
    """Test freezer options."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    freezer = Freezer(executables=[Executable("hello.py")], **kwargs)
    for option, value in expected.items():
        assert getattr(freezer, option) == value


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        pytest.param(
            {"zip_filename": None},
            {"zip_filename": "library.zip"},  # default compress is True
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
            {"zip_filename": "test.zip", "target_dir": "ação"},
            {"zip_filename": "test.zip"},
            id="zip_filename=test.zip/target_dir=utf_8/portuguese",
        ),
        pytest.param(
            {"zip_filename": "test.zip", "target_dir": "行動"},
            {"zip_filename": "test.zip"},
            id="zip_filename=test.zip/target_dir=utf_8/chinese",
        ),
        pytest.param(
            {"compress": True},
            {"compress": True, "zip_filename": "library.zip"},
            id="zip_filename=none/compress=true",
        ),
        pytest.param(
            {"compress": False},
            {"compress": False, "zip_filename": None},
            id="zip_filename=none/compress=false",
        ),
        pytest.param(
            {"compress": False, "zip_filename": "library.zip"},
            {"compress": False, "zip_filename": "library.zip"},
            id="zip_filename=name/compress=false",
        ),
    ],
)
def test_freezer_zip_filename(
    tmp_path: Path,
    monkeypatch,
    kwargs: dict[str, ...],
    expected: dict[str, ...],
) -> None:
    """Test freezer zip_filename option."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    freezer = Freezer(
        executables=[Executable("hello.py")], silent=True, **kwargs
    )
    target_dir = freezer.target_dir

    freezer.freeze()
    for option, value in expected.items():
        if option == "zip_filename":
            if value:
                assert freezer.zip_filename == target_dir / "lib" / value
                assert freezer.zip_filename.is_file()
            else:
                assert not (target_dir / "lib" / "library.zip").is_file()
        else:
            assert getattr(freezer, option) == value

    executable = target_dir / f"hello{EXE_SUFFIX}"
    assert executable.is_file()

    output = run_command(tmp_path, executable, timeout=10)
    assert output.startswith("Hello from cx_Freeze")
