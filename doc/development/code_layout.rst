
The project's code layout
=========================

* ``cx_Freeze/`` (Python files)

  * ``freezer.py`` - The core class for freezing code.
  * ``finder.py`` - Discovers what modules are required by the code
  * ``hooks.py`` - A collection of functions which are triggered automatically
    by ``finder.py`` when certain packages are included or not found.
  * ``dist.py`` - The classes and functions with which cx_Freeze :ref:`extends
    distutils <distutils>`.
  * ``windist.py`` - Extends distutils to build Windows installer packages.
  * ``main.py`` - The code behind the :ref:`cxfreeze script <script>`.

* ``source/`` (C files)

  * ``util.c`` - Compiled functions for cx_Freeze itself. Compiles to
    :mod:`cx_Freeze.util`. Most of the functions are used only on Windows.
  * ``bases/`` - The source of the base executables which are used to launch
    your Python applications. Different bases serve for different types of
    application on Windows (GUI, console application or service). The base
    executable calls the initscript, which in turn calls the user's code.

* ``initscripts/`` - Python scripts which set up the interpreter to run from
  frozen code, then load the code from the zip file and set it running.
* ``samples/`` - Examples of using cx_Freeze with a number of common modules.
* ``doc/`` - The Sphinx documentation.
