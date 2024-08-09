"""Tests for cx_Freeze.command.bdist_mac."""

from __future__ import annotations

import os
import plistlib
import sys
from importlib import import_module
from typing import TYPE_CHECKING

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import IS_MACOS

if TYPE_CHECKING:
    from pathlib import Path

bdist_mac = pytest.importorskip(
    "cx_Freeze.command.bdist_mac", reason="macOS tests"
).bdist_mac

if not IS_MACOS:
    pytest.skip(reason="macOS tests", allow_module_level=True)

SOURCE_SIMPLE = """\
hello.py
    import sys
    from datetime import datetime, timezone

    today = datetime.now(tz=timezone.utc)
    print("Hello from cx_Freeze")
    print(f"The current date is {today:%B %d, %Y %H:%M:%S}\n")

    print(f"Executable: {sys.executable}")
    print(f"Prefix: {sys.prefix}")
    print(f"Default encoding: {sys.getdefaultencoding()}")
    print(f"File system encoding: {sys.getfilesystemencoding()}\n")

    print("ARGUMENTS:")
    for arg in sys.argv:
        print(f"{arg}")
    print()

    print("PATH:")
    for path in sys.path:
        print(f"{path}")
    print()
setup.py
    from cx_Freeze import setup

    setup(
        name="hello",
        version="0.1.2.3",
        description="Sample cx_Freeze script",
        executables=["hello.py"],
    )
command
    python setup.py bdist_mac
"""


def test_bdist_mac(tmp_path: Path) -> None:
    """Test a simple sample with bdist_mac."""
    name = "hello"
    version = "0.1.2.3"
    base_name = f"{name}-{version}"
    create_package(tmp_path, SOURCE_SIMPLE)
    run_command(tmp_path)
    dist_created = tmp_path / "build"
    file_created = dist_created / f"{base_name}.app"
    assert file_created.is_dir(), f"{base_name}.app"


SOURCE_PLIST = """\
plist_data.py
    TEST_KEY = "TestKey"
    TEST_VALUE = "TextValue"
    BUILD_DIR = "Built_App"
    BUNDLE_NAME = "Bundle"
setup.py
    from cx_Freeze import setup
    from plist_data import BUILD_DIR, BUNDLE_NAME, TEST_KEY, TEST_VALUE

    setup(
        name="hello",
        version="0.1",
        description="Sample cx_Freeze script",
        executables=["hello.py"],
        options={
            "build": {"build_base": BUILD_DIR},
            "bdist_mac": {
                "bundle_name": BUNDLE_NAME,
                "plist_items": [(TEST_KEY, TEST_VALUE)],
            },
        },
    )
"""


def test_plist_items(tmp_path: Path) -> None:
    """Test that the plist_items option is working correctly."""
    create_package(tmp_path, SOURCE_SIMPLE)
    create_package(tmp_path, SOURCE_PLIST)
    run_command(tmp_path)
    # Test that the additional keys were correctly added to the plist.
    sys.path.insert(0, os.fspath(tmp_path))
    data = import_module("plist_data")
    path = f"{data.BUILD_DIR}/{data.BUNDLE_NAME}.app/Contents/Info.plist"
    contents = plistlib.loads(tmp_path.joinpath(path).read_bytes())
    # compare contents of Info.plist with provided data
    assert contents[data.TEST_KEY] == data.TEST_VALUE
