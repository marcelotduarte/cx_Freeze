"""Module used to inject a debug code to PySide2/__init__."""
import os
import sys
from pathlib import Path


def _debug():
    # Inject a option to debug if environment variable QT_DEBUG is set.
    if os.environ.get("QT_DEBUG"):
        qtcore = __import__("PySide2", fromlist=["QtCore"]).QtCore
        # Show QLibraryInfo paths.
        data = {}
        for key, value in qtcore.QLibraryInfo.__dict__.items():
            if isinstance(value, qtcore.QLibraryInfo.LibraryLocation):
                data[key] = Path(qtcore.QLibraryInfo.location(value))
        print("QLibraryInfo:", file=sys.stdout)
        for key, value in data.items():
            print(" ", key, value, file=sys.stdout)
        print("LibraryPaths:", file=sys.stdout)
        print(" ", qtcore.QCoreApplication.libraryPaths(), file=sys.stdout)


_debug()
