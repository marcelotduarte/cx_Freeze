"""Tests for cx_Freeze.command.bdist_dmg."""

from __future__ import annotations

import sys

import pytest

bdist_dmg = pytest.importorskip(
    "cx_Freeze.command.bdist_dmg", reason="macOS tests"
).bdist_dmg

if sys.platform != "darwin":
    pytest.skip(reason="macOS tests", allow_module_level=True)


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
