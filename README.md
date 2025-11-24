**cx_Freeze** Creates standalone executables from Python scripts with the same performance
as the original script.

It is cross-platform and should work on any platform that Python runs on.

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

> [!NOTE]
> For more information, please check the
> [installation](https://cx-freeze.readthedocs.io/en/latest/installation.html).

> [!IMPORTANT]
> If you are creating "service" standalone executables, see this
> [readme](https://github.com/marcelotduarte/cx_Freeze/tree/main/samples/service#readme).

# Changelog

[Changelog](https://github.com/marcelotduarte/cx_Freeze/blob/main/CHANGELOG.md)

# Documentation

[Documentation](https://cx-freeze.readthedocs.io).

If you need help you can also ask on the
[discussion](https://github.com/marcelotduarte/cx_Freeze/discussions) channel.

# License

cx_Freeze uses a license derived from the
[Python Software Foundation License](https://www.python.org/psf/license).
You can read the cx_Freeze license in the
[documentation](https://cx-freeze.readthedocs.io/en/stable/license.html)
or in the [source repository](LICENSE.md).
