"""Test ModuleFinder."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest
from generate_samples import (
    FIND_SPEC_TEST,
    INVALID_MODULE_NAME_TEST,
    SCAN_CODE_TEST,
    SYNTAX_ERROR_TEST,
    create_package,
)

from cx_Freeze import ConstantsModule, ModuleFinder

if TYPE_CHECKING:
    from pathlib import Path


class TestModuleFinder:
    """Provides test cases for ModuleFinder class."""

    @pytest.fixture
    def fix_module_finder(self) -> ModuleFinder:
        constants = ConstantsModule()
        return ModuleFinder(constants_module=constants)

    def test_scan_code(
        self, tmp_path: Path, fix_module_finder, mocker
    ) -> None:
        create_package(tmp_path, source=SCAN_CODE_TEST[4])
        any3 = (mocker.ANY,) * 3
        import_mock = mocker.patch.object(
            fix_module_finder, "_import_module", return_value=None
        )
        fix_module_finder.include_file_as_module(
            tmp_path / "imports_sample.py"
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
        self, tmp_path: Path, fix_module_finder
    ) -> None:
        """testpkg1 contains not.importable.py, which shouldn't be included."""
        create_package(tmp_path, source=INVALID_MODULE_NAME_TEST[4])
        fix_module_finder.path.insert(0, os.fspath(tmp_path))
        # Threw ImportError before the bug was fixed
        module = fix_module_finder.include_package("testpkg1")
        assert "invalid-identifier" in module.global_names, (
            "submodules whose names contain invalid identifiers should still "
            "be imported"
        )

    def test_invalid_syntax(self, tmp_path: Path, fix_module_finder) -> None:
        """Invalid syntax (e.g. Py2 only code) should not break freezing."""
        create_package(tmp_path, source=SYNTAX_ERROR_TEST[4])
        fix_module_finder.path.insert(0, os.fspath(tmp_path))
        with pytest.raises(ImportError):
            # Threw SyntaxError before the bug was fixed
            fix_module_finder.include_module("invalid_syntax")

    def test_find_spec(self, tmp_path: Path, fix_module_finder) -> None:
        """Sample find_spec contains broken modules."""
        create_package(tmp_path, source=FIND_SPEC_TEST[4])
        fix_module_finder.path.insert(0, os.fspath(tmp_path / "find_spec"))
        module = fix_module_finder.include_module("hello")
        assert "dummypackage" in module.global_names, (
            "packages that raises exceptions should still be imported"
        )
