| Version | Downloads | Python | Code |
| --- | --- | --- | --- |
| [![PyPI version](https://img.shields.io/pypi/v/cx_Freeze)](https://pypi.org/project/cx-freeze/) | [![PyPi Downloads](https://img.shields.io/pypi/dm/cx_Freeze)](https://pypistats.org/packages/cx-freeze) | [![Python](https://img.shields.io/pypi/pyversions/cx-freeze)](https://www.python.org/) | ![CodeQL](https://github.com/marcelotduarte/cx_Freeze/workflows/CodeQL/badge.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) |
| [![Conda Version](https://img.shields.io/conda/vn/conda-forge/cx_freeze.svg)](https://anaconda.org/conda-forge/cx_freeze) | [![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/cx_freeze.svg)](https://anaconda.org/conda-forge/cx_freeze) | | |

**cx\_Freeze** creates standalone executables from Python scripts, with the same
performance, is cross-platform and should work on any platform that Python
itself works on.

# Installation

In a virtual environment, install by issuing the command:

```
pip install --upgrade cx_Freeze
```

To install the latest development build:

```
pip install --pre --extra-index-url https://marcelotduarte.github.io/packages/ cx_Freeze
```

Please check the [installation](https://cx-freeze.readthedocs.io/en/latest/installation.html)
for more information and how to install in others environment such as pipenv,
conda-forge, etc.

# Documentation

[![Documentation Status](https://readthedocs.org/projects/cx-freeze/badge/?version=latest)](https://cx-freeze.readthedocs.io/en/latest/?badge=latest)

The official documentation is available
[here](https://cx-freeze.readthedocs.io).

If you need help you can also ask on the [discussion](https://github.com/marcelotduarte/cx_Freeze/discussions) channel.

# Highlights of Version 6.14:
- Support Python 3.11
- Binary wheels (x86_64 and aarch64) for musllinux
- Maintain Windows base executables on git (install from sources without C compiler)
- Improved documentation
- New hooks: charset_normalizer, shapely, sklearn, pytorch
- Improved hooks: scipy, sqlite3
- Bug fixes and improvements

# Highlights of Version 6.2 up to 6.13:
- Binary wheels (x86_64 and aarch64) for manylinux and macOS (including Apple Silicon)
- New or improved hooks, especially matplotlib, numpy, PyQt5, PyQt6, PySide2, PySide6 and Tkinter
- Support Application Manifests in Windows: manifest and uac-admin
- Complete integration to setuptools instead of distutils
- New dependency resolver on Windows
- Support for pathlib.Path
- New ModuleFinder engine uses importlib.machinery
- Refactored Freezer
- New support for package metadata improving Module and new DitributionCache
- Enhanced support for Python 3.8 to 3.10, including MSYS2 and conda-forge distributions
- Improvements for multiprocessing
- Optimizations in detection and distribution of libraries
- Code modernization
- Various bug fixes.

# License

[![License](https://img.shields.io/pypi/l/cx_Freeze.svg)](https://cx-freeze.readthedocs.io/en/latest/license.html)

cx\_Freeze uses a license derived from the
[Python Software Foundation License](https://www.python.org/psf/license).
You can read the cx\_Freeze license in the
[documentation](https://cx-freeze.readthedocs.io/en/latest/license.html)
or in the [source repository](doc/src/license.rst).
