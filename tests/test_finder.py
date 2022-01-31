import os
import shutil
import sys
import zipfile

import pytest

from cx_Freeze import ConstantsModule, Module, ModuleFinder


class TestModuleFinderWithConvertedNoseTests:
    """This class provides test cases that are conversions of the old NoseTests
    in `test_finder` that predated usage of the PyTest Framework"""

    @pytest.fixture()
    def fix_module_finder(self):
        constants = ConstantsModule()
        mf = ModuleFinder(constants_module=constants)
        return mf

    def test_ScanCode(self, mocker, fix_test_samples_dir, fix_module_finder):
        any3 = (mocker.ANY,) * 3
        import_mock = mocker.patch.object(
            fix_module_finder, "_import_module", return_value=None
        )
        fix_module_finder.IncludeFile(
            os.path.join(fix_test_samples_dir, "imports_sample.py")
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
        module = fix_module_finder.IncludePackage(
            "testpkg1"
        )  # Threw ImportError before the bug was fixed
        assert (
            "invalid-identifier" in module.global_names
        ), "submodules whose names contain invalid identifiers should still be imported"

    def test_invalid_syntax(self, mocker, fix_test_samples_dir):
        """Invalid syntax (e.g. Py2 or Py3 only code) should not break freezing."""
        constants = ConstantsModule()
        mf = ModuleFinder(
            path=[fix_test_samples_dir] + sys.path, constants_module=constants
        )
        with pytest.raises(ImportError):
            mf.IncludeModule(
                "invalid_syntax"
            )  # Threw SyntaxError before the bug was fixed

    @pytest.mark.skip(
        "Test skipped, uncertain if no longer supported - waiting for maintainer to comment on:"
        "https://github.com/marcelotduarte/cx_Freeze/pull/1234"
    )
    def test_FindModule_from_zip(
        self, fix_module_finder, fix_samples_dir, tmpdir
    ):
        # -----------------
        # Helper Methods from `test_zip_packages`
        def clean_pyc_files():
            for dirpath, dirnames, filenames in os.walk(fix_samples_dir):
                for filename in filenames:
                    if filename.endswith((".pyc", ".pyo")):
                        os.unlink(os.path.join(dirpath, filename))
                if "__pycache__" in dirnames:
                    dirnames.remove("__pycache__")
                    shutil.rmtree(os.path.join(dirpath, "__pycache__"))

        def prepare_zip_file():
            clean_pyc_files()
            tmpd = tmpdir.mkdir()
            egg = os.path.join(tmpd, "testpkg1.egg")
            eggzip = zipfile.PyZipFile(egg, "w", zipfile.ZIP_DEFLATED)
            eggzip.writepy(os.path.join(fix_samples_dir, "testmod1.py"))
            eggzip.writepy(os.path.join(fix_samples_dir, "testpkg1"))
            eggzip.close()
            return egg

        # End Helper Methods
        # -----------------

        # Original test
        egg = prepare_zip_file()
        try:
            fix_module_finder.path = [egg]
            mod = fix_module_finder._internal_import_module(
                "testpkg1.submod", deferred_imports=[]
            )
            assert isinstance(mod, Module)
        finally:
            os.unlink(egg)
