"""
This is the first script that is run when cx_Freeze starts up. It simply
determines the name of the initscript that is to be executed.
"""

import os
import string
import sys
from importlib.machinery import (
    EXTENSION_SUFFIXES,
    ExtensionFileLoader,
    ModuleSpec,
    PathFinder,
)

STRINGREPLACE = list(
    string.whitespace + string.punctuation.replace(".", "").replace("_", "")
)


class ExtensionFinder(PathFinder):
    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        """
        This finder is only for extension modules found within packages that
        are included in the zip file (instead of as files on disk);
        extension modules cannot be found within zip files but are stored in
        the lib subdirectory; if the extension module is found in a package,
        however, its name has been altered so this finder is needed.
        """
        if path is None:
            return None
        suffixes = EXTENSION_SUFFIXES
        for entry in sys.path:
            if ".zip" in entry:
                continue
            for ext in suffixes:
                location = os.path.join(entry, fullname + ext)
                if os.path.isfile(location):
                    loader = ExtensionFileLoader(fullname, location)
                    return ModuleSpec(fullname, loader, origin=location)
        return None


sys.meta_path.append(ExtensionFinder)


def run():
    # fix PATH for anaconda/miniconda
    if sys.platform == "win32":
        add_to_path = os.path.join(os.path.dirname(sys.executable), "lib")
        os.environ["PATH"] = add_to_path + ";" + os.environ["PATH"]
    # get the real name of __init__ script
    # basically, the basename of executable plus __init__
    # but can be renamed when only one executable exists
    name = os.path.basename(sys.executable)
    if sys.platform == "win32":
        name, _ = os.path.splitext(name)
    name = name.partition(".")[0]
    if not name.isidentifier():
        for ch in STRINGREPLACE:
            name = name.replace(ch, "_")
    name = os.path.normcase(name)
    try:
        module = __import__(name + "__init__")
    except ModuleNotFoundError:
        files = []
        for k in __loader__._files:
            if k.endswith("__init__.pyc"):
                k = k.rpartition("__init__")[0]
                if k.isidentifier():
                    files.append(k)
        if len(files) != 1:
            raise RuntimeError(
                "Apparently, the original executable has been renamed to "
                f"{name!r}. When multiple executables are generated, "
                "renaming is not allowed."
            ) from None
        name = files[0]
        module = __import__(name + "__init__")
    module.run()
