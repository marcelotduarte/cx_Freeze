version = "4.2.3"

import sys
from cx_Freeze.dist import *
if sys.platform == "win32" and sys.version_info[:2] >= (2, 5):
    from cx_Freeze.windist import *
from cx_Freeze.finder import *
from cx_Freeze.freezer import *
from cx_Freeze.main import *

del dist
del finder
del freezer

