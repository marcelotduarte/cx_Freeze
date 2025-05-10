"""Tests for cx_Freeze.hooks of pillow."""

from __future__ import annotations

import shutil
import sys
from importlib.resources import files

import pytest

from cx_Freeze._compat import IS_ARM_64, IS_WINDOWS

SOURCE_TEST_PILLOW = """
test_pillow.py
    import os.path
    import sys

    from PIL import Image


    def find_data_file(filename) -> str:
        if getattr(sys, "frozen", False):
            # The application is frozen
            datadir = os.path.join(sys.prefix, "share")
        else:
            # The application is not frozen
            # Change this bit to match where you store your data files:
            datadir = os.path.dirname(__file__)
        return os.path.join(datadir, filename)


    print("Hello from cx_Freeze: Opening image with PIL")

    filename_png = find_data_file("icon.png")
    filename_pdf = os.path.join(
        os.path.dirname(filename_png), "test_pillow.pdf"
    )
    with Image.open(filename_png) as im, open(filename_pdf, "w+b") as fp:
        if im.mode == "RGBA":
            im2 = im.convert("RGB")
            im2.save(fp, format="PDF")
        else:
            im.save(fp, format="PDF")
    print("OK")
pyproject.toml
    [project]
    name = "test_pillow"
    version = "0.1.2.3"

    [tool.cxfreeze]
    executables = ["test_pillow.py"]

    [tool.cxfreeze.build_exe]
    include_files = [["icon.png", "share/icon.png"]]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""

if sys.version_info[:2] < (3, 12):
    PILLOW_VERSIONS = [
        pytest.param("pillow<10", False, id="pillow<10"),
        pytest.param("pillow<10", True, id="pillow<10][zip_packages"),
    ]
if sys.version_info[:2] == (3, 12):
    PILLOW_VERSIONS = [
        pytest.param("pillow<10.2", False, id="pillow<10.2"),
        pytest.param("pillow<10.2", True, id="pillow<10.2][zip_packages"),
    ]
else:
    PILLOW_VERSIONS = [
        pytest.param("pillow", False, id="pillow"),
        pytest.param("pillow", True, id="pillow][zip_packages"),
    ]


@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="pillow not supported in windows arm64",
    strict=True,
)
@pytest.mark.parametrize(("package", "zip_packages"), PILLOW_VERSIONS)
def test_pillow(tmp_package, package: str, zip_packages: bool) -> None:
    """Test if pillow hook is working correctly."""
    tmp_package.create(SOURCE_TEST_PILLOW)
    # use an icon: cp $SRC/cx_Freeze/icons/py.png $DST/icon.png
    src_dir = files("cx_Freeze").resolve()
    shutil.copyfile(src_dir / "icons/py.png", tmp_package.path / "icon.png")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.install(package)
    output = tmp_package.run()
    executable = tmp_package.executable("test_pillow")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    lines = output.splitlines()
    assert lines[0].startswith("Hello from cx_Freeze")
    assert lines[1] == "OK"
    assert len(lines) == 2
