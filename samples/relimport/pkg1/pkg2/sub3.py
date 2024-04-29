print("importing pkg1.pkg2.sub3")

from pkg1 import sub6  # noqa: E402,F401

from . import sub5  # noqa: E402,F401
