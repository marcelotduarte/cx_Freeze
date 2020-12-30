"""
This is the first script that is run when cx_Freeze starts up. It simply
determines the name of the initscript that is to be executed.
"""

import os
import sys
import importlib.machinery
import importlib.util


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
            if ".zip" in entry:
                continue
            for ext in suffixes:
                location = os.path.join(entry, fullname + ext)
                if os.path.isfile(location):
                    loader = loaderClass(fullname, location)
                    return importlib.util.spec_from_loader(fullname, loader)


sys.meta_path.append(ExtensionFinder)


def run():
    name = os.path.basename(sys.executable)
    if sys.platform == "win32":
        name, _ = os.path.splitext(name)
    name = os.path.normcase(name).replace(" ", "_")
    name = name.partition("-")[0]
    name = name.partition(".")[0]
    try:
        module = __import__(name + "__init__")
    except ModuleNotFoundError:
        files = [k for k in __loader__._files if k.endswith("__init__.pyc")]
        if len(files) != 1:
            raise RuntimeError(
                "Apparently the original executable has been renamed to "
                f"'{name}'. When multiple executables are generated, "
                "renaming is not allowed."
            ) from None
        name = files[0].rpartition("__init__")[0]
        module = __import__(name + "__init__")
    module.run()
