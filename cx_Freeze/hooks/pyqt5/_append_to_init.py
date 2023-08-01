"""Module used to inject a code to guessing and set the plugins directory."""
import os
import sys
from pathlib import Path


def _run():
    qtcore = __import__("PyQt5", fromlist=["QtCore"]).QtCore

    # With PyQt5 5.15.4, if the folder name contains non-ascii characters, the
    # libraryPaths returns empty. Prior to this version, this doesn't happen.
    executable_dir = Path(sys.executable).parent
    qt_root_dir = executable_dir / "lib" / "PyQt5"
    plugins_dir = qt_root_dir / "Qt5" / "plugins"  # PyQt5 5.15.4
    if not plugins_dir.is_dir():
        plugins_dir = qt_root_dir / "Qt" / "plugins"
    if not plugins_dir.is_dir():
        plugins_dir = qt_root_dir / "plugins"
    if plugins_dir.is_dir():
        qtcore.QCoreApplication.addLibraryPath(plugins_dir.as_posix())

    # Inject a option to debug if environment variable QT_DEBUG is set.
    if os.environ.get("QT_DEBUG"):
        # Show QLibraryInfo paths.
        data = {}
        for key, value in qtcore.QLibraryInfo.__dict__.items():
            if isinstance(value, (qtcore.QLibraryInfo.LibraryLocation, int)):
                data[key] = Path(qtcore.QLibraryInfo.location(value))
        print("QLibraryInfo:", file=sys.stdout)
        for key, value in data.items():
            print(" ", key, value, file=sys.stdout)
        print("LibraryPaths:", file=sys.stdout)
        print(" ", qtcore.QCoreApplication.libraryPaths(), file=sys.stdout)


_run()
