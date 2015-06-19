try:
    from unittest import mock  # Python >= 3.3
except ImportError:
    import mock

import imp
import os.path
import sys

test_dir = os.path.dirname(__file__)

from cx_Freeze.finder import ModuleFinder

any3 = (mock.ANY,)*3

def test_ScanCode():
    mf = ModuleFinder()
    with mock.patch.object(mf, '_ImportModule') as _ImportModule_mock:
        _ImportModule_mock.return_value = None
        mf.IncludeFile(os.path.join(test_dir, 'imports_sample.py'))
        _ImportModule_mock.assert_has_calls([mock.call('moda', *any3),
                                             mock.call('modb', *any3),
                                             mock.call('', *any3),
                                             mock.call('modd', *any3),
                                             mock.call('mode', *any3),
                                             mock.call('modf', *any3),
                                             mock.call('modg.submod', *any3),
                                             mock.call('modh', *any3),
                                            ])

def test_not_import_invalid_module_name():
    """testpkg1 contains not.importable.py, which shouldn't be included."""
    mf = ModuleFinder()
    mf.path.insert(0, os.path.join(test_dir, 'samples'))

    try:
        module = mf.IncludePackage('testpkg1')  # Threw ImportError before the bug was fixed
    except ImportError:
        assert False, "submodules with names containing '.' should not be included"

    assert 'invalid-identifier' in module.globalNames, \
            'submodules that contain invalid identifiers should still be imported'
        
def test_suffixes_attempted_in_correct_order():
    with mock.patch('imp.get_suffixes') as get_suffixes:
        get_suffixes.return_value = [('.so', 'r', imp.C_EXTENSION),
                                     ('.platform.so', 'r', imp.C_EXTENSION)]

        mf = ModuleFinder()

        real_iim = mf._InternalImportModule
        def iim(name, *args, **kwargs):
            if name == 'testpkg2.some_module':
                return mock.MagicMock()
            else:
                return real_iim(name, *args, **kwargs)

        with mock.patch.object(mf, "_InternalImportModule") as _InternalImportModule:
            _InternalImportModule.side_effect = iim

            mf.path.insert(0, os.path.join(test_dir, 'samples'))

            module = mf.IncludePackage('testpkg2')  # Threw ImportError before the bug was fixed
            assert 'some_module' in module.globalNames, \
                    "some_module.platform.so should be imported as 'some_module'"

def test_invalid_syntax():
    """Invalid syntax (e.g. Py2 or Py3 only code) should not break freezing."""
    mf = ModuleFinder(path=[os.path.join(test_dir, 'samples')]+sys.path)
    try:
        mf.IncludeModule('invalid_syntax')  # Threw SyntaxError before the bug was fixed
    except ImportError:
        pass
    else:
        assert False, "Expected ImportError, but no error was raised"
