import os
import sys
import pytest
from cx_Freeze import ModuleFinder, ConstantsModule


class TestModuleFinder:

    @pytest.mark.skip(reason="Not Implemented!")
    def test_init_finder(self):
        pass

    @pytest.mark.skip(reason="Not Implemented!")
    def test__add_base_modules(self):
        pass


class TestModuleFinderWithConvertedNoseTests:
    """ This class provides test cases that are conversions of the old NoseTests
    that predated usage of the PyTest Framework"""

    @pytest.fixture()
    def fix_module_finder(self):
        constants = ConstantsModule()
        mf = ModuleFinder(constants_module=constants)
        return mf

    def test_ScanCode(self, mocker, fix_test_samples_dir, fix_module_finder):
        any3 = (mocker.ANY,) * 3
        import_mock = mocker.patch.object(fix_module_finder, "_import_module", return_value=None)
        fix_module_finder.IncludeFile(os.path.join(fix_test_samples_dir, "imports_sample.py"))
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

    def test_not_import_invalid_module_name(self, mocker, fix_test_samples_dir, fix_module_finder):
        """ testpkg1 contains not.importable.py, which shouldn't be included."""
        fix_module_finder.path.insert(0, fix_test_samples_dir)
        module = fix_module_finder.IncludePackage(
            "testpkg1"
        )  # Threw ImportError before the bug was fixed
        assert ("invalid-identifier" in module.global_names), \
            "submodules whose names contain invalid identifiers should still be imported"

    def test_invalid_syntax(self, mocker, fix_test_samples_dir):
        """Invalid syntax (e.g. Py2 or Py3 only code) should not break freezing."""
        constants = ConstantsModule()
        mf = ModuleFinder(path=[fix_test_samples_dir] + sys.path, constants_module=constants)
        with pytest.raises(ImportError):
            mf.IncludeModule(
                "invalid_syntax"
            )  # Threw SyntaxError before the bug was fixed
