#------------------------------------------------------------------------------
# Console.py
#   Initialization script for cx_Freeze. Sets the attribute sys.frozen so that
# modules that expect it behave as they should.
#------------------------------------------------------------------------------

import os
import sys

sys.frozen = True

FILE_NAME = sys.executable
DIR_NAME = os.path.dirname(sys.executable)

os.environ["TCL_LIBRARY"] = os.path.join(DIR_NAME, "tcl")
os.environ["TK_LIBRARY"] = os.path.join(DIR_NAME, "tk")

m = __import__("__main__")
name, ext = os.path.splitext(os.path.basename(os.path.normcase(FILE_NAME)))
moduleName = "%s__main__" % name
scriptModule = __import__(moduleName)
m.__dict__.update(scriptModule.__dict__)

versionInfo = sys.version_info[:3]
if versionInfo >= (2, 5, 0) and versionInfo <= (2, 6, 4):
    module = sys.modules.get("threading")
    if module is not None:
        module._shutdown()

