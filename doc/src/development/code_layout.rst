
The project's code layout
=========================

* ``cx_Freeze/`` (Python files)

  * ``command/`` - Creates or extends setuptools commands.

    * ``bdist_appimage.py`` - Implements the 'bdist_appimage' command
      (create Linux AppImage format).
    * ``bdist_deb.py`` - Implements the 'bdist_deb' command
      (create DEB binary distributions).
    * ``bdist_mac.py`` - Implements the 'bdist_dmg' and 'bdist_mac' commands
      (create macOS dmg and/or app blundle.
    * ``bdist_msi.py`` - Implements the 'bdist_msi' command
      (create Windows installer packages).
    * ``bdist_rpm.py`` - Implements the 'bdist_rpm' command
      (create RPM binary distributions).
    * ``build_exe.py`` - Implements the 'build_exe' command.
    * ``install.py`` - Extends setuptools 'install' command.
    * ``install_exe.py`` - Implements the 'install_exe' command.

  * ``hooks/`` - A collection of functions which are triggered automatically
    by ``finder.py`` when certain packages are included or not found.
  * ``initscripts/`` - Python scripts which set up the interpreter to run from
    frozen code, then load the code from the zip file and set it running.
  * ``cli.py`` - The code behind the :doc:`cxfreeze script <../script>`.
  * ``common.py`` - Common utility functions shared between cx_Freeze modules.
  * ``dep_parser.py`` - Implements `Parser` interface to create an abstraction
    to parse binary files.
  * ``exception.py`` - Internal exception classes.
  * ``executable.py`` - Module for the Executable base class.
  * ``finder.py`` - Module Finder - discovers what modules are required by the
    code.
  * ``freezer.py`` - The core class for freezing scripts into executables.
  * ``module.py`` - Base class for Module and ConstantsModule.
  * ``winmsvcr.py`` - DLL list of MSVC runtimes.
  * ``winversioninfo.py`` - Module for the VersionInfo base class.

* ``doc/`` - The Sphinx documentation.
* ``samples/`` - Examples of using cx_Freeze with a number of common modules.
* ``source/`` (C files)

  * ``bases/`` - The source of the base executables which are used to launch
    your Python applications. Different bases serve for different types of
    application on Windows (GUI, console application or service). The base
    executable calls the initscript, which in turn calls the user's code.
  * ``util.c`` - Compiled functions for cx_Freeze itself. Compiles to
    :file:`cx_Freeze.util`. Functions are used only on Windows.
