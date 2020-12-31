"""
Initialization script for cx_Freeze which imports the site module (as per
normal processing of a Python script) and then searches for a file with the
same name as the shared library but with the extension .pth. The entries in
this file are used to modify the path to use for subsequent imports.
"""

import os
import sys
import warnings

# the site module must be imported for normal behavior to take place; it is
# done dynamically so that cx_Freeze will not add all modules referenced by
# the site module to the frozen executable
__import__("site")

# now locate the pth file to modify the path appropriately
baseName, ext = os.path.splitext(FILE_NAME)  # noqa: F821
pathFileName = baseName + ".pth"
with open(pathFileName) as in_file:
    sys.path = [s.strip() for s in in_file.read().splitlines()] + sys.path


def run():
    pass
