"""
Initialization script for cx_Freeze. Sets the attribute sys.frozen so that
modules that expect it behave as they should.
"""

import os
import sys

import BUILD_CONSTANTS

sys.frozen = True

DIR_NAME = os.path.dirname(sys.executable)

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
