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
[![Coverage](https://raw.githubusercontent.com/marcelotduarte/cx_Freeze/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Documentation Status](https://readthedocs.org/projects/cx-freeze/badge/?version=stable)](https://cx-freeze.readthedocs.io/en/stable/?badge=stable)

# Installation

Choose the Python package manager according to your system. See how the
installation works with the most common ones, which are pip and conda.

To install the latest version of `cx_Freeze` using `pip` into a
virtual environment:
```
pip install --upgrade cx_Freeze
```

To install the latest development build:

```
pip uninstall cx_Freeze
pip install --extra-index-url https://test.pypi.org/simple/ cx_Freeze --pre --no-cache
```

Installing cx_freeze from the conda-forge channel can be achieved with the
command:
```
conda install conda-forge::cx_freeze
```

Please check the
[installation](https://cx-freeze.readthedocs.io/en/latest/installation.html)
for more information.

# Documentation

The official documentation is available
[here](https://cx-freeze.readthedocs.io).

If you need help you can also ask on the
[discussion](https://github.com/marcelotduarte/cx_Freeze/discussions) channel.

# What's New v7.2:
- Improved bdist_dmg
- Add license for msi (bdist_msi)
- Minor improvements in bdist_appimage
- Drop rpm2_mode in bdist_rpm
- Use an optimized mode as default for pip installations of selected packages
- hooks: support numpy 2.0, rasterio, multiprocess (a multiprocessing fork), etc
- Regression fixes, bug fixes and improvements

# What's New v7.1:
- Added new option --zip-filename in build_exe
- Bug fixes and improvements

# What's New v7.0:
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
