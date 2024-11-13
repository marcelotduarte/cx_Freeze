"""Tests for cx_Freeze.module."""

from collections.abc import Generator
from importlib.machinery import EXTENSION_SUFFIXES
from pathlib import Path

import pytest

from cx_Freeze import Module

ROOT = Path(__file__).parent


@pytest.fixture
def namespace() -> Module:
    """Return implicit namespace package ``namespace``."""
    data = ROOT / "data"
    return Module(
        name="namespace",
        path=[data / "namespace"],
        filename=None,
    )


@pytest.fixture
def foo(namespace: Module) -> Generator[Module, None, None]:
    """Return extension module ``namespace.foo.__init__``."""
    data = ROOT / "data"
    prefix = data / "namespace" / "foo" / "__init__"
    tempfile = Path(prefix.with_suffix(EXTENSION_SUFFIXES[-1]))
    try:
        tempfile.write_text(prefix.with_suffix(".py").read_text())
        yield Module(
            name="namespace.foo",
            path=[data / "namespace" / "foo"],
            filename=tempfile,
            parent=namespace,
        )
    finally:
        tempfile.unlink()


def test_implicit_namespace_package(foo: Module, namespace: Module) -> None:
    """Test `Module.stub_code` with a namespace package.

    Implicit namespace packages do not contain an `__init__.py`. Thus
    `Module.root.file` becomes `None`. This test checks that
    `Module.stub_code` does not raise errors in this scenario.
    """
    assert foo.stub_code is None
    assert namespace.stub_code is None
