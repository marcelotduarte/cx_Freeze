"""Tests for hooks of pycparser."""

from __future__ import annotations

import pytest

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_PYCPARSER = """
test_pycparser.py
    import pycparser

    print("Hello from cx_Freeze")
    print("pycparser version", pycparser.__version__)

    text = r'''
    void func(void)
    {
      x = 1;
    }
    '''

    if __name__ == "__main__":
        parser = pycparser.c_parser.CParser()
        ast = parser.parse(text)
        print("Before:")
        ast.show(offset=2)

        assign = ast.ext[0].body.block_items[0]
        assign.lvalue.name = "y"
        assign.rvalue.value = 2

        print("After:")
        ast.show(offset=2)
pyproject.toml
    [project]
    name = "test_pycparser"
    version = "0.1.2.3"
    dependencies = [
        "pycparser<3.0;python_version < '3.12'",
        "pycparser>=3.0;python_version >= '3.12'",
    ]

    [tool.cxfreeze]
    executables = ["test_pycparser.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.venv
@zip_packages
def test_pycparser(tmp_package, zip_packages: bool) -> None:
    """Test if pycparser hook is working correctly."""
    tmp_package.create(SOURCE_TEST_PYCPARSER)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_pycparser")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(
        ["Hello from cx_Freeze", "pycparser version *"]
    )
