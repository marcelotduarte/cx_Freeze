"""Test ModuleFinder"""

from __future__ import annotations

import os
import sys

import pytest

from cx_Freeze import ConstantsModule, ModuleFinder


# pylint: disable=missing-function-docstring,unused-argument
class TestModuleFinderWithConvertedNoseTests:
    """This class provides test cases that are conversions of the old NoseTests
    in `test_finder` that predated usage of the PyTest Framework"""

    @pytest.fixture()
    def fix_module_finder(self):
        constants = ConstantsModule()
        finder = ModuleFinder(constants_module=constants)
        return finder

    def test_scan_code(self, mocker, fix_test_samples_path, fix_module_finder):
        any3 = (mocker.ANY,) * 3
        import_mock = mocker.patch.object(
            fix_module_finder, "_import_module", return_value=None
        )
        fix_module_finder.include_file_as_module(
            fix_test_samples_path / "imports_sample.py"
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
        self, mocker, fix_test_samples_dir, fix_module_finder
    ):
        """testpkg1 contains not.importable.py, which shouldn't be included."""
        fix_module_finder.path.insert(0, fix_test_samples_dir)
        # Threw ImportError before the bug was fixed
        module = fix_module_finder.include_package("testpkg1")
        assert "invalid-identifier" in module.global_names, (
            "submodules whose names contain invalid identifiers should still "
            "be imported"
        )

    def test_invalid_syntax(self, mocker, fix_test_samples_dir):
        """Invalid syntax (e.g. Py2 only code) should not break freezing."""
        constants = ConstantsModule()
        finder = ModuleFinder(
            path=[fix_test_samples_dir] + sys.path, constants_module=constants
        )
        with pytest.raises(ImportError):
            # Threw SyntaxError before the bug was fixed
            finder.include_module("invalid_syntax")

    def test_find_spec(self, mocker, fix_test_samples_path, fix_module_finder):
        """Sample find_spec contains broken modules."""
        path = fix_test_samples_path / "find_spec"
        fix_module_finder.path.insert(0, os.fspath(path))
        module = fix_module_finder.include_module("hello")
        assert (
            "dummypackage" in module.global_names
        ), "packages that raises exceptions should still be imported"
