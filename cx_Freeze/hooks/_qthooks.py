"""A collection of functions which are the base to hooks for PyQt5, PyQt6,
PySide2 and PySide6."""

import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Tuple

from ..finder import ModuleFinder
from ..module import Module

DARWIN = sys.platform == "darwin"
WIN32 = sys.platform == "win32"


def _qt_implementation(module: Module) -> str:
    """Helper function to get the name of the Qt implementation."""
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
        if hasattr(lib.LibraryPath, "__members__"):
            for key, value in lib.LibraryPath.__members__.items():
                source_paths[key] = Path(lib.path(value))
        else:
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
    source_paths.setdefault("SettingsPath", ".")

    # set the target paths
    data: Dict[str, Tuple[Path, Path]] = {}
    target_base = Path("lib", name)
    try:
        target_base = target_base / prefix_path.relative_to(qt_root_dir)
    except ValueError:
        pass
    if name == "PyQt5" and prefix_path.name != "Qt5":
        # conda pyqt
        target_base = target_base / "Qt5"

    # set some defaults or use relative path
    for key, source in source_paths.items():
        if key == "SettingsPath":
            target = Path("Contents/Resources" if DARWIN else ".")
        elif key in ("ArchDataPath", "DataPath", "PrefixPath"):
            target = target_base
        elif key == "BinariesPath":
            target = target_base / "bin"
        elif key == "LibrariesPath":
            target = target_base / "lib"
        elif key == "LibraryExecutablesPath":
            target = target_base / ("bin" if WIN32 else "libexec")
        elif key == "PluginsPath":
            target = target_base / "plugins"
        elif key == "TranslationsPath":
            target = target_base / "translations"
        elif source == Path("."):
            target = target_base
        else:
            target = target_base / source.relative_to(prefix_path)
        data[key] = source, target

    # debug
    if os.environ.get("QT_DEBUG"):
        print("QLibraryInfo:")
        for key, (source, target) in sorted(data.items()):
            print(" ", key, source, "->", target)
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
    source_path, target_path = libraryinfo_paths[variable]  # type: Path, Path
    for arg in args[1:]:
        if "*" in arg:
            # XXX: this code needs improvement
            for source in source_path.glob(arg):
                if source.is_file():
                    finder.include_files(source, target_path / source.name)
            return
        source_path = source_path / arg
        target_path = target_path / arg
    if not source_path.exists():
        return
    finder.include_files(source_path, target_path)


def load_qt_phonon(finder: ModuleFinder, module: Module) -> None:
    """In Windows, phonon5.dll requires an additional dll phonon_ds94.dll to
    be present in the build directory inside a folder phonon_backend."""
    if WIN32:
        name = _qt_implementation(module)
        copy_qt_files(finder, name, "PluginsPath", "phonon_backend")


def load_qt_qt(finder: ModuleFinder, module: Module) -> None:
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


def load_qt_qtcharts(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_qt_qtdatavisualization(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtGui")


def load_qt_qtdesigner(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module("datetime")
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_files(finder, name, "PluginsPath", "designer")


def load_qt_qtgui(finder: ModuleFinder, module: Module) -> None:
    """There is a chance that QtGui will use some image formats, then, add the
    image format plugins."""
    name = _qt_implementation(module)
    copy_qt_files(finder, name, "PluginsPath", "imageformats")
    # On Qt5, we need the platform plugins. For simplicity, we just copy
    # any that are installed.
    copy_qt_files(finder, name, "PluginsPath", "platforms")
    copy_qt_files(finder, name, "PluginsPath", "platformthemes")
    copy_qt_files(finder, name, "PluginsPath", "styles")


def load_qt_qthelp(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_qt_qtlocation(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtPositioning")


def load_qt_qtmultimedia(finder: ModuleFinder, module: Module) -> None:
    """This module depends on other modules and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")
    finder.include_module(f"{name}.QtMultimediaWidgets")
    copy_qt_files(finder, name, "PluginsPath", "audio")
    copy_qt_files(finder, name, "PluginsPath", "mediaservice")


def load_qt_qtmultimediawidgets(finder: ModuleFinder, module: Module) -> None:
    """This module depends on other modules."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    finder.include_module(f"{name}.QtMultimedia")


def load_qt_qtopengl(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_files(finder, name, "PluginsPath", "renderers")


def load_qt_qtpositioning(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    copy_qt_files(finder, name, "PluginsPath", "position")


def load_qt_qtprintsupport(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_files(finder, name, "PluginsPath", "printsupport")


def load_qt_qtqml(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")
    copy_qt_files(finder, name, "PluginsPath", "qmltooling")


def load_qt_qtscripttools(finder: ModuleFinder, module: Module) -> None:
    """This module depends on other modules."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    finder.include_module(f"{name}.QtScript")


def load_qt_qtsql(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_files(finder, name, "PluginsPath", "sqldrivers")


def load_qt_qtsvg(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_qt_qttest(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_qt_qtuitools(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_qt_qtwebengine(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWebEngineCore")


def load_qt_qtwebenginecore(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another modules and QtWebEngineProcess files."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtGui")
    finder.include_module(f"{name}.QtNetwork")
    if WIN32:
        for filename in (
            "QtWebEngineProcess.exe",
            "d3dcompiler_47.dll",
            "libEGL.dll",
            "libGLESv2.dll",
            "opengl32sw.dll",
        ):
            # pyside2 - only QtWebEngineProcess is in LibraryExecutablesPath
            # pyside6 - like pyside2, but the two lib*.dll are missing
            copy_qt_files(finder, name, "ArchDataPath", filename)
            # pyqt5 - all files listed in LibraryExecutablesPath
            copy_qt_files(finder, name, "LibraryExecutablesPath", filename)
    elif DARWIN:
        copy_qt_files(
            finder, name, "LibrariesPath", "QtWebEngineCore.framework"
        )
    else:
        copy_qt_files(
            finder, name, "LibraryExecutablesPath", "QtWebEngineProcess"
        )
        # conda-forge linux
        copy_qt_files(finder, name, "LibrariesPath", "libnss*.*")
    copy_qt_files(finder, name, "DataPath", "resources")
    copy_qt_files(finder, name, "TranslationsPath")


def load_qt_qtwebenginewidgets(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module, data and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWebChannel")
    finder.include_module(f"{name}.QtWebEngineCore")
    finder.include_module(f"{name}.QtWidgets")
    finder.include_module(f"{name}.QtPrintSupport")
    copy_qt_files(finder, name, "LibrariesPath", "*WebEngineWidgets.*")
    copy_qt_files(finder, name, "PluginsPath", "webview")
    copy_qt_files(finder, name, "PluginsPath", "xcbglintegrations")


def load_qt_qtwebkit(finder: ModuleFinder, module: Module) -> None:
    """This module depends on other modules."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")
    finder.include_module(f"{name}.QtGui")


def load_qt_qtwebsockets(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")


def load_qt_qtwidgets(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtGui")


def load_qt_qtxmlpatterns(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")


def load_qt_uic(finder: ModuleFinder, module: Module) -> None:
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
    if source_dir.exists():
        finder.include_files(source_dir, f"{name}.uic.widget-plugins")
