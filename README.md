# About cx\_Freeze

**cx\_Freeze** is a set of scripts and modules for freezing Python scripts into
executables, in much the same way that [py2exe](http://www.py2exe.org/) and
[py2app](https://pythonhosted.org/py2app/) do. Unlike these two tools,
cx\_Freeze is cross platform and should work on any platform that Python itself works on. It supports [Python](https://www.python.org/) 3.5 or higher.

If you need support for Python 2.x, cx\_Freeze version 5 should be used
instead.

# Download/Install

Install by issuing the command

```
python -m pip install cx_Freeze --upgrade
```

or download directly from [PyPI](https://pypi.python.org/pypi/cx_Freeze).

If you do not have pip installed or would prefer a more manual installation
process, the following steps also work once the source package has been
downloaded and extracted:

```
python setup.py build
python setup.py install
```

To build with MSVC versions after 9.0 use this trick:

```
set VS100COMNTOOLS=%VS140COMNTOOLS%
```

# Documentation

The official documentation is available
[here](https://cx-freeze.readthedocs.io).

If you need help you can also ask on the official mailing list:
https://lists.sourceforge.net/lists/listinfo/cx-freeze-users

# License

cx\_Freeze uses a license derived from the
[Python Software Foundation License](https://www.python.org/psf/license).
You can read the cx\_Freeze license in the
[documentation](https://cx-freeze.readthedocs.io/en/latest/license.html)
or in the [source repository](doc/license.rst).

