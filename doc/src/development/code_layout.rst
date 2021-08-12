
The project's code layout
=========================

* ``cx_Freeze/`` (Python files)

  * ``cli.py`` - The code behind the :ref:`cxfreeze script <script>`.
  * ``dist.py`` - The classes and functions with which cx_Freeze :ref:`extends
    setuptools <setup_script>`.
  * ``finder.py`` - Module Finder - discovers what modules are required by the code.
  * ``freezer.py`` - The core class for freezing code.
  * ``hooks.py`` - A collection of functions which are triggered automatically
    by ``finder.py`` when certain packages are included or not found.
  * ``macdist.py`` - Extends setuptools to build macOS dmg or app blundle.
  * ``module.py`` - Base class for Module and ConstantsModule.
  * ``windist.py`` - Extends setuptools to build Windows installer packages.

* ``source/`` (C files)

  * ``bases/`` - The source of the base executables which are used to launch
    your Python applications. Different bases serve for different types of
    application on Windows (GUI, console application or service). The base
    executable calls the initscript, which in turn calls the user's code.
  * ``util.c`` - Compiled functions for cx_Freeze itself. Compiles to
    :mod:`cx_Freeze.util`. Functions are used only on Windows.

* ``doc/`` - The Sphinx documentation.
* ``initscripts/`` - Python scripts which set up the interpreter to run from
  frozen code, then load the code from the zip file and set it running.
* ``samples/`` - Examples of using cx_Freeze with a number of common modules.
