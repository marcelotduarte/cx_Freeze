[![PyPI version](https://img.shields.io/pypi/v/cx_Freeze)](https://pypi.org/project/cx-freeze/)
[![PyPi Downloads](https://img.shields.io/pypi/dm/cx_Freeze)](https://pypistats.org/packages/cx-freeze)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/cx_freeze/badges/version.svg)](https://anaconda.org/conda-forge/cx_freeze)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/cx_freeze/badges/downloads.svg)](https://anaconda.org/conda-forge/cx_freeze)
[![Python](https://img.shields.io/pypi/pyversions/cx-freeze)](https://www.python.org/)
[![Documentation Status](https://readthedocs.org/projects/cx-freeze/badge/?version=latest)](https://cx-freeze.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/pypi/l/cx_Freeze.svg)](https://pypi.org/project/cx-Freeze/)
[![LGTM](https://img.shields.io/lgtm/grade/python/g/marcelotduarte/cx_Freeze.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/marcelotduarte/cx_Freeze)


**cx\_Freeze** creates standalone executables from Python scripts, with the same
performance, is cross-platform and should work on any platform that Python
itself works on.

# Highlights of Version 6.2 up to 6.9:
- Support for pathlib.Path
- New or improved hooks, with emphasis on matplotlib, numpy, PyQt5 and PySide2
- New ModuleFinder engine uses importlib.machinery
- Refactored Freezer
- New support for package metadata improving Module and new DitributionCache
- Enhanced support for Python 3.8 and Python 3.9, including MSYS2 and Anaconda distributions
- Improvements for multiprocessing
- Optimizations in detection and distribution of libraries
- Integrated to setuptools and importlib-metadata
- Code modernization
- Various bug fixes.

# Installation

In a virtual environment, install by issuing the command:

```
pip install --upgrade cx_Freeze
```

To install beta versions:
```
pip install --upgrade cx_Freeze --pre
```

Please check the installation in documentation for requirements.

# Documentation

The official documentation is available
[here](https://cx-freeze.readthedocs.io).

If you need help you can also ask on the discussion channel:
https://github.com/marcelotduarte/cx_Freeze/discussions

# License

cx\_Freeze uses a license derived from the
[Python Software Foundation License](https://www.python.org/psf/license).
You can read the cx\_Freeze license in the
[documentation](https://cx-freeze.readthedocs.io/en/latest/license.html)
or in the [source repository](doc/src/license.rst).
