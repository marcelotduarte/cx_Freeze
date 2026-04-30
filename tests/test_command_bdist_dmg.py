"""Tests for cx_Freeze.command.bdist_dmg."""

from __future__ import annotations

import pytest
from setuptools import Distribution

from cx_Freeze._compat import IS_MACOS
from cx_Freeze.command.bdist_dmg import bdist_dmg
from cx_Freeze.exception import PlatformError

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "description": "cx_Freeze script to test bdist_dmg",
    "executables": ["hello.py"],
    "script_name": "setup.py",
    "author": "Marcelo Duarte",
    "author_email": "marcelotduarte@users.noreply.github.com",
    "url": "https://github.com/marcelotduarte/cx_Freeze/",
}


@pytest.mark.skipif(IS_MACOS, reason="Test for non-macOS platform")
def test_bdist_dmg_in_non_macos() -> None:
    """Test the bdist_dmg fail in non-macOS."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_dmg(dist)
    msg = "bdist_dmg is only supported on macOS"
    with pytest.raises(PlatformError, match=msg):
        cmd.finalize_options()


@pytest.mark.skipif(not IS_MACOS, reason="macOS test")
@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        pytest.param(
            {},
            {"volume_label": "foo-0.0"},
            id="volume_label=none",
        ),
        pytest.param(
            {"volume_label": "simple test"},
            {"volume_label": "simple test"},
            id='volume_label="simple test"',
        ),
    ],
)
def test_bdist_dmg_call(
    kwargs: dict[str, ...], expected: dict[str, ...]
) -> None:
    """Test the bdist_dmg with options."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_dmg(dist, **kwargs)
    cmd.finalize_options()
    for option, value in expected.items():
        assert getattr(cmd, option) == value


@pytest.mark.skipif(not IS_MACOS, reason="macOS test")
def test_bdist_dmg(tmp_package) -> None:
    """Test the simple sample with bdist_dmg."""
    name = "Howdy Yall"
    dist_created = tmp_package.path / "build"

    tmp_package.create_from_sample("dmg")
    result = tmp_package.freeze("python setup.py bdist_dmg")
    if result.ret != 0:
        msg = str(result.stderr)
        expected_err = "bdist_dmg: Unable to "
        if expected_err in msg:
            pytest.xfail(expected_err)
        else:
            pytest.fail(msg)

    file_created = dist_created / f"{name}.dmg"
    assert file_created.is_file(), f"{name}.dmg"


@pytest.mark.skipif(not IS_MACOS, reason="macOS test")
def test_bdist_dmg_custom_layout(tmp_package) -> None:
    """Test the simple sample with bdist_dmg."""
    name = "Howdy Yall"
    dist_created = tmp_package.path / "build"

    tmp_package.create_from_sample("dmg_layout")
    result = tmp_package.freeze("python setup.py bdist_dmg")
    if result.ret != 0:
        msg = str(result.stderr)
        expected_err = "bdist_dmg: Unable to "
        if expected_err in msg:
            pytest.xfail(expected_err)
        else:
            pytest.fail(msg)

    file_created = dist_created / f"{name}.dmg"
    assert file_created.is_file(), f"{name}.dmg"
