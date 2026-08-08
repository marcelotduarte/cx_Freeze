"""Use getdependentfiles.py in a batch of tests."""

# This sample uses the getdependentfiles.py script to try to get the
# dependents of some predetermined files.

from __future__ import annotations

import glob
import os
import sys

try:
    import cx_Freeze
except ImportError:
    cx_Freeze = None


def main() -> int | None:
    if sys.platform != "win32":
        print(sys.argv[0] + " is only for windows", file=sys.stderr)
        return -1
    if cx_Freeze is None:
        print("Please install a cx-freeze package to test", file=sys.stderr)
        return -1

    fname = os.path.join(os.path.dirname(sys.argv[0]), "getdependentfiles.py")
    command = [sys.executable, fname]
    dlls = os.path.join(sys.base_prefix, "DLLs")
    scripts = os.path.join(sys.base_prefix, "Scripts")
    module_dir = os.path.dirname(cx_Freeze.__file__)

    dependencies_to_check = [
        os.path.join(sys.base_prefix, os.path.basename(sys.executable)),
        os.path.join(
            sys.base_prefix,
            f"python{sys.version_info[0]}{sys.version_info[1]}.dll",
        ),
        sys.executable,
        os.path.join(dlls, "_ctypes.pyd"),
        os.path.join(dlls, "_sqlite3.pyd"),
        os.path.join(dlls, "_ssl.pyd"),
        os.path.join(scripts, "pip.exe"),
    ]
    dependencies_to_check.extend(
        list(glob.glob(os.path.join(module_dir, "bases", "console*.exe")))
    )

    print("testing with default PATH environ")
    cmdline = " ".join(command + dependencies_to_check)
    print(cmdline)
    for line in os.popen(cmdline):  # noqa: S605
        print(line, end="")
    print()

    print("testing with sys.path into PATH environ")
    syspath = ["--path", os.pathsep.join(sys.path)]
    cmdline = " ".join(command + syspath + dependencies_to_check)
    print(cmdline)
    for line in os.popen(cmdline):  # noqa: S605
        print(line, end="")
    print()

    print("testing with os.add_dll_directory")
    dllpath = ["--dllpath", dlls]
    cmdline = " ".join(command + dllpath + dependencies_to_check)
    print(cmdline)
    for line in os.popen(cmdline):  # noqa: S605
        print(line, end="")
    print()
    return None


if __name__ == "__main__":
    sys.exit(main())
