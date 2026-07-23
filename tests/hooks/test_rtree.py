"""Tests for hooks of rtree."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.conftest import TempPackage

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_RTREE = """
test_rtree.py
    import rtree
    import rtree.finder
    import rtree.index

    print("Hello from cx_Freeze")
    print("rtree version", rtree.__version__)
    print("rtree file", rtree.__file__)
    rt = rtree.finder.load()
    print("rtree lib", rt)

    idx = rtree.index.Index()
    idx.add(1, (2, 2))
    idx.add(1, (3, 3))
    print(list(idx.intersection((0, 0, 5, 5))))
pyproject.toml
    [project]
    name = "test_rtree"
    version = "0.1.2.3"
    dependencies = ["rtree"]

    [tool.cxfreeze]
    executables = ["test_rtree.py"]

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["tkinter"]
    silent = true
"""


@pytest.mark.venv
@zip_packages
def test_rtree(tmp_package: TempPackage, zip_packages: bool) -> None:
    """Test if rtree hook is working correctly."""
    tmp_package.create(SOURCE_TEST_RTREE)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_rtree")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)

    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "rtree version *",
            "rtree file *",
            "rtree lib *",
            "[1, 1]",
        ]
    )
