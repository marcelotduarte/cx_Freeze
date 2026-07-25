"""Tests for cx_Freeze.command.bdist_mac."""

from __future__ import annotations

import plistlib
from copy import deepcopy
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

    tmp_package.create_from_sample("simple")
    attrs = deepcopy(DIST_ATTRS)
    attrs["name"] = name
    attrs["version"] = version
    dist = Distribution(attrs)
    cmd = bdist_mac(dist, bundle_name=name)
    cmd.finalize_options()
    cmd.run()

    app_created = tmp_package.path / "build" / f"{name}.app"
    assert app_created.is_dir(), f"{name}.app"

    info_plist = app_created / "Contents" / "Info.plist"
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
