"""First script that is run when cx_Freeze starts up. It determines the name of
the initscript that is to be executed after a basic initialization.
"""

from __future__ import annotations

import contextlib
import os
import string
import sys
from importlib.machinery import (
    EXTENSION_SUFFIXES,
    ExtensionFileLoader,
    ModuleSpec,
    PathFinder,
)

import BUILD_CONSTANTS

STRINGREPLACE = list(
    string.whitespace + string.punctuation.replace(".", "").replace("_", "")
)


class ExtensionFinder(PathFinder):
    """A Finder for extension modules of packages in zip files."""

    @classmethod
    def find_spec(
        cls,
        fullname,
        path=None,
        target=None,  # noqa: ARG003
    ) -> ModuleSpec | None:
        """Finder only for extension modules found within packages that
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


def get_name(executable) -> str:
    """Get the module basename to search for init and main scripts."""
    name = os.path.normcase(os.path.basename(executable))
    if sys.platform.startswith("win"):
        name, _ = os.path.splitext(name)
    name = name.partition(".")[0]
    if not name.isidentifier():
        for char in STRINGREPLACE:
            name = name.replace(char, "_")
    return name


def init() -> None:
    """Basic initialization of the startup script."""
    # to avoid bugs (especially in MSYS2) use normpath after any change
    sys.executable = os.path.normpath(sys.executable)
    sys.frozen_dir = frozen_dir = os.path.dirname(sys.executable)
    sys.meta_path.append(ExtensionFinder)

    # normalize and check sys.path, preserving the reference
    j = 0
    for path in list(map(os.path.normpath, sys.path)):
        if os.path.exists(path):
            sys.path[j] = path
            j = j + 1
        else:
            sys.path.remove(path)

    if sys.platform.startswith("win"):
        # the search path for dependencies
        search_path: list[str] = [
            entry for entry in sys.path if os.path.isdir(entry)
        ]
        # add to dll search path (or to path)
        env_path = os.environ.get("PATH", "").split(os.pathsep)
        env_path = list(map(os.path.normpath, env_path))
        for directory in search_path:
            with contextlib.suppress(OSError):
                os.add_dll_directory(directory)
            # we need to add to path for packages like 'gi' in MSYS2
            if directory not in env_path:
                env_path.insert(0, directory)
        env_path = [entry.replace(os.sep, "\\") for entry in env_path]
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
            var_path = os.path.join(frozen_dir, os.path.normpath(value))
            if not os.path.exists(var_path) and sys.platform == "darwin":
                # when using bdist_mac
                var_path = os.path.join(
                    os.path.dirname(frozen_dir),
                    "Resources",
                    os.path.normpath(value),
                )
            os.environ[name] = var_path


def run() -> None:
    """Determines the name of the initscript and execute it."""
    name = get_name(sys.executable)
    try:
        # basically, the basename of the executable plus __init__
        module_init = __import__(name + "__init__")
    except ModuleNotFoundError:
        # but can be renamed when only one executable exists
        num = BUILD_CONSTANTS._EXECUTABLES_NUMBER  # noqa: SLF001
        if num > 1:
            msg = (
                "Apparently, the original executable has been renamed to "
                f"{name!r}. When multiple executables are generated, "
                "renaming is not allowed."
            )
            raise RuntimeError(msg) from None
        name = get_name(BUILD_CONSTANTS._EXECUTABLE_NAME_0)  # noqa: SLF001
        module_init = __import__(name + "__init__")
    module_init.run(name + "__main__")
