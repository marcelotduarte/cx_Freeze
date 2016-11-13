#------------------------------------------------------------------------------
# __startup__.py
#   This is the first script that is run when cx_Freeze starts up. It simply
# determines the name of the initscript that is to be executed.
#------------------------------------------------------------------------------

import os
import sys

baseName = os.path.normcase(os.path.basename(sys.executable))
name, ext = os.path.splitext(baseName)
__import__(name + "__init__")

