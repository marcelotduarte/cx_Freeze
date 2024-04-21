**cx\_Freeze** creates standalone executables from Python scripts, with the
same performance, is cross-platform and should work on any platform that Python
itself works on.

#

[![PyPI version](https://img.shields.io/pypi/v/cx_Freeze)](https://pypi.org/project/cx-freeze/)
[![PyPi Downloads](https://img.shields.io/pypi/dm/cx_Freeze)](https://pypistats.org/packages/cx-freeze)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/cx_freeze.svg)](https://anaconda.org/conda-forge/cx_freeze)
[![Conda Downloads](https://anaconda.org/conda-forge/cx_freeze/badges/downloads.svg)](https://anaconda.org/conda-forge/cx_freeze)
[![Python](https://img.shields.io/pypi/pyversions/cx-freeze)](https://www.python.org/)
[![Actions status](https://github.com/marcelotduarte/cx_Freeze/workflows/CI/badge.svg)](https://github.com/marcelotduarte/cx_Freeze/actions/workflows/ci.yml)
[![CodeQL](https://github.com/marcelotduarte/cx_Freeze/workflows/CodeQL/badge.svg)](https://github.com/marcelotduarte/cx_Freeze/actions/workflows/codeql.yml)
[![Coverage](https://img.shields.io/codecov/c/github/marcelotduarte/cx_Freeze/main.svg?logo=codecov&logoColor=white)](https://codecov.io/gh/marcelotduarte/cx_Freeze)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Documentation Status](https://readthedocs.org/projects/cx-freeze/badge/?version=stable)](https://cx-freeze.readthedocs.io/en/stable/?badge=stable)

# Installation

In a virtual environment, install by issuing the command:

```
pip install --upgrade cx_Freeze
```

To install the latest development build:

```
pip install --force --no-cache --pre --extra-index-url https://marcelotduarte.github.io/packages/ cx_Freeze
```

Please check the
[installation](https://cx-freeze.readthedocs.io/en/latest/installation.html)
for more information and how to install in other environments such as pipenv,
conda-forge, etc.

# Documentation

The official documentation is available
[here](https://cx-freeze.readthedocs.io).

If you need help you can also ask on the
[discussion](https://github.com/marcelotduarte/cx_Freeze/discussions) channel.

# What's New:
- Added support for [pyproject.toml](https://cx-freeze.readthedocs.io/en/stable/setup_script.html)
- Create Linux AppImage format: [bdist_appimage](https://cx-freeze.readthedocs.io/en/stable/bdist_appimage.html)
- Create an DEB distribution: [bdist_deb](https://cx-freeze.readthedocs.io/en/stable/bdist_deb.html)
- Improved bdist_mac
- New and updated hooks, including support for QtWebengine on macOS
- Python 3.12 support.
- Improved tests and coverage ( >80% ).
- Bug fixes and improvements

# License

cx\_Freeze uses a license derived from the
[Python Software Foundation License](https://www.python.org/psf/license).
You can read the cx\_Freeze license in the
[documentation](https://cx-freeze.readthedocs.io/en/stable/license.html)
or in the [source repository](LICENSE.md).
