"""Tests for hooks of comtypes."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.conftest import TempPackage

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_COMTYPES = """
test_comtypes.py
    import importlib.util

    import comtypes

    print("Hello from cx_Freeze")
    print("comtypes imported", comtypes.__name__)
    print(
        "comtypes.stream found",
        importlib.util.find_spec("comtypes.stream") is not None,
    )

test_comtypes_client.py
    import importlib.util

    from comtypes.client import GetModule

    print("GetModule imported", GetModule.__name__)
    print(
        "comtypes.stream found",
        importlib.util.find_spec("comtypes.stream") is not None,
    )

pyproject.toml
    [project]
    name = "test_comtypes"
    version = "0.1.2.3"
    dependencies = ["comtypes"]

    [tool.cxfreeze]
    executables = ["test_comtypes.py", "test_comtypes_client.py"]

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.venv(scope="module", install_dependencies=False)
@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
@zip_packages
def test_comtypes(tmp_package: TempPackage, zip_packages: bool) -> None:
    """Test if comtypes hook is working correctly."""
    tmp_package.create(SOURCE_TEST_COMTYPES)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    try:
        tmp_package.install_dependencies()
    except ModuleNotFoundError as exc:
        pytest.skip(f"Depends on extra package: {exc}")
    tmp_package.freeze()

    executable = tmp_package.executable("test_comtypes")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "comtypes imported comtypes",
            "comtypes.stream found True",
        ]
    )

    executable = tmp_package.executable("test_comtypes_client")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(
        [
            "GetModule imported GetModule",
            "comtypes.stream found True",
        ]
    )
