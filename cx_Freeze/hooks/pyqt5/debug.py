"""Module used to inject a debug code to show QLibraryInfo paths if environment
variable QT_DEBUG is set.
"""

import os
import sys
from pathlib import Path
from pkgutil import resolve_name


def _debug() -> None:
    # Inject a option to debug if environment variable QT_DEBUG is set.
    if not os.environ.get("QT_DEBUG"):
        return
    # Show QLibraryInfo paths.
    qtcore = resolve_name("PyQt5.QtCore")
    data = {}
    for key, value in qtcore.QLibraryInfo.__dict__.items():
        if isinstance(value, (qtcore.QLibraryInfo.LibraryLocation, int)):
            data[key] = Path(qtcore.QLibraryInfo.location(value))
    print("QLibraryInfo:", file=sys.stderr)
    for key, value in data.items():
        print(" ", key, value, file=sys.stderr)
    print("LibraryPaths:", file=sys.stderr)
    print(" ", qtcore.QCoreApplication.libraryPaths(), file=sys.stderr)
    print("FrozenDir:", sys.frozen_dir, file=sys.stderr)


_debug()
