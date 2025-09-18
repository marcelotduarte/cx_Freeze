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
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("hello")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=10)
    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "The current date is *",
            "",
            "Executable:*",
            "Prefix:*",
            "Default encoding:*",
            "File system encoding:*",
            "",
            "BUILD_CONSTANTS variables:",
            "BUILD_COPYRIGHT = 'Copyright (C) *",
            "BUILD_HOST = *",
            "BUILD_RELEASE_STRING = *",
            "BUILD_TIMESTAMP = *",
            "SOURCE_TIMESTAMP = *",
            "USERDEFINED_A = 7",
            "USERDEFINED_B = 'hello=7'",
            "USERDEFINED_C = ''",
            "USER_UNDEFINED = None",
        ]
    )


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
    include_msvcr = true
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

    tmp_package.freeze()
    executable = tmp_package.executable("test_egg_info")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=10)
    result.stdout.fnmatch_lines(
        ["Hello from cx_Freeze", "Hello module1", "Hello module2"]
    )
