"""Tests for cx_Freeze.command.bdist_msi."""

from __future__ import annotations

import pytest
from setuptools import Distribution

from cx_Freeze._compat import IS_ARM_64, IS_MINGW, IS_WINDOWS, IS_X86_64
from cx_Freeze.command.bdist_msi import bdist_msi
from cx_Freeze.exception import OptionError

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
    assert cmd.fullname == "foo-0.0.0"
    assert cmd.output_name == f"foo-0.0.0-{MSI_PLATFORM}.msi"


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_target_name() -> None:
    """Test the bdist_msi with extra target_name [removed] option."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_msi(dist)
    cmd.target_name = "mytest"
    msg = "target_name option was removed, use output_name"
    with pytest.raises(OptionError, match=msg):
        cmd.finalize_options()


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_target_version() -> None:
    """Test the bdist_msi with extra target_version [removed] option."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_msi(dist)
    cmd.target_version = "0.1"
    msg = "target_version option was removed,"
    with pytest.raises(OptionError, match=msg):
        cmd.finalize_options()


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_no_name() -> None:
    """Test the bdist_msi with no project name option."""
    dist = Distribution(
        {"executables": ["hello.py"], "script_name": "setup.py"}
    )
    cmd = bdist_msi(dist)
    cmd.target_name = "mytest"
    msg = "target_name option was removed, use output_name"
    with pytest.raises(OptionError, match=msg):
        cmd.finalize_options()


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_product_name() -> None:
    """Test the bdist_msi with extra product_name option."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_msi(dist)
    cmd.product_name = "my test"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "my test-0.0.0"
    assert cmd.output_name == f"my test-0.0.0-{MSI_PLATFORM}.msi"


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_product_name_and_version() -> None:
    """Test the bdist_msi with extra target options."""
    dist = Distribution(DIST_ATTRS)
    cmd = bdist_msi(dist)
    cmd.product_name = "mytest"
    cmd.product_version = "0.1"
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.fullname == "mytest-0.1"
    assert cmd.output_name == f"mytest-0.1-{MSI_PLATFORM}.msi"


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
def test_bdist_msi_output_name_with_extension(tmp_package) -> None:
    """Test the msi_extensions sample, with a specified output_name that
    includes an ".msi" extension.
    """
    msi_name = "output.msi"
    tmp_package.create_from_sample("msi_extensions")
    tmp_package.freeze(f"python setup.py bdist_msi --output-name {msi_name}")
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
    tmp_package.freeze(f"python setup.py bdist_msi --output-name {msi_name}")
    file_created = tmp_package.path / "dist" / msi_name
    assert file_created.is_file()


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_asmodule(tmp_package) -> None:
    """Test the asmodule sample."""
    msi_name = "output.msi"

    tmp_package.create_from_sample("asmodule")
    tmp_package.freeze(f"python setup.py bdist_msi --output-name {msi_name}")
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
    product_name = "Hello cx_Freeze"
    product_version = "0.1.2.3"
    output_name = "output.msi"
"""


@pytest.mark.skipif(not (IS_WINDOWS or IS_MINGW), reason="Windows test")
def test_bdist_msi_advanced2(tmp_package) -> None:
    """Test the executables option."""
    tmp_package.create(SOURCE_HELLO)
    tmp_package.freeze("cxfreeze bdist_msi")
    file_created = tmp_package.path / "dist" / "output.msi"
    assert file_created.is_file()
