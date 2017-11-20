version = "5.1.1"
__version__ = version

import sys
from cx_Freeze.dist import *
if sys.platform == "win32":
    from cx_Freeze.windist import *
elif sys.platform == "darwin":
    from cx_Freeze.macdist import *
from cx_Freeze.finder import *
from cx_Freeze.freezer import *
from cx_Freeze.main import *

del dist
del finder
del freezer

