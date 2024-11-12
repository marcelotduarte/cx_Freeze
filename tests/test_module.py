import tempfile
from importlib.machinery import EXTENSION_SUFFIXES
from pathlib import Path

from cx_Freeze import Module

ROOT = Path(__file__).parent


def test_namespace_package():

    data = ROOT / "data"
    namespace = Module(
        name="namespace",
        path=[data / "namespace"],
        filename=None,
    )

    prefix = data / "namespace" / "foo" / "__init__"
    with tempfile.NamedTemporaryFile(
        "w",
        prefix=prefix.as_posix(),
        suffix=EXTENSION_SUFFIXES[-1],
    ) as f:
        f.write(prefix.with_suffix(".py").read_text())
        foo = Module(
            name="namespace.foo",
            path=[data / "namespace" / "foo"],
            filename=f.name,
            parent=namespace,
        )

    assert foo.stub_code is None
    assert namespace.stub_code is None
