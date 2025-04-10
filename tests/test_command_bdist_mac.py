"""Tests for cx_Freeze.command.bdist_mac."""

from __future__ import annotations

import sys

import pytest

bdist_mac = pytest.importorskip(
    "cx_Freeze.command.bdist_mac", reason="macOS tests"
).bdist_mac

if sys.platform != "darwin":
    pytest.skip(reason="macOS tests", allow_module_level=True)

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


def test_bdist_mac(tmp_package) -> None:
    """Test the simple sample with bdist_mac."""
    name = "hello"
    version = "0.1.2.3"
    base_name = f"{name}-{version}"

    tmp_package.create_from_sample("simple")
    tmp_package.run("python setup.py bdist_mac")
    file_created = tmp_package.path / "build" / f"{base_name}.app"
    assert file_created.is_dir(), f"{base_name}.app"
