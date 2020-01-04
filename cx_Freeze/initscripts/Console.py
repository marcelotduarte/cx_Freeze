#------------------------------------------------------------------------------
# Console.py
#   Initialization script for cx_Freeze. Sets the attribute sys.frozen so that
# modules that expect it behave as they should.
#------------------------------------------------------------------------------

import os
import sys

import BUILD_CONSTANTS

sys.frozen = True

FILE_NAME = sys.executable
DIR_NAME = os.path.dirname(sys.executable)

if hasattr(BUILD_CONSTANTS, "TCL_LIBRARY"):
    os.environ["TCL_LIBRARY"] = os.path.join(DIR_NAME,
                                             BUILD_CONSTANTS.TCL_LIBRARY)

if hasattr(BUILD_CONSTANTS, "TK_LIBRARY"):
    os.environ["TK_LIBRARY"] = os.path.join(DIR_NAME,
                                             BUILD_CONSTANTS.TK_LIBRARY)

if hasattr(BUILD_CONSTANTS, "MATPLOTLIBDATA"):
    os.environ["MATPLOTLIBDATA"] = os.path.join(DIR_NAME,
                                             BUILD_CONSTANTS.MATPLOTLIBDATA)

if hasattr(BUILD_CONSTANTS, "PYTZ_TZDATADIR"):
    os.environ["PYTZ_TZDATADIR"] = os.path.join(DIR_NAME,
                                                BUILD_CONSTANTS.PYTZ_TZDATADIR)

def run():
    name, ext = os.path.splitext(os.path.basename(os.path.normcase(FILE_NAME)))
    moduleName = "%s__main__" % name
    code = __loader__.get_code(moduleName)
    exec(code, {'__name__': '__main__'})
