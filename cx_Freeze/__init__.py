import setuptools
import sys
from cx_Freeze.dist import (
    bdist_rpm,
    build,
    build_exe,
    install,
    install_exe,
    setup,
)

if sys.platform == "win32":
    from cx_Freeze.windist import bdist_msi
elif sys.platform == "darwin":
    from cx_Freeze.macdist import bdist_dmg, bdist_mac
from cx_Freeze.finder import Module, ModuleFinder
from cx_Freeze.freezer import ConfigError, ConstantsModule, Executable, Freezer

try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata

__version__ = importlib_metadata.version("cx_Freeze")
version = __version__
