"""Tests for hooks of compression.zstd."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest

from cx_Freeze._compat import IS_MINGW

if TYPE_CHECKING:
    from pathlib import Path

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST = """
test_zstd.py
    import sys

    if sys.version_info >= (3, 14):
        try:
            from compression import zstd
        except ModuleNotFoundError as exc:
            print(exc, file=sys.stderr)
            sys.exit(1)
        import tarfile
        import zipfile
    else:
        from backports import zstd
        from backports.zstd import tarfile
        from backports.zstd import zipfile


    print("Hello from cx_Freeze")
    options = {
       zstd.CompressionParameter.checksum_flag: 1
    }
    with zstd.open("hello.zst", "w", options=options) as f:
        f.write(b"Hello from cx_Freeze")

    with open("hello.txt", "w") as f:
        f.write("Hello from cx_Freeze")

    with tarfile.open("hello.tar.zst", "w:zst") as tf:
        tf.add("hello.txt")

    with zipfile.ZipFile("hello.zip", "w") as zf:
        zf.write("hello.txt", compress_type=zipfile.ZIP_ZSTANDARD)
pyproject.toml
    [project]
    name = "test_zstd"
    version = "0.1.2.3"
    dependencies = [
        "backports.zstd ; python_version < '3.14'",
    ]

    [tool.cxfreeze]
    executables = ["test_zstd.py"]

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "unittest"]
    include_msvcr = true
    silent = true
"""


@pytest.mark.xfail(
    IS_MINGW,
    raises=ModuleNotFoundError,
    reason="backports.zstd not supported in mingw",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_zstd(tmp_package, zip_packages: bool) -> None:
    """Test if compression.zstd hook is working correctly."""
    tmp_package.create(SOURCE_TEST)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_zstd")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    if result.ret != 0 and sys.version_info[:2] >= (3, 14):
        result.stderr.fnmatch_lines("No module named '_zstd'")
        pytest.xfail("zstd is not available in your version of Python")
    result.stdout.fnmatch_lines("Hello from cx_Freeze")
    cwd: Path = tmp_package.path
    assert cwd.joinpath("hello.zst").is_file()
    assert cwd.joinpath("hello.txt").is_file()
    assert cwd.joinpath("hello.tar.zst").is_file()
    assert cwd.joinpath("hello.zip").is_file()
