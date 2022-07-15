"""A collection of functions which are triggered automatically by finder when
PyQt5 package is included."""

import sys
from pathlib import Path
from typing import List, Tuple

from ..finder import ModuleFinder
from ..module import Module

WIN32 = sys.platform == "win32"


def _qt_implementation(module: Module) -> str:
    """Helper function to get the name of the Qt implementation (PyQt5)."""
    return module.name.split(".")[0]


def _qt_library_paths(name: str) -> List[str]:
    """Cache the QtCore library paths."""
    if _qt_library_paths.data:
        return _qt_library_paths.data
    try:
        qtcore = __import__(name, fromlist=["QtCore"]).QtCore
    except RuntimeError:
        print("WARNING: Tried to load multiple incompatible Qt ", end="")
        print("wrappers. Some incorrect files may be copied.")
        qtcore = None
    else:
        data = [Path(p) for p in qtcore.QCoreApplication.libraryPaths()]
    if not data:
        # check the common location for conda
        plugins_path = Path(sys.base_prefix, "Library", "plugins")
        if plugins_path.exists():
            data.append(plugins_path)
        elif qtcore:
            # use a hack
            app = qtcore.QCoreApplication([])
            data = [Path(p) for p in app.libraryPaths()]
    if not data and qtcore:
        # Qt Plugins can be in a plugins directory next to the Qt libraries
        qt_root_dir = Path(qtcore.__file__).parent
        data.append(qt_root_dir / "plugins")
        data.append(qt_root_dir / "Qt5" / "plugins")
        data.append(qt_root_dir / "Qt" / "plugins")
    _qt_library_paths.data = data
    return data


_qt_library_paths.data: List[Path] = []


def get_qt_subdir_paths(name: str, subdir: str) -> List[Tuple[Path, Path]]:
    """Helper function to get a list of source and target paths of Qt
    subdirectories, indicated to be used in include_files."""
    include_files = []
    for library_dir in _qt_library_paths(name):
        if library_dir.parts[-1] == "plugins":
            library_dir = library_dir.parent
        source_path = library_dir / subdir
        if not source_path.exists():
            continue
        if library_dir.parts[-1] == name:  # {name}/{subdir}
            target_path = Path("lib") / name / subdir
        elif library_dir.parts[-2] == name:  # {name}/Qt*/{subdir}
            target_path = Path("lib") / name / library_dir.parts[-1] / subdir
        else:
            target_path = Path("lib") / name / "Qt" / subdir
        include_files.append((source_path, target_path))
    return include_files


def get_qt_plugins_paths(name: str, plugins: str) -> List[Tuple[str, str]]:
    """Helper function to get a list of source and target paths of Qt plugins,
    indicated to be used in include_files."""
    return get_qt_subdir_paths(name, str(Path("plugins", plugins)))


def copy_qt_data(name: str, subdir: str, finder: ModuleFinder) -> None:
    """Helper function to find and copy Qt resources, translations, etc."""
    for source_path, target_path in get_qt_subdir_paths(name, subdir):
        finder.include_files(source_path, target_path)


def copy_qt_plugins(name: str, plugins: str, finder: ModuleFinder) -> None:
    """Helper function to find and copy Qt plugins."""
    for source_path, target_path in get_qt_plugins_paths(name, plugins):
        finder.include_files(source_path, target_path)


