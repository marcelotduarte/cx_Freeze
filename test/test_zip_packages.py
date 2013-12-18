import imp
import os
import tempfile
import zipfile

test_dir = os.path.dirname(__file__)

from cx_Freeze.finder import ZipModulesCache

def prepare_zip_file():
    tmpd = tempfile.mkdtemp()
    egg = os.path.join(tmpd, 'testpkg1.egg')
    eggzip = zipfile.PyZipFile(egg, 'w', zipfile.ZIP_DEFLATED)
    eggzip.writepy(os.path.join(test_dir, 'samples', 'testmod1.py'))
    eggzip.writepy(os.path.join(test_dir, 'samples', 'testpkg1'))
    eggzip.close()
    return egg

def test_ZipModulesCache():
    egg = prepare_zip_file()
    try:
        zmc = ZipModulesCache()
        
        mod = zmc.find(egg, 'testmod1')
        assert mod is not None
        assert mod[2][2] == imp.PY_COMPILED
        
        pkg = zmc.find(egg, 'testpkg1')
        assert pkg is not None
        assert pkg[2][2] == imp.PKG_DIRECTORY
        
        # This needs to be called after zmc.find(egg, *)
        submod = zmc.find(os.path.join(egg, 'testpkg1'), 'submod')
        assert submod is not None
        assert submod[2][2] == imp.PY_COMPILED
    finally:
        os.unlink(egg)