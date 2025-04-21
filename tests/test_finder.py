"""Test ModuleFinder."""

from __future__ import annotations

import os

import pytest

from cx_Freeze import ConstantsModule, ModuleFinder

from .datatest import (
    FIND_SPEC_TEST,
    INVALID_MODULE_NAME_TEST,
    SCAN_CODE_TEST,
    SYNTAX_ERROR_TEST,
)


class TestModuleFinder:
    """Provides test cases for ModuleFinder class."""

    @pytest.fixture
    def fix_module_finder(self) -> ModuleFinder:
        constants = ConstantsModule()
        return ModuleFinder(constants_module=constants)

    def test_scan_code(self, tmp_package, fix_module_finder, mocker) -> None:
        tmp_package.create(SCAN_CODE_TEST[4])
        any3 = (mocker.ANY,) * 3
        import_mock = mocker.patch.object(
            fix_module_finder, "_import_module", return_value=None
        )
        fix_module_finder.include_file_as_module(
            tmp_package.path / "imports_sample.py"
        )
        import_mock.assert_has_calls(
            [
                mocker.call("moda", *any3),
                mocker.call("modb", *any3),
                mocker.call("", *any3),
                mocker.call("modd", *any3),
                mocker.call("mode", *any3),
                mocker.call("modf", *any3),
                mocker.call("modg.submod", *any3),
                mocker.call("modh", *any3),
            ]
        )

    def test_not_import_invalid_module_name(
        self, tmp_package, fix_module_finder
    ) -> None:
        """testpkg1 contains not.importable.py, which shouldn't be included."""
        tmp_package.create(INVALID_MODULE_NAME_TEST[4])
        fix_module_finder.path.insert(0, os.fspath(tmp_package.path))
        # Threw ImportError before the bug was fixed
        module = fix_module_finder.include_package("testpkg1")
        assert "invalid-identifier" in module.global_names, (
            "submodules whose names contain invalid identifiers should still "
            "be imported"
        )

    def test_invalid_syntax(self, tmp_package, fix_module_finder) -> None:
        """Invalid syntax (e.g. Py2 only code) should not break freezing."""
        tmp_package.create(SYNTAX_ERROR_TEST[4])
        fix_module_finder.path.insert(0, os.fspath(tmp_package.path))
        with pytest.raises(ImportError):
            # Threw SyntaxError before the bug was fixed
            fix_module_finder.include_module("invalid_syntax")

    def test_find_spec(self, tmp_package, fix_module_finder) -> None:
        """Sample find_spec contains broken modules."""
        tmp_package.create(FIND_SPEC_TEST[4])
        fix_module_finder.path.insert(
            0, os.fspath(tmp_package.path / "find_spec")
        )
        module = fix_module_finder.include_module("hello")
        assert "dummypackage" in module.global_names, (
            "packages that raises exceptions should still be imported"
        )
