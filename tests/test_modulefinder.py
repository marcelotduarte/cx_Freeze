"""Test ModuleFinder."""

from __future__ import annotations

import os
import py_compile
import sys
from importlib.machinery import BYTECODE_SUFFIXES, SOURCE_SUFFIXES

import pytest
from generate_samples import (
    ABSOLUTE_IMPORT_TEST,
    BYTECODE_TEST,
    CODING_DEFAULT_UTF8_TEST,
    CODING_EXPLICIT_CP1252_TEST,
    CODING_EXPLICIT_UTF8_TEST,
    EXTENDED_OPARGS_TEST,
    IMPORT_CALL_TEST,
    MAYBE_TEST,
    MAYBE_TEST_NEW,
    NAMESPACE_TEST,
    NESTED_NAMESPACE_TEST,
    PACKAGE_TEST,
    RELATIVE_IMPORT_TEST,
    RELATIVE_IMPORT_TEST_2,
    RELATIVE_IMPORT_TEST_3,
    RELATIVE_IMPORT_TEST_4,
    SAME_NAME_AS_BAD_TEST,
    SUB_PACKAGE_TEST,
    create_package,
)

from cx_Freeze import ConstantsModule, ModuleFinder

# Each test description is a list of 5 items:
#
# 1. a module name that will be imported by ModuleFinder
# 2. a list of module names that ModuleFinder is required to find
# 3. a list of module names that ModuleFinder should complain
#    about because they are not found
# 4. a list of module names that ModuleFinder should complain
#    about because they MAY be not found
# 5. a string specifying packages to create; the format is obvious imo.
#
# Each package will be created in test_dir, and test_dir will be
# removed after the tests again.
# ModuleFinder searches in a path that contains test_dir, plus
# the standard path search directory.


def _do_test(
    test_dir,
    import_this,
    modules,
    missing,  # noqa: ARG001
    maybe_missing,  # noqa: ARG001
    source,
    report=False,
    debug=0,  # noqa: ARG001
    modulefinder_class=ModuleFinder,
    **kwargs,
) -> None:
    create_package(test_dir, source)
    finder = modulefinder_class(
        ConstantsModule(), path=[test_dir, *sys.path], **kwargs
    )
    finder.include_module(import_this)
    if report:
        finder.report_missing_modules()
    modules = sorted(set(modules))
    found = sorted([module.name for module in finder.modules])
    # check if we found what we expected, not more, not less
    assert found == modules


@pytest.mark.parametrize(
    ("import_this", "modules", "missing", "maybe_missing", "source"),
    [
        ABSOLUTE_IMPORT_TEST,
        CODING_DEFAULT_UTF8_TEST,
        CODING_EXPLICIT_CP1252_TEST,
        CODING_EXPLICIT_UTF8_TEST,
        EXTENDED_OPARGS_TEST,
        IMPORT_CALL_TEST,
        MAYBE_TEST,
        MAYBE_TEST_NEW,
        NAMESPACE_TEST,
        NESTED_NAMESPACE_TEST,
        PACKAGE_TEST,
        RELATIVE_IMPORT_TEST,
        RELATIVE_IMPORT_TEST_2,
        RELATIVE_IMPORT_TEST_3,
        RELATIVE_IMPORT_TEST_4,
        SAME_NAME_AS_BAD_TEST,
        SUB_PACKAGE_TEST,
    ],
    ids=[
        "absolute_import_test",
        "coding_default_utf8_test",
        "coding_explicit_cp1252_test",
        "coding_explicit_utf8_test",
        "extended_opargs_test",
        "import_call_test",
        "maybe_test",
        "maybe_test_new",
        "namespace_test",
        "nested_namespace_test",
        "package_test",
        "relative_import_test",
        "relative_import_test_2",
        "relative_import_test_3",
        "relative_import_test_4",
        "same_name_as_bad_test",
        "sub_package_test",
    ],
)
def test_finder(
    tmp_path,
    import_this,
    modules,
    missing,
    maybe_missing,
    source,
) -> None:
    """Provides test cases for ModuleFinder class."""
    _do_test(tmp_path, import_this, modules, missing, maybe_missing, source)


def test_bytecode(tmp_path) -> None:
    """Provides bytecode test case for ModuleFinder class."""
    base_path = tmp_path / "a"
    source_path = base_path.with_suffix(SOURCE_SUFFIXES[0])
    bytecode_path = base_path.with_suffix(BYTECODE_SUFFIXES[0])
    with source_path.open("wb") as file:
        file.write(b"testing_modulefinder = True\n")
    py_compile.compile(os.fspath(source_path), cfile=os.fspath(bytecode_path))
    os.remove(source_path)
    _do_test(tmp_path, *BYTECODE_TEST)


def test_zip_include_packages(tmp_path) -> None:
    """Provides test cases for ModuleFinder class."""
    _do_test(
        tmp_path,
        *SUB_PACKAGE_TEST,
        zip_exclude_packages=["*"],
        zip_include_packages=["p"],
        zip_include_all_packages=False,
    )


def test_zip_exclude_packages(tmp_path) -> None:
    """Provides test cases for ModuleFinder class."""
    _do_test(
        tmp_path,
        *SUB_PACKAGE_TEST,
        zip_exclude_packages=["p"],
        zip_include_packages=["*"],
        zip_include_all_packages=True,
    )
