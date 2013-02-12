try:
    from unittest import mock  # Python >= 3.3
except ImportError:
    import mock

import os.path

test_dir = os.path.dirname(__file__)

from cx_Freeze.finder import ModuleFinder

def test_ScanCode():
    mf = ModuleFinder()
    with mock.patch.object(mf, '_ImportModule') as _ImportModule_mock:
        _ImportModule_mock.return_value = None
        mf.IncludeFile(os.path.join(test_dir, 'imports_sample.py'))
        any3 = (mock.ANY,)*3
        _ImportModule_mock.assert_has_calls([mock.call('moda', *any3),
                                             mock.call('modb', *any3),
                                             mock.call('', *any3),
                                             mock.call('modd', *any3),
                                             mock.call('mode', *any3),
                                             mock.call('modf', *any3),
                                             mock.call('modg.submod', *any3),
                                            ])
    
