#------------------------------------------------------------------------------
# ConsoleSetLibPath.py
#   Initialization script for cx_Freeze which manipulates the path so that the
# directory in which the executable is found is searched for extensions but
# no other directory is searched. The environment variable LD_LIBRARY_PATH is
# manipulated first, however, to ensure that shared libraries found in the
# target directory are found. This requires a restart of the executable because
# the environment variable LD_LIBRARY_PATH is only checked at startup.
#------------------------------------------------------------------------------

import encodings
import os
import sys
import warnings
import zipimport

fileName = sys.path[0]
while os.path.islink(fileName):
    fileName = os.path.normpath(os.path.join(os.path.dirname(fileName),
            os.readlink(fileName)))
dirName = os.path.dirname(fileName)

paths = os.environ.get("LD_LIBRARY_PATH", "").split(os.pathsep)
if dirName not in paths:
    paths.insert(0, dirName)
    os.environ["LD_LIBRARY_PATH"] = os.pathsep.join(paths)
    os.execv(sys.executable, sys.argv)

sys.frozen = True
sys.path = [fileName, dirName]

m = __import__("__main__")
importer = zipimport.zipimporter(fileName)
code = importer.get_code(m.__name__)
exec code in m.__dict__

