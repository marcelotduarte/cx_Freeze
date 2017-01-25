# About cx_Freeze

**cx_Freeze** is a set of scripts and modules for freezing Python scripts into executables,
in much the same way that [py2exe](http://www.py2exe.org/) and
[py2app](https://pythonhosted.org/py2app/) do. Unlike these two tools, cx_Freeze is cross
platform and should work on any platform that Python itself works on. It supports
[Python](https://www.python.org/) 2.7 or higher (including Python 3).

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

The official documentation is available at https://cx-freeze.readthedocs.io/

If you need help you can also ask on the official mailing list:
https://lists.sourceforge.net/lists/listinfo/cx-freeze-users

