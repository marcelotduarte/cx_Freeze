"""Tests for hooks of zeroconf."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import ABI_THREAD, IS_ARM_64, IS_CONDA, IS_WINDOWS

TIMEOUT_SLOW = 60 if IS_CONDA else 30

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)
SOURCE_TEST = """
test_zeroconf.py
    import zeroconf

    def main():
        print("Zeroconf imported successfully!")
        print(f"Zeroconf version: {zeroconf.__version__}")

    if __name__ == "__main__":
        main()
pyproject.toml
    [project]
    name = "test_zeroconf"
    version = "0.1.2.3"
    dependencies = ["zeroconf>=0.146.3"]

    [tool.cxfreeze]
    executables = ["test_zeroconf.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="zeroconf does not support Windows arm64",
    strict=True,
)
@pytest.mark.xfail(
    sys.version_info[:2] == (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="zeroconf does not support Python 3.13t",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_zeroconf(tmp_package, zip_packages: bool) -> None:
    """Test if zeroconf hook is working correctly."""
    tmp_package.create(SOURCE_TEST)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_zeroconf")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    result.stdout.fnmatch_lines(
        ["Zeroconf imported successfully!", "Zeroconf version: *"]
    )
