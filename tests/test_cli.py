"""Tests for 'cxfreeze'."""

from __future__ import annotations

import contextlib
import sys
from importlib import import_module
from pathlib import Path
from subprocess import CalledProcessError

import pytest
from generate_samples import create_package, run_command

SUFFIX = ".exe" if sys.platform == "win32" else ""

SOURCE = """
test.py
    print("Hello from cx_Freeze")
command
    cxfreeze test.py --target-dir=dist --excludes=tkinter
"""


def test_cxfreeze(tmp_path: Path):
    """Test cxfreeze."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path)

    file_created = tmp_path / "dist" / f"test{SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_cxfreeze_help(tmp_path: Path):
    """Test cxfreeze help."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path, "cxfreeze --help")
    assert output.startswith("usage")


def test_cxfreeze_additional_help(tmp_path: Path):
    """Test cxfreeze additional help."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path, "cxfreeze build_exe --help")
    assert "usage: " in output


def test_cxfreeze_deprecated_option(tmp_path: Path):
    """Test cxfreeze deprecated option."""
    create_package(tmp_path, SOURCE)
    output = run_command(
        tmp_path, "cxfreeze -c test.py --target-dir=dist --excludes=tkinter"
    )
    assert "WARNING: deprecated" in output

    file_created = tmp_path / "dist" / f"test{SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_cxfreeze_without_options(tmp_path: Path):
    """Test cxfreeze without options."""
    create_package(tmp_path, SOURCE)
    with pytest.raises(CalledProcessError):
        run_command(tmp_path, "cxfreeze")


def test_import_tomli(monkeypatch):
    """Test using tomli as a last resort."""
    if sys.version_info >= (3, 11):
        monkeypatch.delattr("tomllib.loads")
    with contextlib.suppress(AttributeError, ModuleNotFoundError):
        monkeypatch.delattr("setuptools.extern.tomli.loads")
    # monkeypatch.delattr("tomli.loads")
    try:
        pyproject = import_module("cx_Freeze._pyproject")
    except ImportError as exc:
        pytest.xfail(reason=f"ImportError: {exc.args[0]}")
    assert pyproject.get_pyproject_tool_data
    assert pyproject.toml_loads.__module__.startswith("tomli.")