def load_pyqt5(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PyQt5/PySide2 init to locate and load plugins."""
    if module.code is None:
        return
    # With PyQt5 5.15.4, if the folder name contains non-ascii characters, the
    # libraryPaths returns empty. Prior to this version, this doesn't happen.
    # With PySide2 the same happens in some versions.
    # So, this hack will be used to:
    # - fix empty libraryPaths
    # - workaround issues with anaconda
    # - locate plugins when using zip_include_packages
    name = _qt_implementation(module)
    code_string = module.file.read_text()
    code_string += f"""
# cx_Freeze patch start
import os
import sys
from pathlib import Path
from {name}.QtCore import QCoreApplication, QLibraryInfo

# configure
executable_dir = Path(sys.executable).parent
qt_root_dir = executable_dir / "lib" / "{name}"
plugins_dir = qt_root_dir / "Qt5" / "plugins"  # PyQt5 5.15.4
if not plugins_dir.is_dir():
    plugins_dir = qt_root_dir / "Qt" / "plugins"
if not plugins_dir.is_dir():
    plugins_dir = qt_root_dir / "plugins"
if plugins_dir.is_dir():
    QCoreApplication.addLibraryPath(plugins_dir.as_posix())

# debug
if os.environ.get("QT_DEBUG") or os.environ.get("QT_DEBUG_PLUGINS"):
    major_version = QLibraryInfo.version().majorVersion()
    data = dict()
    if major_version == 6:
        for key, value in QLibraryInfo.__dict__.items():
            if isinstance(value, QLibraryInfo.LibraryPath):
                data[key] = Path(QLibraryInfo.path(value))
    else:
        for key, value in QLibraryInfo.__dict__.items():
            if isinstance(value, (QLibraryInfo.LibraryLocation, int)):
                data[key] = Path(QLibraryInfo.location(value))
    print("QLibraryInfo:")
    for key, value in data.items():
        print(" ", key, value)
# cx_Freeze patch end
"""
    module.code = compile(code_string, str(module.file), "exec")
    if module.in_file_system == 0:
        module.in_file_system = 2  # use optimized mode
    finder.include_module(f"{name}.QtCore")  # imported by all modules


def load_pyqt5_phonon(finder: ModuleFinder, module: Module) -> None:
    """In Windows, phonon5.dll requires an additional dll phonon_ds94.dll to
    be present in the build directory inside a folder phonon_backend."""
    if WIN32:
        name = _qt_implementation(module)
        copy_qt_plugins(name, "phonon_backend", finder)


def load_pyqt5_qt(finder: ModuleFinder, module: Module) -> None:
    """The PyQt5.Qt module is an extension module which imports a number of
    other modules and injects their namespace into its own. It seems a
    foolish way of doing things but perhaps there is some hidden advantage
    to this technique over pure Python; ignore the absence of some of
    the modules since not every installation includes all of them."""
    name = _qt_implementation(module)
    for mod in (
        "_qt",
        "QtSvg",
        "Qsci",
        "QtAssistant",
        "QtNetwork",
        "QtOpenGL",
        "QtScript",
        "QtSql",
        "QtSvg",
        "QtTest",
        "QtXml",
    ):
        try:
            finder.include_module(f"{name}.{mod}")
        except ImportError:
            pass


def load_pyqt5_qtcharts(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_pyqt5_qtcore(finder: ModuleFinder, module: Module) -> None:
    """The PyQt5.QtCore module implicitly imports the sip module and,
    depending on configuration, the PyQt5._qt module."""
    name = _qt_implementation(module)
    try:
        finder.include_module(f"{name}.sip")  # PyQt5 >= 5.11
    except ImportError:
        finder.include_module("sip")
    try:
        finder.include_module(f"{name}._qt")
    except ImportError:
        pass


def load_pyqt5_qtdatavisualization(
    finder: ModuleFinder, module: Module
) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtGui")


def load_pyqt5_qtdesigner(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module("datetime")
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_plugins(name, "designer", finder)


def load_pyqt5_qtgui(finder: ModuleFinder, module: Module) -> None:
    """There is a chance that QtGui will use some image formats, then, add the
    image format plugins."""
    name = _qt_implementation(module)
    copy_qt_plugins(name, "imageformats", finder)
    # On Qt5, we need the platform plugins. For simplicity, we just copy
    # any that are installed.
    copy_qt_plugins(name, "platforms", finder)
    copy_qt_plugins(name, "styles", finder)


def load_pyqt5_qthelp(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_pyqt5_qtlocation(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtPositioning")


def load_pyqt5_qtmultimedia(finder: ModuleFinder, module: Module) -> None:
    """This module depends on other modules and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")
    finder.include_module(f"{name}.QtMultimediaWidgets")
    copy_qt_plugins(name, "audio", finder)
    copy_qt_plugins(name, "mediaservice", finder)


def load_pyqt5_qtmultimediawidgets(
    finder: ModuleFinder, module: Module
) -> None:
    """This module depends on other modules."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    finder.include_module(f"{name}.QtMultimedia")


def load_pyqt5_qtopengl(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_plugins(name, "renderers", finder)


def load_pyqt5_qtpositioning(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    copy_qt_plugins(name, "position", finder)


def load_pyqt5_qtprintsupport(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_plugins(name, "printsupport", finder)


def load_pyqt5_qtqml(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")
    copy_qt_plugins(name, "qmltooling", finder)


def load_pyqt5_qtscripttools(finder: ModuleFinder, module: Module) -> None:
    """This module depends on other modules."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    finder.include_module(f"{name}.QtScript")


def load_pyqt5_qtsql(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_plugins(name, "sqldrivers", finder)


def load_pyqt5_qtsvg(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_pyqt5_qttest(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_pyqt5_qtuitools(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_pyqt5_qtwebengine(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWebEngineCore")


def load_pyqt5_qtwebenginecore(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtGui")
    finder.include_module(f"{name}.QtNetwork")


def load_pyqt5_qtwebenginewidgets(
    finder: ModuleFinder, module: Module
) -> None:
    """This module depends on another module, data and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWebChannel")
    finder.include_module(f"{name}.QtWebEngineCore")
    finder.include_module(f"{name}.QtPrintSupport")
    if WIN32:
        copy_qt_data(name, "QtWebEngineProcess.exe", finder)
    else:
        copy_qt_data(name, "libexec", finder)
    copy_qt_data(name, "resources", finder)
    copy_qt_data(name, "translations", finder)
    copy_qt_plugins(name, "webview", finder)
    copy_qt_plugins(name, "xcbglintegrations", finder)


def load_pyqt5_qtwebkit(finder: ModuleFinder, module: Module) -> None:
    """This module depends on other modules."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")
    finder.include_module(f"{name}.QtGui")


def load_pyqt5_qtwebsockets(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")


def load_pyqt5_qtwidgets(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtGui")


def load_pyqt5_qtxmlpatterns(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")


def load_pyqt5_uic(finder: ModuleFinder, module: Module) -> None:
    """The uic module makes use of "plugins" that need to be read directly and
    cannot be frozen; the PyQt5.QtWebKit and PyQt5.QtNetwork modules are
    also implicity loaded."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")
    try:
        finder.include_module(f"{name}.QtWebKit")
    except ImportError:
        pass
    source_dir = module.path[0] / "widget-plugins"
    finder.include_files(source_dir, f"{name}.uic.widget-plugins")
