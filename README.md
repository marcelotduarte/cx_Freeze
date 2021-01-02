# About cx\_Freeze

**cx\_Freeze** creates standalone executables from Python scripts, with the same
performance, is cross-platform and should work on any platform that Python
itself works on.

It supports [Python](https://www.python.org/) 3.6 up to 3.9.

If you need support for older Python check the documentation.

# Highlights of Version 6.2 up to 6.5:
- Improved ModuleFinder, using importlib.machinery
- Support for package metadata
- Enhanced support for Python 3.8 and experimental support for Python 3.9
- Better support for MSYS2 and Anaconda (simultaneously launching the version)
- Improvements for multiprocessing
- Integrated to setuptools and importlib.metadata
- Code modernization
- Various bug fixes.

# Installation

In a virtual environment, install by issuing the command:

```
pip install cx_Freeze --upgrade
```

For other options, check the documentation.

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
