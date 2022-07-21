"""sample to show GetDependentFiles in action - for Windows only"""

# This sample is a piece of code extracted from the freeze module,
# in order to demonstrate the dependencies of the specified file.
#
# Usage:
#   python getdependentfiles.py FILE
# Where FILE is a .exe, .pyd or .dll file
#
# See also: test_1.py - a batch of tests

import os
import sys

try:
    import cx_Freeze.util
except ImportError:
    print("Please install a cx-freeze package to test", file=sys.stderr)
    sys.exit(-1)


def print_usage():
    print("cx_Freeze dependencies demo (for windows only)", file=sys.stderr)
    print("usage:\n\t%s FILE..." % sys.argv[0], file=sys.stderr)
    return -1


def main():
    if len(sys.argv) <= 1:
        return print_usage()
    if sys.platform != "win32":
        print(sys.argv[0] + " is only for windows", file=sys.stderr)
        return -1
    res = 0
    for i in range(1, len(sys.argv)):
        path = sys.argv[i]
        print(path)
        try:
            dependent_files = cx_Freeze.util.GetDependentFiles(path)
        except cx_Freeze.util.BindError as exc:
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
