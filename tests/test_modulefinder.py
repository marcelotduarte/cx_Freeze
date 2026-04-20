"""Test ModuleFinder."""

from __future__ import annotations

import os
import py_compile
import sys

import pytest

from cx_Freeze import ConstantsModule, ModuleFinder

from .datatest import (
    A_MODULE,
    ABSOLUTE_IMPORT_TEST,
    BYTECODE_INVALID_TEST,
    BYTECODE_TEST,
    CODING_DEFAULT_UTF8_TEST,
    CODING_EXPLICIT_CP1252_TEST,
    CODING_EXPLICIT_UTF8_TEST,
    EDITABLE_PACKAGE_TEST,
    EDITABLE_PACKAGE_TEST_1,
    EXTENDED_OPARGS_TEST,
    FIND_SPEC_TEST,
    INVALID_MODULE_NAME_TEST,
    MAYBE_TEST,
    MAYBE_TEST_NEW,
    NAMESPACE_TEST,
    NAMESPACE_TEST_1,
    NAMESPACE_TEST_2,
    OPTIMIZE_0_TEST,
    OPTIMIZE_1_TEST,
    OPTIMIZE_2_TEST,
    PACKAGE_TEST,
    RELATIVE_IMPORT_TEST,
    RELATIVE_IMPORT_TEST_2,
    RELATIVE_IMPORT_TEST_3,
    RELATIVE_IMPORT_TEST_4,
    SAME_NAME_AS_BAD_TEST,
    SCAN_CODE_IMPORT_CALL_TEST,
    SCAN_CODE_IMPORT_MODULE_TEST,
    SCAN_CODE_TEST,
    SUB_PACKAGE_TEST,
    SYNTAX_ERROR_TEST,
    SYNTAX_ERROR_TEST_1,
    SYNTAX_ERROR_TEST_2,
    ZIP_EXCLUDE_TEST,
    ZIP_INCLUDE_TEST,
)

# Each test description is a list of 6 items:
#
# 1. a module name that will be imported by ModuleFinder
# 1.1. to import a package, use 'package:' prefix, e.g, "package:foo"
# 2. a list of module names that ModuleFinder is required to find
# 3. a list of module names that ModuleFinder should complain
#    about because they are not found
# 4. a list of module names that ModuleFinder should complain
#    about because they MAY be not found
# 5. a string specifying packages to create; the format is obvious imo.
# 6. a dictionary of ModuleFinder kwargs.
#
# Each package will be created in test_dir, and test_dir will be
# removed after the tests again.
# ModuleFinder searches in a path that contains test_dir, plus
# the standard path search directory.


def _do_test(
    test_dir,
    import_this: str,
    modules: list[str],
    missing: list[str],
    maybe_missing: list[str],  # noqa: ARG001
    source: str,
    report=False,
    debug=0,  # noqa: ARG001
    modulefinder_class=ModuleFinder,
    **kwargs,
) -> None:
    test_dir.create(source)
    path = kwargs.pop("path", sys.path)
    finder = modulefinder_class(
        ConstantsModule(), path=[test_dir.path, *path], **kwargs
    )
    if import_this.startswith("package:"):
        module = finder.include_package(import_this.removeprefix("package:"))
    else:
        module = finder.include_module(import_this)
    if report:
        finder.report_missing_modules()
    modules = sorted(set(modules))
    found = sorted([m.name for m in finder.modules])
    # check if we found what we expected, not more, not less
    assert found == modules
    if module.error_msg:
        assert module.name in missing


