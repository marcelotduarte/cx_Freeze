"""Tests for cx_Freeze.command.bdist_mac."""

from __future__ import annotations

import os
import plistlib
import sys
from copy import deepcopy
from importlib import import_module
from typing import TYPE_CHECKING, Any

import pytest
from setuptools import Distribution

from cx_Freeze._compat import IS_MACOS
from cx_Freeze.command.bdist_mac import bdist_mac
from cx_Freeze.exception import PlatformError

if TYPE_CHECKING:
    from tests.conftest import TempPackage

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "description": "cx_Freeze script to test bdist_mac",
    "executables": ["hello.py"],
    "script_name": "setup.py",
    "author": "Marcelo Duarte",
    "author_email": "marcelotduarte@users.noreply.github.com",
    "url": "https://github.com/marcelotduarte/cx_Freeze/",
}


@pytest.mark.skipif(IS_MACOS, reason="Test for non-macOS platform")
def test_bdist_mac_in_non_macos() -> None:
    """Test the bdist_mac fail in non-macOS."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_mac(dist)
    msg = "bdist_mac is only supported on macOS"
    with pytest.raises(PlatformError, match=msg):
        cmd.finalize_options()


@pytest.mark.skipif(not IS_MACOS, reason="macOS test")
@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        pytest.param(
            {},
            {"bundle_name": "foo-0.0"},
            id="bundle_name=none",
        ),
        pytest.param(
            {"bundle_name": "simple test"},
            {"bundle_name": "simple test"},
            id='bundle_name="simple test"',
        ),
    ],
)
def test_bdist_mac_call(
    kwargs: dict[str, Any], expected: dict[str, Any]
) -> None:
    """Test the bdist_mac with options."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_mac(dist, **kwargs)
    cmd.finalize_options()
    for option, value in expected.items():
        assert getattr(cmd, option) == value


@pytest.mark.skipif(not IS_MACOS, reason="macOS test")
def test_bdist_mac(tmp_package: TempPackage) -> None:
    """Test the simple sample with bdist_mac."""
    name = "hello"
    version = "0.1.2.3"
    bundle_name = name

    tmp_package.create_from_sample("simple")
    attrs = deepcopy(DIST_ATTRS)
    attrs["name"] = name
    attrs["version"] = version
    dist = Distribution(attrs)
    cmd = bdist_mac(dist, bundle_name=bundle_name)
    cmd.finalize_options()
    cmd.run()

    build_app_dir = tmp_package.path / "build" / f"{bundle_name}.app"
    assert build_app_dir.is_dir(), f"{bundle_name}.app"

    executable = build_app_dir / "Contents/MacOS" / name
    assert executable.is_file()
    result = tmp_package.run(executable)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")

    info_plist = build_app_dir / "Contents" / "Info.plist"
    assert info_plist.exists(), "Info.plist"
    with info_plist.open("rb") as fp:
        contents = plistlib.load(fp)
    assert contents["CFBundleIconFile"] == "icon.icns"
    assert contents["CFBundleDevelopmentRegion"] == "English"
    assert contents["CFBundleIdentifier"] == name
    assert contents["CFBundlePackageType"] == "APPL"
    assert contents["NSHighResolutionCapable"] == "True"
    assert contents["CFBundleVersion"] == version
    assert contents["CFBundleExecutable"] == name


PLIST_TEST = """\
hello.py
    import sys
    from datetime import datetime
    print("Hello from cx_Freeze")
    print(f"The current date is {datetime.today():%B %d, %Y %H:%M:%S}")
    print(f"Executable: {sys.executable}")
    print(f"Prefix: {sys.prefix}")
    print(f"Default encoding: {sys.getdefaultencoding()}")
    print(f"File system encoding: {sys.getfilesystemencoding()}")
    print("ARGUMENTS:")
    for a in sys.argv: print(f"{a}")
    print()
    print("PATH:")
    for p in sys.path: print(f"{p}")
    print()
plist_data.py
    TEST_KEY = "TestKey"
    TEST_VALUE = "TextValue"
    BUILD_DIR = "Built_App"
    BUNDLE_NAME = "Bundle"
setup.py
    from plist_data import BUILD_DIR, BUNDLE_NAME, TEST_KEY, TEST_VALUE
    from cx_Freeze import setup

    setup(
        name="hello",
        version="0.1",
        description="Sample cx_Freeze script",
        options={
            "build": {
                "build_base": BUILD_DIR,
            },
            "build_exe": {
                "silent": True,
            },
            "bdist_mac": {
                "bundle_name": BUNDLE_NAME,
                "plist_items": [(TEST_KEY, TEST_VALUE)],
            },
        },
        executables=["hello.py"],
    )
command
    python setup.py bdist_mac
"""


@pytest.mark.skipif(not IS_MACOS, reason="macOS test")
def test_bdist_mac_plist_items(tmp_package: TempPackage) -> None:
    """Test that the plist_items option is working correctly."""
    tmp_package.create(PLIST_TEST)
    tmp_package.freeze()
    # Test that the additional keys were correctly added to the plist.
    sys.path.insert(0, os.path.normpath(tmp_package.path))
    data = import_module("plist_data")
    path = tmp_package.path.joinpath(
        f"{data.BUILD_DIR}/{data.BUNDLE_NAME}.app/Contents/Info.plist"
    )
    assert path.exists()
    with path.open("rb") as fp:
        contents = plistlib.load(fp)
    assert contents[data.TEST_KEY] == data.TEST_VALUE
