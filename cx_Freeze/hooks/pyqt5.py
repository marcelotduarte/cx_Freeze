"""A collection of functions which are triggered automatically by finder when
PyQt5 package is included."""

import sys
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Tuple

from ..finder import ModuleFinder
from ..module import Module

DARWIN = sys.platform == "darwin"
WIN32 = sys.platform == "win32"


def _qt_implementation(module: Module) -> str:
    """Helper function to get the name of the Qt implementation (PyQt5)."""
    return module.name.split(".")[0]


@lru_cache(maxsize=None)
def _qt_libraryinfo_paths(name: str) -> Dict[str, Tuple[Path, Path]]:
    """Cache the QtCore library paths."""

    try:
        qtcore = __import__(name, fromlist=["QtCore"]).QtCore
    except RuntimeError:
        print("WARNING: Tried to load multiple incompatible Qt ", end="")
        print("wrappers. Some incorrect files may be copied.")
        return {}

    # get paths from QLibraryInfo
    source_paths: Dict[str, Path] = {}
    lib = qtcore.QLibraryInfo
    major_version = lib.version().majorVersion()
    if major_version == 6:
        for key, value in lib.__dict__.items():
            if isinstance(value, lib.LibraryPath):
                source_paths[key] = Path(lib.path(value))
    else:
        for key, value in lib.__dict__.items():
            if isinstance(value, (lib.LibraryLocation, int)):
                source_paths[key] = Path(lib.location(value))
    qt_root_dir = Path(qtcore.__file__).parent

    # if QLibraryInfo has incomplete information
    if not source_paths.get("PluginsPath"):
        # Qt Plugins can be in a plugins directory next to the Qt libraries
        plugins_path = qt_root_dir / "plugins"
        if not plugins_path.exists():
            plugins_path = qt_root_dir / "Qt5" / "plugins"  # PyQt5 5.15.4
        # or in a special location in conda-forge
        if not plugins_path.exists():
            plugins_path = Path(sys.base_prefix, "Library", "plugins")
        # default location
        if not plugins_path.exists():
            plugins_path = qt_root_dir / "Qt" / "plugins"
        source_paths["PluginsPath"] = plugins_path
    source_paths.setdefault("PrefixPath", source_paths["PluginsPath"].parent)
    prefix_path = source_paths["PrefixPath"]
    source_paths.setdefault("DataPath", prefix_path)
    source_paths.setdefault("LibrariesPath", prefix_path / "lib")

    # set the target paths
    data: Dict[str, Tuple[Path, Path]] = {}
    add_qt_subdir = None
    if name == "PyQt5" and prefix_path.name != "Qt5":
        # conda pyqt
        add_qt_subdir = "Qt5"
    elif name == "PySide2" and prefix_path.name != "Qt":
        # conda pyside2, pyside2 windows
        add_qt_subdir = "Qt"
    for key, source in source_paths.items():
        if key == "SettingsPath":
            if DARWIN:
                target = Path("Contents/Resources")
            else:
                target = Path(".")
        elif source == Path("."):
            print(".......", key, source)
            target = source
        else:
            target = Path("lib", name)
            if add_qt_subdir:
                target = target / add_qt_subdir
            try:
                target = target / source.relative_to(qt_root_dir)
            except ValueError:
                # msys2 and conda-forge
                target = target / source.relative_to(prefix_path)
        data[key] = source, target

    # debug
    print("QLibraryInfo:")
    for key, (source, target) in data.items():
        print(" ", key, "\n   ", source, "->", target)
    return data


def get_qt_plugins_paths(name: str, plugins: str) -> List[Tuple[Path, Path]]:
    """Helper function to get a list of source and target paths of Qt plugins,
    indicated to be used in include_files."""
    libraryinfo_paths = _qt_libraryinfo_paths(name)
    source_path, target_path = libraryinfo_paths["PluginsPath"]
    source_path = source_path / plugins
    if not source_path.exists():
        return []
    return [(source_path, target_path / plugins)]


