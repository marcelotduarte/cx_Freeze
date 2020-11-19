"""
Initialization script for cx_Freeze which manipulates the path so that the
directory in which the executable is found is searched for extensions but
no other directory is searched. The environment variable LD_LIBRARY_PATH is
manipulated first, however, to ensure that shared libraries found in the
target directory are found. This requires a restart of the executable because
the environment variable LD_LIBRARY_PATH is only checked at startup.

"""

import os
import sys

import BUILD_CONSTANTS

DIR_NAME = os.path.dirname(sys.executable)

paths = os.environ.get("LD_LIBRARY_PATH", "").split(os.pathsep)

if DIR_NAME not in paths:
    paths.insert(0, DIR_NAME)
    os.environ["LD_LIBRARY_PATH"] = os.pathsep.join(paths)
    os.execv(sys.executable, sys.argv)

sys.frozen = True
sys.path = sys.path[:4]

if hasattr(BUILD_CONSTANTS, "TCL_LIBRARY"):
    os.environ["TCL_LIBRARY"] = os.path.join(
        DIR_NAME, BUILD_CONSTANTS.TCL_LIBRARY
    )

if hasattr(BUILD_CONSTANTS, "TK_LIBRARY"):
    os.environ["TK_LIBRARY"] = os.path.join(
        DIR_NAME, BUILD_CONSTANTS.TK_LIBRARY
    )

if hasattr(BUILD_CONSTANTS, "PYTZ_TZDATADIR"):
    os.environ["PYTZ_TZDATADIR"] = os.path.join(
        DIR_NAME, BUILD_CONSTANTS.PYTZ_TZDATADIR
    )


def run():
    name = __name__.rpartition("__init__")[0] + "__main__"
    code = __loader__.get_code(name)
    m = __import__("__main__")
    m.__dict__["__file__"] = code.co_filename
    exec(code, m.__dict__)
