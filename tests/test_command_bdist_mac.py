"""Tests for cx_Freeze.command.bdist_mac."""

from __future__ import annotations

import pytest
from setuptools import Distribution

from cx_Freeze._compat import IS_MACOS
from cx_Freeze.command.bdist_mac import bdist_mac
from cx_Freeze.exception import PlatformError

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
    kwargs: dict[str, ...], expected: dict[str, ...]
) -> None:
    """Test the bdist_mac with options."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_mac(dist, **kwargs)
    cmd.finalize_options()
    for option, value in expected.items():
        assert getattr(cmd, option) == value


@pytest.mark.skipif(not IS_MACOS, reason="macOS test")
def test_bdist_mac(tmp_package) -> None:
    """Test the simple sample with bdist_mac."""
    name = "hello"
    version = "0.1.2.3"
    base_name = f"{name}-{version}"

    tmp_package.create_from_sample("simple")
    tmp_package.freeze("python setup.py bdist_mac")
    file_created = tmp_package.path / "build" / f"{base_name}.app"
    assert file_created.is_dir(), f"{base_name}.app"
