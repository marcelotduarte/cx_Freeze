# Samples

Here are samples to test cx_Freeze or to show how to use a package in cx_Freeze.

# Installation and requirements:

In a virtual environment, install by issuing the command:

```
pip install --upgrade cx_Freeze PyQt5
```

Using conda-forge:

```
conda install --conda-forge cx_freeze pyqt
```

# Support for inclusion of extra plugins:

Please check the setup.py as example on how to use this feature.

cx_Freeze imports automatically the following plugins depending of the use of
some modules:
- imageformats - QtGui
- platforms - QtGui
- mediaservice - QtMultimedia
- printsupport - QtPrintSupport
