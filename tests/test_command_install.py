"""Tests for cx_Freeze.command.install."""

from __future__ import annotations

import os
from pathlib import Path

from cx_Freeze._compat import EXE_SUFFIX, IS_MINGW, IS_WINDOWS

SOURCE_SETUP = """
test.py
    print("Hello from cx_Freeze")
setup.py
    from cx_Freeze import setup

    options = {
        "build_exe": {
            "include_msvcr": True,
            "excludes": ["tkinter", "unittest"],
            "silent": True
        }
    }
    setup(
        name="hello",
        version="0.1.2.3",
        description="Sample cx_Freeze script",
        executables=["test.py"],
        options=options,
    )

command
    python setup.py install --prefix=base --root=root
"""


def test_install(tmp_package) -> None:
    """Test a simple install."""
    tmp_package.create(SOURCE_SETUP)

    if IS_MINGW or IS_WINDOWS:
        tmp_package.freeze("python setup.py install --root=root")
        program_files = Path(os.getenv("PROGRAMFILES"))
        prefix = program_files.relative_to(program_files.anchor) / "hello"
    else:
        tmp_package.freeze()
        prefix = "base/lib/hello-0.1.2.3"
    install_dir = tmp_package.path / "root" / prefix

    file_created = install_dir / f"test{EXE_SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    result = tmp_package.run(file_created, timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")


SOURCE_PYPROJECT = """
test.py
    print("Hello from cx_Freeze")
pyproject.toml
    [project]
    name = "hello"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"

    [tool.cxfreeze]
    executables = ["test.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
command
    cxfreeze install --prefix=base --root=root
"""


def test_install_pyproject(tmp_package) -> None:
    """Test a simple install."""
    tmp_package.create(SOURCE_PYPROJECT)

    if IS_MINGW or IS_WINDOWS:
        tmp_package.freeze("cxfreeze install --root=root")
        program_files = Path(os.getenv("PROGRAMFILES"))
        prefix = program_files.relative_to(program_files.anchor) / "hello"
    else:
        tmp_package.freeze()
        prefix = "base/lib/hello-0.1.2.3"
    install_dir = tmp_package.path / "root" / prefix

    file_created = install_dir / f"test{EXE_SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    result = tmp_package.run(file_created, timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")
