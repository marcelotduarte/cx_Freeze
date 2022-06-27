"""A collection of functions which are triggered automatically by finder when
PySide6 package is included."""

from .pyqt5 import load_pyqt5 as load_pyside6
from .pyqt5 import load_pyqt5_qt as load_pyside6_qt
from .pyqt5 import load_pyqt5_qtcharts as load_pyside6_qtcharts
from .pyqt5 import (
    load_pyqt5_qtdatavisualization as load_pyside6_qtdatavisualization,
)
from .pyqt5 import load_pyqt5_qtgui as load_pyside6_qtgui
from .pyqt5 import load_pyqt5_qthelp as load_pyside6_qthelp
from .pyqt5 import load_pyqt5_qtlocation as load_pyside6_qtlocation
from .pyqt5 import load_pyqt5_qtmultimedia as load_pyside6_qtmultimedia
from .pyqt5 import (
    load_pyqt5_qtmultimediawidgets as load_pyside6_qtmultimediawidgets,
)
from .pyqt5 import load_pyqt5_qtopengl as load_pyside6_qtopengl
from .pyqt5 import load_pyqt5_qtpositioning as load_pyside6_qtpositioning
from .pyqt5 import load_pyqt5_qtprintsupport as load_pyside6_qtprintsupport
from .pyqt5 import load_pyqt5_qtqml as load_pyside6_qtqml
from .pyqt5 import load_pyqt5_qtscripttools as load_pyside6_qtscripttools
from .pyqt5 import load_pyqt5_qtsql as load_pyside6_qtsql
from .pyqt5 import load_pyqt5_qtsvg as load_pyside6_qtsvg
from .pyqt5 import load_pyqt5_qttest as load_pyside6_qttest
from .pyqt5 import load_pyqt5_qtuitools as load_pyside6_qtuitools
from .pyqt5 import load_pyqt5_qtwebengine as load_pyside6_qtwebengine
from .pyqt5 import load_pyqt5_qtwebenginecore as load_pyside6_qtwebenginecore
from .pyqt5 import (
    load_pyqt5_qtwebenginewidgets as load_pyside6_qtwebenginewidgets,
)
from .pyqt5 import load_pyqt5_qtwebkit as load_pyside6_qtwebkit
from .pyqt5 import load_pyqt5_qtwebsockets as load_pyside6_qtwebsockets
from .pyqt5 import load_pyqt5_qtwidgets as load_pyside6_qtwidgets
from .pyqt5 import load_pyqt5_qtxmlpatterns as load_pyside6_qtxmlpatterns
from .pyqt5 import load_pyqt5_uic as load_pyside6_uic

__all__ = [
    "load_pyside6",
    "load_pyside6_qt",
    "load_pyside6_qtcharts",
    "load_pyside6_qtdatavisualization",
    "load_pyside6_qtgui",
    "load_pyside6_qthelp",
    "load_pyside6_qtlocation",
    "load_pyside6_qtmultimedia",
    "load_pyside6_qtmultimediawidgets",
    "load_pyside6_qtopengl",
    "load_pyside6_qtpositioning",
    "load_pyside6_qtprintsupport",
    "load_pyside6_qtqml",
    "load_pyside6_qtscripttools",
    "load_pyside6_qtsql",
    "load_pyside6_qtsvg",
    "load_pyside6_qttest",
    "load_pyside6_qtuitools",
    "load_pyside6_qtwebengine",
    "load_pyside6_qtwebenginecore",
    "load_pyside6_qtwebenginewidgets",
    "load_pyside6_qtwebkit",
    "load_pyside6_qtwebsockets",
    "load_pyside6_qtwidgets",
    "load_pyside6_qtxmlpatterns",
    "load_pyside6_uic",
]
