#------------------------------------------------------------------------------
# Console.py
#   Initialization script for cx_Freeze which manipulates the path so that the
# directory in which the executable is found is searched for extensions but
# no other directory is searched. It also sets the attribute sys.frozen so that
# the Win32 extensions behave as expected.
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

sys.frozen = True
sys.path = [fileName, dirName]

m = __import__("__main__")
importer = zipimport.zipimporter(fileName)
code = importer.get_code(m.__name__)
exec code in m.__dict__

