#------------------------------------------------------------------------------
# ConsoleKeepPath.py
#   Initialization script for cx_Freeze which leaves the path alone and does
# not set the sys.frozen attribute.
#------------------------------------------------------------------------------

import sys
import zipimport

fileName = sys.path[0]

m = __import__("__main__")
importer = zipimport.zipimporter(fileName)
code = importer.get_code(m.__name__)
exec code in m.__dict__

