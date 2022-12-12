"""
This is the first script that is run when cx_Freeze starts up. It
determines the name of the initscript that is to be executed after
a basic initialization.
"""

from __future__ import annotations

import os
import string
import sys
from importlib.machinery import (
    EXTENSION_SUFFIXES,
    ExtensionFileLoader,
    ModuleSpec,
    PathFinder,
)
from sysconfig import get_platform

import BUILD_CONSTANTS

STRINGREPLACE = list(
    string.whitespace + string.punctuation.replace(".", "").replace("_", "")
)
IS_MINGW = get_platform().startswith("mingw")
IS_WINDOWS = get_platform().startswith("win")


class ExtensionFinder(PathFinder):
    """A Finder for extension modules of packages in zip files."""

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


def init():
    """Basic initialization of the startup script."""

    # update sys module
    sys.executable = os.path.normpath(sys.executable)
    sys.frozen_dir = frozen_dir = os.path.dirname(sys.executable)
    sys.meta_path.append(ExtensionFinder)

    if IS_MINGW:
        sys.path = [os.path.normpath(entry) for entry in sys.path]
    if IS_WINDOWS or IS_MINGW:
        # for python >= 3.8, the search for dlls is sandboxed
        search_path: list[str] = [
            entry for entry in sys.path if os.path.isdir(entry)
        ]
        add_to_path = os.path.join(frozen_dir, "lib")
        if add_to_path not in search_path:
            search_path.insert(0, add_to_path)
        # add numpy+mkl to the PATH
        if hasattr(BUILD_CONSTANTS, "MKL_PATH"):
            add_to_path = os.path.join(frozen_dir, BUILD_CONSTANTS.MKL_PATH)
            search_path.append(os.path.normpath(add_to_path))
        # add to dll search path (or to path)
        env_path = os.environ["PATH"].split(os.pathsep)
        if IS_MINGW:
            env_path = [os.path.normpath(entry) for entry in env_path]
        for directory in search_path:
            try:
                os.add_dll_directory(directory)
            except OSError:
                pass
            except AttributeError:
                # add to path only when python < 3.8
                if directory not in env_path:
                    env_path.insert(0, directory)
        if IS_MINGW:
            env_path = [entry.replace(os.sep, os.altsep) for entry in env_path]
        os.environ["PATH"] = os.pathsep.join(env_path)

    # set environment variables
    for name in (
        "TCL_LIBRARY",
        "TK_LIBRARY",
        "PYTZ_TZDATADIR",
        "PYTHONTZPATH",
    ):
        try:
            value = getattr(BUILD_CONSTANTS, name)
        except AttributeError:
            pass
        else:
            os.environ[name] = os.path.join(frozen_dir, value)


def run():
    """Determines the name of the initscript and execute it."""

    # get the real name of __init__ script
    # basically, the basename of executable plus __init__
    # but can be renamed when only one executable exists
    name = os.path.normcase(os.path.basename(sys.executable))
    if IS_WINDOWS or IS_MINGW:
        name, _ = os.path.splitext(name)
    name = name.partition(".")[0]
    if not name.isidentifier():
        for char in STRINGREPLACE:
            name = name.replace(char, "_")
    try:
        module_init = __import__(name + "__init__")
    except ModuleNotFoundError:
        files = []
        for k in __loader__._files:  # pylint: disable=W0212
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
        module_init = __import__(name + "__init__")
    module_init.run(name + "__main__")