def copy_qt_files(finder: ModuleFinder, name: str, *args) -> None:
    """Helper function to find and copy Qt plugins, resources, translations,
    etc."""
    variable = args[0]
    libraryinfo_paths = _qt_libraryinfo_paths(name)
    source_path, target_path = libraryinfo_paths[variable]
    for i in range(1, len(args)):
        source_path = source_path / args[i]
        target_path = target_path / args[i]
    if not source_path.exists():
        return
    finder.include_files(source_path, target_path)


def load_pyqt5(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PyQt5 __init__ to locate and load plugins and resources.
    Also, this fixes issues with conda-forge versions."""
    if module.code is None:
        return
    # With PyQt5 5.15.4, if the folder name contains non-ascii characters, the
    # libraryPaths returns empty. Prior to this version, this doesn't happen.
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
    print("QLibraryInfo:", file=sys.stderr)
    for key, value in data.items():
        print(" ", key, value, file=sys.stderr)
    print("LibraryPaths:", file=sys.stderr)
    print(" ", QCoreApplication.libraryPaths(), file=sys.stderr)
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
        copy_qt_files(finder, name, "PluginsPath", "phonon_backend")


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
    copy_qt_files(finder, name, "PluginsPath", "designer")


def load_pyqt5_qtgui(finder: ModuleFinder, module: Module) -> None:
    """There is a chance that QtGui will use some image formats, then, add the
    image format plugins."""
    name = _qt_implementation(module)
    copy_qt_files(finder, name, "PluginsPath", "imageformats")
    # On Qt5, we need the platform plugins. For simplicity, we just copy
    # any that are installed.
    copy_qt_files(finder, name, "PluginsPath", "platforms")
    copy_qt_files(finder, name, "PluginsPath", "platformthemes")
    copy_qt_files(finder, name, "PluginsPath", "styles")


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
    copy_qt_files(finder, name, "PluginsPath", "audio")
    copy_qt_files(finder, name, "PluginsPath", "mediaservice")


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
    copy_qt_files(finder, name, "PluginsPath", "renderers")


def load_pyqt5_qtpositioning(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    copy_qt_files(finder, name, "PluginsPath", "position")


def load_pyqt5_qtprintsupport(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_files(finder, name, "PluginsPath", "printsupport")


def load_pyqt5_qtqml(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")
    copy_qt_files(finder, name, "PluginsPath", "qmltooling")


def load_pyqt5_qtscripttools(finder: ModuleFinder, module: Module) -> None:
    """This module depends on other modules."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    finder.include_module(f"{name}.QtScript")


def load_pyqt5_qtsql(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_files(finder, name, "PluginsPath", "sqldrivers")


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
    if WIN32:
        copy_qt_files(
            finder, name, "LibraryExecutablesPath", "QtWebEngineProcess.exe"
        )
        copy_qt_files(
            finder, name, "LibraryExecutablesPath", "d3dcompiler_47.dll"
        )
        copy_qt_files(finder, name, "LibraryExecutablesPath", "libEGL.dll")
        copy_qt_files(finder, name, "LibraryExecutablesPath", "libGLESv2.dll")
        copy_qt_files(finder, name, "LibraryExecutablesPath", "opengl32sw.dll")
    elif DARWIN:
        copy_qt_files(
            finder, name, "LibrariesPath", "QtWebEngineCore.framework"
        )
    else:
        copy_qt_files(
            finder, name, "LibraryExecutablesPath", "QtWebEngineProcess"
        )
        # conda-forge linux
        copy_qt_files(finder, name, "LibrariesPath", "libnssckbi.so")
    copy_qt_files(finder, name, "DataPath", "resources")
    copy_qt_files(finder, name, "TranslationsPath")


def load_pyqt5_qtwebenginewidgets(
    finder: ModuleFinder, module: Module
) -> None:
    """This module depends on another module, data and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWebChannel")
    finder.include_module(f"{name}.QtWebEngineCore")
    finder.include_module(f"{name}.QtWidgets")
    finder.include_module(f"{name}.QtPrintSupport")
    copy_qt_files(finder, name, "PluginsPath", "webview")
    copy_qt_files(finder, name, "PluginsPath", "xcbglintegrations")


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
