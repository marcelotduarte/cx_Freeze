"""A collection of functions which are triggered automatically by finder when
PySide2 package is included."""

from .pyqt5 import load_pyqt5 as load_pyside2
from .pyqt5 import load_pyqt5_qt as load_pyside2_qt
from .pyqt5 import load_pyqt5_qtcharts as load_pyside2_qtcharts
from .pyqt5 import (
    load_pyqt5_qtdatavisualization as load_pyside2_qtdatavisualization,
)
from .pyqt5 import load_pyqt5_qtdesigner as load_pyside2_qtdesigner
from .pyqt5 import load_pyqt5_qtgui as load_pyside2_qtgui
from .pyqt5 import load_pyqt5_qthelp as load_pyside2_qthelp
from .pyqt5 import load_pyqt5_qtlocation as load_pyside2_qtlocation
from .pyqt5 import load_pyqt5_qtmultimedia as load_pyside2_qtmultimedia
from .pyqt5 import (
    load_pyqt5_qtmultimediawidgets as load_pyside2_qtmultimediawidgets,
)
from .pyqt5 import load_pyqt5_qtopengl as load_pyside2_qtopengl
from .pyqt5 import load_pyqt5_qtpositioning as load_pyside2_qtpositioning
from .pyqt5 import load_pyqt5_qtprintsupport as load_pyside2_qtprintsupport
from .pyqt5 import load_pyqt5_qtqml as load_pyside2_qtqml
from .pyqt5 import load_pyqt5_qtscripttools as load_pyside2_qtscripttools
from .pyqt5 import load_pyqt5_qtsql as load_pyside2_qtsql
from .pyqt5 import load_pyqt5_qtsvg as load_pyside2_qtsvg
from .pyqt5 import load_pyqt5_qttest as load_pyside2_qttest
from .pyqt5 import load_pyqt5_qtuitools as load_pyside2_qtuitools
from .pyqt5 import load_pyqt5_qtwebengine as load_pyside2_qtwebengine
from .pyqt5 import load_pyqt5_qtwebenginecore as load_pyside2_qtwebenginecore
from .pyqt5 import (
    load_pyqt5_qtwebenginewidgets as load_pyside2_qtwebenginewidgets,
)
from .pyqt5 import load_pyqt5_qtwebkit as load_pyside2_qtwebkit
from .pyqt5 import load_pyqt5_qtwebsockets as load_pyside2_qtwebsockets
from .pyqt5 import load_pyqt5_qtwidgets as load_pyside2_qtwidgets
from .pyqt5 import load_pyqt5_qtxmlpatterns as load_pyside2_qtxmlpatterns
from .pyqt5 import load_pyqt5_uic as load_pyside2_uic

__all__ = [
    "load_pyside2",
    "load_pyside2_qt",
    "load_pyside2_qtcharts",
    "load_pyside2_qtdatavisualization",
    "load_pyside2_qtdesigner",
    "load_pyside2_qtgui",
    "load_pyside2_qthelp",
    "load_pyside2_qtlocation",
    "load_pyside2_qtmultimedia",
    "load_pyside2_qtmultimediawidgets",
    "load_pyside2_qtopengl",
    "load_pyside2_qtpositioning",
    "load_pyside2_qtprintsupport",
    "load_pyside2_qtqml",
    "load_pyside2_qtscripttools",
    "load_pyside2_qtsql",
    "load_pyside2_qtsvg",
    "load_pyside2_qttest",
    "load_pyside2_qtuitools",
    "load_pyside2_qtwebengine",
    "load_pyside2_qtwebenginecore",
    "load_pyside2_qtwebenginewidgets",
    "load_pyside2_qtwebkit",
    "load_pyside2_qtwebsockets",
    "load_pyside2_qtwidgets",
    "load_pyside2_qtxmlpatterns",
    "load_pyside2_uic",
]
