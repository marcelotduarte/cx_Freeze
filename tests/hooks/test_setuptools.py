"""Tests for some hooks of setuptools package."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest
from packaging.requirements import Requirement

if sys.version_info[:2] >= (3, 11):
    import tomllib
else:
    from setuptools.compat.py310 import tomllib

if TYPE_CHECKING:
    from packaging.specifiers import SpecifierSet

    from tests.conftest import TempPackage

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_SETUPTOOLS = """
test_setuptools.py
    import setuptools
    import jaraco.collections
    import jaraco.functools
    from importlib.metadata import version

    print("Hello from cx_Freeze")
    print(setuptools.__name__, version("setuptools"))
    print(jaraco.collections.__name__, version("jaraco.collections"))
    print(jaraco.functools.__name__, version("jaraco.functools"))
pyproject.toml
    [project]
    name = "test_setuptools"
    version = "0.1.2.3"
    dependencies = [
        "setuptools==78.1.1;python_version <= '3.12'",
        "setuptools==80.9.0;python_version == '3.13'",
        "setuptools==80.10.2;python_version == '3.14'",
        "setuptools>=81.0;python_version > '3.14'",
        # using versions greater than vendored by latest setuptools
        "jaraco.collections>5.1.0",
        "jaraco.functools>4.4.0",
    ]

    [tool.cxfreeze]
    executables = ["test_setuptools.py"]

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.venv
@zip_packages
def test_setuptools(tmp_package: TempPackage, zip_packages: bool) -> None:
    """Test if setuptools hook is working correctly."""
    tmp_package.create(SOURCE_TEST_SETUPTOOLS)
    pyproject = tmp_package.path / "pyproject.toml"
    if zip_packages:
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_setuptools")
    assert executable.is_file()
    result = tmp_package.run(executable)
    output = result.stdout
    output.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "setuptools *",
            "jaraco.collections *",
            "jaraco.functools *",
        ],
        consecutive=True,
    )

    # Check if installed versions are not from setuptools
    with pyproject.open("rb") as file:
        config = tomllib.load(file)
    dependencies = config["project"]["dependencies"]
    tools: list[tuple[str, str]] = [
        tuple(line.split(" ")) for line in output.lines[1:]
    ]
    installed: list[tuple[str, str, SpecifierSet]] = []
    for name, version in tools:
        for dep in dependencies:
            req = Requirement(dep)
            if req.name == name and (
                req.marker is None or req.marker.evaluate()
            ):
                installed.append((name, version, req.specifier))
    assert len(tools) == len(installed)
    for _name, version, specifier in installed:
        assert version in specifier
