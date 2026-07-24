"""sample to show GetDependentFiles in action - for Windows only."""

# This sample is a piece of code extracted from the freeze module,
# in order to demonstrate the dependencies of the specified file.
#
# Usage:
#   python getdependentfiles.py FILE
# Where FILE is a .exe, .pyd or .dll file
#
# See also: test_1.py - a batch of tests

from __future__ import annotations

import os
import sys

try:
    import freeze_core.util
except ImportError:
    print("Please install 'freeze-core' package to test", file=sys.stderr)
    sys.exit(-1)


def print_usage() -> int:
    print("cx_Freeze dependencies demo (for windows only)", file=sys.stderr)
    print(f"usage:\n\t{sys.argv[0]} FILE...", file=sys.stderr)
    return -1


def main() -> int:
    if len(sys.argv) <= 1:
        return print_usage()
    if sys.platform != "win32":
        print(sys.argv[0] + " is only for windows", file=sys.stderr)
        return -1
    path = None
    start = 1
    if sys.argv[1] == "--path":
        paths = sys.argv[2]
        print("--path", paths)
        start = 3
        os.environ["PATH"] = paths + os.pathsep + os.environ["PATH"]
    elif sys.argv[1] == "--dllpath":
        paths = sys.argv[2]
        start = 3
        print("--dllpath", paths)
        os.add_dll_directory(paths)
    res = 0
    for i in range(start, len(sys.argv)):
        path = sys.argv[i]
        print(path)
        try:
            dependent_files = freeze_core.util.GetDependentFiles(path)
        except freeze_core.util.BindError as exc:
            dependent_files = []
            print("error during GetDependentFiles() of ")
            print(f"{path!r}: {exc!s}", file=sys.stderr)
            res = -1
        if dependent_files:
            for file_name in dependent_files:
                print("\t", os.path.basename(file_name), "=>", file_name)
        else:
            print("\t(dependency not found)")
    return res


if __name__ == "__main__":
    sys.exit(main())
