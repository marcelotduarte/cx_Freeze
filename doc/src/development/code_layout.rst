
The project's code layout
=========================

* ``cx_Freeze/`` (Python files)

  * ``command/`` - Creates or extends setuptools commands.

    * ``bdist_mac.py`` - Extends setuptools to build macOS dmg or app blundle.
    * ``bdist_msi.py`` - Extends setuptools to build Windows installer packages.
    * ``bdist_rpm.py`` - Extends setuptools to create an RPM distribution.
    * ``build_exe.py`` - Implements the 'build_exe' command.
    * ``install.py`` - Extends setuptools 'install' command.
    * ``install_exe.py`` - Implements the 'install_exe' command.

  * ``initscripts/`` - Python scripts which set up the interpreter to run from
    frozen code, then load the code from the zip file and set it running.
  * ``cli.py`` - The code behind the :ref:`cxfreeze script <script>`.
  * ``common.py`` - Common utility functions shared between cx_Freeze modules.
  * ``exception.py`` - Internal exception classes.
  * ``executable.py`` - Module for the Executable base class.
  * ``finder.py`` - Module Finder - discovers what modules are required by the
    code.
  * ``freezer.py`` - The core class for freezing scripts into executables.
  * ``hooks.py`` - A collection of functions which are triggered automatically
    by ``finder.py`` when certain packages are included or not found.
  * ``module.py`` - Base class for Module and ConstantsModule.
  * ``parser.py`` - Implements `Parser` interface to create an abstraction to
    parse binary files.
  * ``winmsvcr.py`` - DLL list of MSVC runtimes.
  * ``winversioninfo.py`` - Module for the VersionInfo base class.

* ``source/`` (C files)

  * ``bases/`` - The source of the base executables which are used to launch
    your Python applications. Different bases serve for different types of
    application on Windows (GUI, console application or service). The base
    executable calls the initscript, which in turn calls the user's code.
  * ``util.c`` - Compiled functions for cx_Freeze itself. Compiles to
    :mod:`cx_Freeze.util`. Functions are used only on Windows.

* ``doc/`` - The Sphinx documentation.
* ``samples/`` - Examples of using cx_Freeze with a number of common modules.
