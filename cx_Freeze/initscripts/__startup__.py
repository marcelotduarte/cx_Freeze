#------------------------------------------------------------------------------
# __startup__.py
#   This is the first script that is run when cx_Freeze starts up. It simply
# determines the name of the initscript that is to be executed.
#------------------------------------------------------------------------------

import os
import sys
import importlib.machinery
import importlib.util
from importlib import _bootstrap_external
import zipimport

class ExtensionFinder(importlib.machinery.PathFinder):

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        """This finder is only for extension modules found within packages that
           are included in the zip file (instead of as files on disk);
           extension modules cannot be found within zip files but are stored in
           the lib subdirectory; if the extension module is found in a package,
           however, its name has been altered so this finder is needed."""
        if path is None:
            return
        suffixes = importlib.machinery.EXTENSION_SUFFIXES
        loaderClass = importlib.machinery.ExtensionFileLoader
        for entry in sys.path:
            if '.zip' in entry:
                continue
            for ext in suffixes:
                location = os.path.join(entry, fullname + ext)
                if os.path.isfile(location):
                    loader = loaderClass(fullname, location)
                    return importlib.util.spec_from_loader(fullname, loader)

sys.meta_path.append(ExtensionFinder)

#adapted from https://github.com/python/cpython/pull/6809
path_sep = _bootstrap_external.path_sep
_module_type = type(sys)


class ZipImporter(zipimport.zipimporter):

    def load_module(self, fullname):
        code, ispackage, modpath = _get_module_code(self, fullname)
        mod = sys.modules.get(fullname)
        if mod is None or not isinstance(mod, _module_type):
            mod = _module_type(fullname)
            sys.modules[fullname] = mod
        mod.__loader__ = self

        try:
            path = _get_module_path(self, fullname)
            if ispackage:
                # add __path__ to the module *before* the code gets executed
                fullpath = _bootstrap_external._path_join(self.archive, path)
                mod.__path__ = [fullpath]
                package = path.replace(path_sep, ".")
            else:
                package = path.replace(path_sep, ".").rpartition('.')[0]
            mod.__package__ = package

            if not hasattr(mod, '__builtins__'):
                mod.__builtins__ = __builtins__
            _bootstrap_external._fix_up_module(mod.__dict__, fullname, modpath)
            exec(code, mod.__dict__)
        except:
            del sys.modules[fullname]
            raise

        try:
            mod = sys.modules[fullname]
        except KeyError:
            raise ImportError('Loaded module %r not found in sys.modules' % fullname)
        return mod

    def __repr__(self):
        return '<ZipImporter object "%s%s%s">' % (self.archive, path_sep, self.prefix)

# _zip_searchorder defines how we search for a module in the Zip
# archive: we first search for a package __init__, then for
# non-package .pyc, and .py entries. The .pyc entries
# are swapped by initzipimport() if we run in optimized mode. Also,
# '/' is replaced by path_sep there.
_zip_searchorder = (
    (path_sep + '__init__.pyc', True, True),
    (path_sep + '__init__.py', False, True),
    ('.pyc', True, False),
    ('.py', False, False),
)

# Given a module name, return the potential file path in the
# archive (without extension).
def _get_module_path(self, fullname):
    return self.prefix + fullname.rpartition('.')[2]

# Given a string buffer containing Python source code, compile it
# and return a code object.
def _compile_source(pathname, source):
    source = importlib.util.decode_source(source)
    return compile(source, pathname, 'exec', dont_inherit=True)

# Get the code object associated with the module specified by 'fullname'.
def _get_module_code(self, fullname):
    path = _get_module_path(self, fullname)
    for suffix, isbytecode, ispackage in _zip_searchorder:
        fullpath = path + suffix
        #_bootstrap._verbose_message('trying {}{}{}', self.archive, path_sep, fullpath, verbosity=2)
        try:
            toc_entry = self._files[fullpath]
        except KeyError:
            pass
        else:
            modpath = toc_entry[0]
            if isbytecode:
                code = self.get_code(fullname)
            else:
                data = self.get_data(fullname)
                code = _compile_source(modpath, data)
            if code is None:
                # bad magic number or non-matching mtime in byte code, try next
                continue
            modpath = toc_entry[0]
            return code, ispackage, modpath
    else:
        raise zipimport.ZipImportError("can't find module %r" % fullname)

sys.path_hooks[0] = ZipImporter


def run():
    baseName = os.path.normcase(os.path.basename(sys.executable))
    name, ext = os.path.splitext(baseName)
    module = __import__(name + "__init__")
    module.run()