@pytest.mark.parametrize(
    ("import_this", "modules", "missing", "maybe_missing", "source", "kwargs"),
    [
        ABSOLUTE_IMPORT_TEST,
        BYTECODE_INVALID_TEST,
        CODING_DEFAULT_UTF8_TEST,
        CODING_EXPLICIT_CP1252_TEST,
        CODING_EXPLICIT_UTF8_TEST,
        EXTENDED_OPARGS_TEST,
        FIND_SPEC_TEST,
        INVALID_MODULE_NAME_TEST,
        MAYBE_TEST,
        MAYBE_TEST_NEW,
        NAMESPACE_TEST,
        NAMESPACE_TEST_1,
        NAMESPACE_TEST_2,
        OPTIMIZE_0_TEST,
        OPTIMIZE_1_TEST,
        OPTIMIZE_2_TEST,
        PACKAGE_TEST,
        RELATIVE_IMPORT_TEST,
        RELATIVE_IMPORT_TEST_2,
        RELATIVE_IMPORT_TEST_3,
        RELATIVE_IMPORT_TEST_4,
        SAME_NAME_AS_BAD_TEST,
        SCAN_CODE_TEST,
        SCAN_CODE_IMPORT_CALL_TEST,
        SCAN_CODE_IMPORT_MODULE_TEST,
        SUB_PACKAGE_TEST,
        SYNTAX_ERROR_TEST,
        SYNTAX_ERROR_TEST_1,
        SYNTAX_ERROR_TEST_2,
        ZIP_EXCLUDE_TEST,
        ZIP_INCLUDE_TEST,
    ],
    ids=[
        "absolute_import_test",
        "bytecode_invalid_test",
        "coding_default_utf8_test",
        "coding_explicit_cp1252_test",
        "coding_explicit_utf8_test",
        "extended_opargs_test",
        "find_spec_test",
        "invalid_module_name_test",
        "maybe_test",
        "maybe_test_new",
        "namespace_test",
        "namespace_test_1",
        "namespace_test_2",
        "optimize_0_test",
        "optimize_1_test",
        "optimize_2_test",
        "package_test",
        "relative_import_test",
        "relative_import_test_2",
        "relative_import_test_3",
        "relative_import_test_4",
        "same_name_as_bad_test",
        "scan_code_test",
        "scan_code_import_call_test",
        "scan_code_import_module_test",
        "sub_package_test",
        "syntax_error_test",
        "syntax_error_test_1",
        "syntax_error_test_2",
        "zip_exclude_test",
        "zip_include_test",
    ],
)
def test_finder(
    tmp_package, import_this, modules, missing, maybe_missing, source, kwargs
) -> None:
    """Provides test cases for ModuleFinder class."""
    _do_test(
        tmp_package,
        import_this,
        modules,
        missing,
        maybe_missing,
        source,
        **kwargs,
    )


def test_bytecode(tmp_package) -> None:
    """Provides bytecode test case for ModuleFinder class."""
    tmp_package.create(BYTECODE_TEST[4])
    source_path = tmp_package.path / "a.py"
    bytecode_path = source_path.with_suffix(".pyc")
    py_compile.compile(os.fspath(source_path), cfile=os.fspath(bytecode_path))
    os.remove(source_path)
    _do_test(tmp_package, *BYTECODE_TEST)


@pytest.mark.parametrize(
    ("import_this", "modules", "missing", "maybe_missing", "source", "kwargs"),
    [EDITABLE_PACKAGE_TEST, EDITABLE_PACKAGE_TEST_1],
    ids=["editable_package_test", "editable_package_test_1"],
)
def test_editable_packages(
    tmp_package, import_this, modules, missing, maybe_missing, source, kwargs
) -> None:
    """Provides test cases for ModuleFinder class."""
    tmp_package.create(source)
    tmp_package.install(["-e", f"{tmp_package.path}/foo-bar"], backend="pip")
    _do_test(
        tmp_package,
        import_this,
        modules,
        missing,
        maybe_missing,
        source,
        **kwargs,
    )


def test_load_module_code(tmp_package) -> None:
    """Test case for _load_module_code method of ModuleFinder class."""
    tmp_package.create(A_MODULE[4])

    finder = ModuleFinder(
        ConstantsModule(), path=[tmp_package.path, *sys.path]
    )
    module = finder.include_module("a")
    module.loader = None  # to coverage the error handler in _load_module_code
    deferred_imports = []
    finder._load_module_code(module, deferred_imports)  # noqa: SLF001

    path = tmp_package.path / "a.py"
    msg = f"Unknown module loader in {path}"
    assert module.error_msg == msg
