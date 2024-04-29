print("importing pkg1.pkg2")

from pkg1 import sub4  # noqa: E402,F401

from . import sub3  # noqa: E402,F401
