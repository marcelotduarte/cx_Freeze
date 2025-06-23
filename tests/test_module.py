"""Tests for cx_Freeze.module."""

from __future__ import annotations

import os
import shutil
from importlib.machinery import EXTENSION_SUFFIXES
from types import CodeType

import pytest

from cx_Freeze import ConstantsModule, Module
from cx_Freeze._compat import IS_CONDA, IS_MINGW
from cx_Freeze.exception import OptionError

SOURCE = """
namespacepack/firstchildpack/__init__{extension}
    from .foo import FOO
namespacepack/firstchildpack/__init__.pyi
    from .foo import FOO
namespacepack/firstchildpack/foo.py
    FOO = 42
"""


def test_implicit_namespace_package(tmp_package) -> None:
    """Test `Module.stub_code` with a namespace package.

    Implicit namespace packages do not contain an `__init__.py`. Thus
    `Module.root.file` becomes `None`. This test checks that
    `Module.stub_code` does not raise errors in this scenario.
    """
    ext = EXTENSION_SUFFIXES[-1]
    tmp_package.create(SOURCE.format(extension=ext))

    root = tmp_package.path / "namespacepack"
    namespacepack = Module(
        name="namespacepack",
        path=[tmp_package.path],
        filename=None,
    )
    firstchildpack = Module(
        name="namespacepack.firstchildpack",
        path=[root / "firstchildpack"],
        filename=root / "firstchildpack" / f"__init__{ext}",
        parent=namespacepack,
    )
    assert isinstance(firstchildpack.stub_code, CodeType)
    assert namespacepack.stub_code is None


zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


@zip_packages
def test_build_constants(tmp_package, zip_packages: bool) -> None:
    """Test if build_constants is working correctly."""
    tmp_package.create_from_sample("build_constants")
    command = "python setup.py build_exe --excludes=tkinter,unittest --silent"
    if zip_packages:
        command += " --zip-include-packages=* --zip-exclude-packages="
    command += " --include-msvcr"
    output = tmp_package.run(command)

    executable = tmp_package.executable("hello")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    lines = output.splitlines()
    assert lines[0].startswith("Hello from cx_Freeze")
    assert lines[8].startswith("BUILD_CONSTANTS")
    assert lines[9].startswith("BUILD_COPYRIGHT = 'Copyright (C)")
    assert lines[14].startswith("USERDEFINED_A = 7")
    assert lines[15].startswith("USERDEFINED_B = 'hello=7'")
    assert lines[16].startswith("USERDEFINED_C = ''")
    assert lines[17].startswith("USER_UNDEFINED = None")


@pytest.mark.parametrize(
    ("class_to_test", "kwargs", "expected_exception", "expected_match"),
    [
        (ConstantsModule, {"constants": ["#1234=10"]}, OptionError, "Invalid"),
        (ConstantsModule, {"constants": ["def=20"]}, OptionError, "Invalid"),
    ],
    ids=["invalid-constant-isidentifier", "invalid-constant-iskeyword"],
)
def test_invalid(
    class_to_test, kwargs, expected_exception, expected_match
) -> None:
    """Test invalid values to use in ConstantsModule class."""
    with pytest.raises(expected_exception, match=expected_match):
        class_to_test(**kwargs)


SOURCE_TEST_EGG_INFO = """
test_egg_info.py
    print("Hello from cx_Freeze")
    import module1
    import module2
pyproject.toml
    [project]
    name = "test_egg_info"
    version = "0.1.2.3"

    [tool.cxfreeze]
    executables = ["test_egg_info.py"]

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "unittest"]
    silent = true
extra/module1.py
    print("Hello module1")
extra/module1.egg-info
    Name: module1
    Version: 1.0
extra/module2.py
    print("Hello module2")
extra/module2.egg-info/PKG-INFO
    Name: module2
    Version: 1.0
extra/module2.egg-info/entry_points.txt
    [distutils.setup_keywords]
    entry_points = setuptools.dist:check_entry_points
extra/module2.egg-info/top_level.txt
    module2
"""


@pytest.mark.skipif(IS_MINGW, reason="Disabled in MinGW")
@pytest.mark.skipif(IS_CONDA, reason="Disabled in conda-forge")
def test_egg_info(tmp_package) -> None:
    """Use fake packages to test conversion of egg_info to dist_info in
    DistributionCache.
    """
    tmp_package.create(SOURCE_TEST_EGG_INFO)

    # patch the fake packages
    tmp_package.prefix = tmp_package.path / ".tmp_prefix"
    tmp_site = tmp_package.prefix / tmp_package.relative_site
    shutil.copytree(tmp_package.path / "extra", tmp_site, dirs_exist_ok=True)
    tmp_package.monkeypatch.setenv("PYTHONPATH", os.path.normpath(tmp_site))

    output = tmp_package.run()
    executable = tmp_package.executable("test_egg_info")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    assert output.splitlines()[0] == "Hello from cx_Freeze"
    assert output.splitlines()[1].startswith("Hello module1")
    assert output.splitlines()[2].startswith("Hello module2")
