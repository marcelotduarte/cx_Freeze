import sys

from dist import *
if sys.platform == "win32":
    from windist import *
from finder import *
from freezer import *
from main import *

del dist
del finder
del freezer

