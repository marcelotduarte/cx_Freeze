"""Tests for cx_Freeze.freezer."""

from __future__ import annotations

import sys
from pathlib import Path
from sysconfig import get_config_vars, get_platform, get_python_version

import pytest
from generate_samples import create_package

from cx_Freeze import Executable, Freezer
from cx_Freeze.exception import OptionError

PLATFORM = get_platform()
IS_LINUX = PLATFORM.startswith("linux")
IS_MACOS = PLATFORM.startswith("macos")
IS_WINDOWS = PLATFORM.startswith("win")
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"

SOURCE = """
hello.py
    print("Hello from cx_Freeze")
"""


def test_freezer_target_dir_empty(tmp_path: Path, monkeypatch):
    """Test freezer target_dir empty."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    freezer = Freezer(executables=[Executable("hello.py")])
    target_dir = tmp_path / BUILD_EXE_DIR
    assert freezer.target_dir == target_dir


def test_freezer_target_dir_in_path(tmp_path: Path, monkeypatch):
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


def test_freezer_target_dir_locked(tmp_path: Path, monkeypatch):
    """Test freezer target_dir locked."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    def t_rmtree(path, _ignore_errors=False, _onerror=None):
        raise OSError(f"cannot clean {path}")

    monkeypatch.setattr("shutil.rmtree", t_rmtree)

    target_dir = tmp_path / BUILD_EXE_DIR
    target_dir.mkdir(parents=True)
    with pytest.raises(
        OptionError, match="the build_exe directory cannot be cleaned"
    ):
        Freezer(executables=[Executable("hello.py")], target_dir=target_dir)


def test_freezer_default_bin_includes(tmp_path: Path, monkeypatch):
    """Test freezer _default_bin_includes."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    freezer = Freezer(executables=[Executable("hello.py")])
    if IS_WINDOWS:
        expected = f"python{PYTHON_VERSION.replace('.','')}.dll"
    elif IS_MACOS:
        if sys.version_info[:2] <= (3, 10):
            expected = f"libpython{PYTHON_VERSION}.dylib"
        else:
            expected = f"Python.framework/Versions/{PYTHON_VERSION}/Python"
    else:
        expected = f"libpython{PYTHON_VERSION}.so"
    assert expected in freezer.bin_includes


def test_freezer_default_bin_includes_emulated(tmp_path: Path, monkeypatch):
    """Test freezer _default_bin_includes in conda/mingw environments."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    def t_get_config_var(name):
        if name == "INSTSONAME":
            # emulate conda and/or mingw
            soname = f"libpython{PYTHON_VERSION}.a"
            if IS_WINDOWS:  # emulate mingw
                soname = soname.replace(".a", ".dll.a")
            return soname
        return get_config_vars().get(name)

    monkeypatch.setattr("sysconfig.get_config_var", t_get_config_var)

    freezer = Freezer(executables=[Executable("hello.py")])
    if IS_WINDOWS:
        expected = f"libpython{PYTHON_VERSION}.dll"
    elif IS_MACOS:
        expected = f"libpython{PYTHON_VERSION}.dylib"
    else:
        expected = f"libpython{PYTHON_VERSION}.so"
    assert expected in freezer.bin_includes


def test_freezer_populate_zip_options(tmp_path: Path, monkeypatch):
    """Test freezer _populate_zip_options."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)

    # zip_include_packages and zip_exclude_packages are None (default)
    freezer = Freezer(executables=[Executable("hello.py")])
    assert freezer.zip_include_packages == set()
    assert freezer.zip_exclude_packages == set("*")
    assert freezer.zip_include_all_packages is False

    # zip_include_packages=*
    freezer = Freezer(
        executables=[Executable("hello.py")],
        zip_include_packages=["*"],
        zip_exclude_packages=[],
    )
    assert freezer.zip_include_packages == set("*")
    assert freezer.zip_exclude_packages == set()
    assert freezer.zip_include_all_packages is True

    # zip_exclude_packages=*
    freezer = Freezer(
        executables=[Executable("hello.py")],
        zip_include_packages=[],
        zip_exclude_packages=["*"],
    )
    assert freezer.zip_include_packages == set()
    assert freezer.zip_exclude_packages == set("*")
    assert freezer.zip_include_all_packages is False

    # zip_include_packages and zip_exclude_packages are "*"
    with pytest.raises(
        OptionError, match="all packages cannot be included and excluded "
    ):
        freezer = Freezer(
            executables=[Executable("hello.py")],
            zip_include_packages=["*"],
            zip_exclude_packages=["*"],
        )

    # zip_include_packages and zip_exclude_packages has the same package
    with pytest.raises(OptionError, match="package 'tkinter' cannot be both"):
        freezer = Freezer(
            executables=[Executable("hello.py")],
            zip_include_packages=["tkinter"],
            zip_exclude_packages=["tkinter"],
        )
    with pytest.raises(
        OptionError, match="packages 'tkinter, unittest' cannot be both"
    ):
        freezer = Freezer(
            executables=[Executable("hello.py")],
            zip_include_packages=["tkinter", "unittest"],
            zip_exclude_packages=["tkinter", "unittest", "codeop"],
        )

    # zip_include_packages and zip_exclude_packages are namespace packages
    freezer = Freezer(
        executables=[Executable("hello.py")],
        zip_include_packages=["namespace.test"],
        zip_exclude_packages=["zope.event", "zope.interface"],
    )
    assert freezer.zip_include_packages == {"namespace"}
    assert freezer.zip_exclude_packages == {"zope"}
    assert freezer.zip_include_all_packages is False
