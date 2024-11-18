"""Tests for cx_Freeze.module."""

from importlib.machinery import EXTENSION_SUFFIXES
from pathlib import Path
from types import CodeType

from generate_samples import create_package

from cx_Freeze import Module

SOURCE = """
namespacepack/firstchildpack/__init__{extension}
    from .foo import FOO
namespacepack/firstchildpack/__init__.pyi
    from .foo import FOO
namespacepack/firstchildpack/foo.py
    FOO = 42
"""


def test_implicit_namespace_package(tmp_path: Path) -> None:
    """Test `Module.stub_code` with a namespace package.

    Implicit namespace packages do not contain an `__init__.py`. Thus
    `Module.root.file` becomes `None`. This test checks that
    `Module.stub_code` does not raise errors in this scenario.
    """
    ext = EXTENSION_SUFFIXES[-1]
    create_package(tmp_path, SOURCE.format(extension=ext))

    root = tmp_path / "namespacepack"
    namespacepack = Module(
        name="namespacepack",
        path=[tmp_path],
        filename=None,
    )
    firstchildpack = Module(
        name="namespacepack.firstchildpack",
        path=[root / "firstchildpack"],
        filename=root / "firstchildpack" / f"__init__{ext}",
        parent=namespacepack,
    )
    assert isinstance(firstchildpack.stub_code, CodeType)
    assert namespacepack.stub_code is None
