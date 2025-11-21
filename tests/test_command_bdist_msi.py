"""Tests for cx_Freeze.command.bdist_msi."""

from __future__ import annotations

import pytest
from setuptools import Distribution

from cx_Freeze._compat import IS_ARM_64, IS_MINGW, IS_WINDOWS, IS_X86_64
from cx_Freeze.command.bdist_msi import bdist_msi

DIST_ATTRS = {
    "name": "foo",
    "executables": ["hello.py"],
    "script_name": "setup.py",
}
if IS_ARM_64:
    MSI_PLATFORM = "win-arm64"
elif IS_X86_64:
    MSI_PLATFORM = "win64"
else:
    MSI_PLATFORM = "win32"


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_target_dir() -> None:
    """Test the bdist_msi initial_target_dir option."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_msi(dist)
    cmd.finalize_options()
    cmd.ensure_finalized()
    if IS_ARM_64 or IS_X86_64:
        expected = r"[ProgramFiles64Folder]\foo"
    else:
        expected = r"[ProgramFilesFolder]\foo"
    assert cmd.initial_target_dir == expected
    assert cmd.fullname == "foo"
    assert cmd.target_name == "foo"


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_target_name() -> None:
    """Test the bdist_msi with extra target_name option."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_msi(dist)
    cmd.target_name = "mytest"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest"
    assert cmd.target_name == "mytest"


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_target_name_and_version() -> None:
    """Test the bdist_msi with extra target options."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_msi(dist)
    cmd.target_name = "mytest"
    cmd.target_version = "0.1"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.1"
    assert cmd.target_name == "mytest"


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_default(tmp_package) -> None:
    """Test the msi_binary_data sample."""
    tmp_package.create_from_sample("msi_binary_data")
    tmp_package.freeze("cxfreeze bdist_msi")
    file_created = (
        tmp_package.path / "dist" / f"hello-0.1.2.3-{MSI_PLATFORM}.msi"
    )
    assert file_created.is_file()


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_target_name_with_extension(tmp_package) -> None:
    """Test the msi_extensions sample, with a specified target_name that
    includes an ".msi" extension.
    """
    msi_name = "output.msi"
    tmp_package.create_from_sample("msi_extensions")
    tmp_package.freeze(f"python setup.py bdist_msi --target-name {msi_name}")
    file_created = tmp_package.path / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_target_name_with_extension_1(tmp_package) -> None:
    """Test the msi_summary_data sample."""
    msi_name = "output.1.msi"

    tmp_package.create_from_sample("msi_summary_data")
    tmp_package.freeze(f"python setup.py bdist_msi --target-name {msi_name}")
    file_created = tmp_package.path / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_with_license(tmp_package) -> None:
    """Test the msi_license sample."""
    msi_name = f"hello-0.1-{MSI_PLATFORM}.msi"

    tmp_package.create_from_sample("msi_license")
    tmp_package.freeze("python setup.py bdist_msi")
    file_created = tmp_package.path / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_advanced(tmp_package) -> None:
    """Test the advanced sample."""
    msi_name = "output.msi"

    tmp_package.create_from_sample("advanced")
    tmp_package.freeze(f"python setup.py bdist_msi --target-name {msi_name}")
    file_created = tmp_package.path / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_asmodule(tmp_package) -> None:
    """Test the asmodule sample."""
    msi_name = "output.msi"

    tmp_package.create_from_sample("asmodule")
    tmp_package.freeze(f"python setup.py bdist_msi --target-name {msi_name}")
    file_created = tmp_package.path / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_sqlite(tmp_package) -> None:
    """Test the sqlite sample."""
    msi_name = "output.msi"

    tmp_package.create_from_sample("sqlite")
    tmp_package.freeze(f"python setup.py bdist_msi --target-name {msi_name}")
    file_created = tmp_package.path / "dist" / msi_name
    assert file_created.is_file()


SOURCE_HELLO = """
hello.py
    import pkg.hi
    print("Hello from cx_Freeze")
pkg/hi.py
    print("Hi!")
pyproject.toml
    [project]
    name = "hello"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"
    authors = [{name = "cx_Freeze"}]

    [[tool.cxfreeze.executables]]
    script = "hello.py"

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "unittest"]

    [tool.cxfreeze.bdist_msi]
    target_name = "output.msi"
"""


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_advanced2(tmp_package) -> None:
    """Test the executables option."""
    tmp_package.create(SOURCE_HELLO)
    tmp_package.freeze("cxfreeze bdist_msi")
    file_created = tmp_package.path / "dist" / "output.msi"
    assert file_created.is_file()
