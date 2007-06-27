#------------------------------------------------------------------------------
# SharedLib.py
#   Initialization script for cx_Freeze which behaves similarly to the one for
# console based applications but must handle the case where Python has already
# been initialized and another DLL of this kind has been loaded. As such it
# does not totally block the path unless sys.frozen is not already set.
#------------------------------------------------------------------------------

import encodings
import os
import sys
import warnings

fileName = sys.path[0]
dirName = os.path.dirname(fileName)

if hasattr(sys, "frozen"):
    sys.path.append(dirName)
else:
    sys.frozen = True
    sys.path = [fileName, dirName]

