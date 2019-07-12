#------------------------------------------------------------------------------
# __startup__.py
#   This is the first script that is run when cx_Freeze starts up. It simply
# determines the name of the initscript that is to be executed.
#------------------------------------------------------------------------------

import os
import sys
from importlib.machinery import ExtensionFileLoader, EXTENSION_SUFFIXES, PathFinder
from importlib.util import spec_from_file_location


class ExtensionFinder(PathFinder):

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        print('ExtensionFinder.find_spec', fullname, path, target)
        for path in sys.path:
            for ext in EXTENSION_SUFFIXES:
                location = os.path.join(path, fullname + ext)
                if os.path.isfile(location):
                    loader = ExtensionFileLoader(fullname, location)
                    spec = spec_from_file_location(fullname, location,
                                                   loader=loader)
                    if spec:
                        return spec

sys.meta_path.append(ExtensionFinder)


def run():
    baseName = os.path.normcase(os.path.basename(sys.executable))
    name, ext = os.path.splitext(baseName)
    module = __import__(name + "__init__")
    module.run()
