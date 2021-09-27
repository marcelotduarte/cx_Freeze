import os
import pytest
from cx_Freeze import ModuleFinder, ConstantsModule


class TestModuleFinder:

    @pytest.mark.skip(reason="Not Implemented!")
    def test_init_finder(self):
        pass

    @pytest.mark.skip(reason="Not Implemented!")
    def test__add_base_modules(self):
        pass

    def test_ScanCode_legacy(self, mocker, fix_test_samples_dir):
        """ This test is an adaptation of the old `test_ScanCode` nose test """
        any3 = (mocker.ANY,) * 3
        constants = ConstantsModule()
        mf = ModuleFinder(constants_module=constants)
        import_mock = mocker.patch.object(mf, "_import_module", return_value=None)
        mf.IncludeFile(os.path.join(fix_test_samples_dir, "imports_sample.py"))
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


# from unittest import mock
# import os.path
# import sys
#
# test_dir = os.path.dirname(__file__)
#
# from cx_Freeze.finder import ModuleFinder, ConstantsModule
#
# any3 = (mock.ANY,) * 3
#
#
# def test_ScanCode():
#     constants = ConstantsModule()
#     mf = ModuleFinder(constants_module=constants)
#     with mock.patch.object(mf, "_import_module") as _ImportModule_mock:
#         _ImportModule_mock.return_value = None
#         mf.IncludeFile(os.path.join(test_dir, "imports_sample.py"))
#         _ImportModule_mock.assert_has_calls(
#             [
#                 mock.call("moda", *any3),
#                 mock.call("modb", *any3),
#                 mock.call("", *any3),
#                 mock.call("modd", *any3),
#                 mock.call("mode", *any3),
#                 mock.call("modf", *any3),
#                 mock.call("modg.submod", *any3),
#                 mock.call("modh", *any3),
#             ]
#         )
#
