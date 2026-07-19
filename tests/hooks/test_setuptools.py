"""Tests for some hooks of setuptools package."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest
from packaging.requirements import Requirement

from cx_Freeze._compat import IS_LINUX, IS_MACOS, IS_WINDOWS

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
    from importlib.metadata import version

    import setuptools
    import {package_1}
    import {package_2}

    print("Hello from cx_Freeze")
    print(setuptools.__name__, version("setuptools"))
    print({package_1}.__name__, version("{package_1}"))
    print({package_2}.__name__, version("{package_2}"))
pyproject.toml
    [project]
    name = "test_setuptools"
    version = "0.1.2.3"
    dependencies = [
        "{setuptools}{version}",
        "{package_1}{package_1v}",
        "{package_2}{package_2v}",
    ]

    [tool.cxfreeze]
    executables = ["test_setuptools.py"]

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["tkinter"]
    silent = true
"""

if IS_LINUX or IS_MACOS or IS_WINDOWS:
    SETUPTOOLS_VERSIONS = (
        "==78.1.1",
        "==80.9.0",
        "==80.10.2",
        "==81.0.0",
        "==82.0.0",
        "==83.0.0",
    )
else:
    SETUPTOOLS_VERSIONS = ("installed",)  # mingw, ...


@pytest.mark.venv
@zip_packages
@pytest.mark.parametrize("pkgver", SETUPTOOLS_VERSIONS)
def test_setuptools(
    tmp_package: TempPackage, zip_packages: bool, pkgver: str
) -> None:
    """Test if setuptools hook is working correctly."""
    setuptools = "setuptools"
    version = pkgver
    if pkgver == "installed":
        version = ">=78.1.1"
        package_1 = "jaraco.context"
        package_1v = ">6.1.0"
        package_2 = "platformdirs"
        package_2v = ">4.4.0"
    else:
        package_1 = "jaraco.collections"
        package_1v = ">5.1.0"
        package_2 = "jaraco.functools"
        package_2v = ">4.4.0"
    tmp_package.create(
        SOURCE_TEST_SETUPTOOLS.format(
            setuptools=setuptools,
            version=version,
            package_1=package_1,
            package_1v=package_1v,
            package_2=package_2,
            package_2v=package_2v,
        )
    )
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
            f"{package_1} *",
            f"{package_2} *",
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
