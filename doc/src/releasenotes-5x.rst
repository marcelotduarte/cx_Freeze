5.x releases and older
######################


Version 5.1.1 (December 2017)
-----------------------------

#)  Correct code used to identify the directory in which the library and its
    zip file are located (:issue:`324`, :issue:`325`).
#)  Ensure that the pythoncom and pywintypes DLLs are found in the lib
    directory, not in the base directory (:issue:`332`).
#)  Copy dependent files to the same directory as the file it depends on, not
    the root directory; also add a sample for PyQt5 to demonstrate its correct
    use (:issue:`328`).


Version 5.1 (November 2017)
---------------------------

#)  Use fixed library location on all platforms; should correct the error
    "no module named __startup__" (:pull:`286`).
#)  Correct sqlite3 hook for use in Python 2.7 (:pull:`272`).
#)  Correct usage of scipy.lib (:pull:`281`).
#)  Correct handling of __path__ attribute in module (:pull:`295`).
#)  Fix gevent bug #42 (:pull:`301`).
#)  Droppped support for Python 3.4.


Version 5.0.2 (May 2017)
------------------------

#) Correct handling of import in child thread (:pull:`245`)
#) Correct handling of "dis" module with Python 3.5.1 (:issue:`225`)
#) Correct handling of "multiprocess.process" module (:issue:`230`)
#) Correct attempt to assign variable to an empty list (:pull:`260`)
#) Improved README (:pull:`235`, :pull:`236`)
#) Add hook for pythonnet package (:pull:`251`)
#) Add hook for sqlite3 and improve win32file hook (:pull:`261`)
#) Add FAQ entry (:pull:`267`)


Version 5.0.1 (January 2017)
----------------------------

#) Added support for Python 3.6.
#) Corrected hooks for the pythoncom and pywintypes modules.
#) Use realpath() to get the absolute path of the executable; this resolves
   symbolic links and ensures that changing the path before all imports are
   complete does not result in the executable being unable to find modules.
#) Correct issue with usage of 'if __main__ == "__main__"'. (`Issue #211`_)
#) Correct handling of the zip_include_packages option. (`Issue #208`_)
#) Correct logic regarding importing of submodules. (`Issue #219`_)

.. _Issue #208: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/208
.. _Issue #211: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/211
.. _Issue #219: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/219


Version 5.0 (November 2016)
---------------------------

.. note:: This version supports Python 2.7 and above.

#) Added support for Python 3.5.
#) Switched from using C compiled frozen modules which embed part of the
   standard library to using the default named zip file and library file
   locations. This eliminates the need to recompile cx_Freeze for each new
   Python version as no parts of the standard library are included in the
   installation now. This also implies that appending a zip file to the
   executable is no longer supported since the standard name and location are
   used.
#) Removed unnecessary options and parameters from cx_Freeze.
   (`PR #60`_, `PR #67`_)
#) Added support for Win32Service base with Python 3.x. (`PR #49`_)
#) Add __version__ as an alias to version. (`PR #65`_)
#) Updated hooks for PyQt, h5py. (`PR #68`_, `PR #64`_, `PR #70`_)
#) Set copyDependentFiles = True for include files. (`PR #66`_)
#) Reallow including modules with non-identifier names. (`PR #79`_)
#) Fix missing space in Windows installer. (`PR #81`_)
#) Use pattern "not in string" isntead of "string.find(pattern)" (`PR #76`_)
#) Fix --add-to-path writing to the per-user instead of system environment
   (`PR #86`_)
#) Fix documentation (`PR #77`_, `PR #78`_)
#) Do not import excluded submodules. (`PR #89`_)
#) Correct distribution files for bdist_msi (`PR #95`_)
#) Allow proper handling of Unicode command line parameters under Windows
   (`PR #87`_)
#) Add pyzmq hook (`PR #63`_)
#) Add copyright and trademarks to version information (`PR #94`_)
#) Fix compilation on Ubuntu (`Issue #32`_)
#) Set defaults in class directly, rather than as defaults in the function
   signature. (`Issue #185`_)
#) Correct relative import of builtin module (cx_Freeze was incorrectly
   considering it an extension found within a package). (`Issue #127`_)
#) Ensure that included files are added relative to the executable, not to the
   location of the zip file. (`Issue #183`_)
#) Prevent infinite loop while using cx_Freeze installed in a prefix.
   (`Issue #204`_)
#) Added support for storing packages in the file system instead of in the zip
   file. There are a number of packages that assume that they are found in the
   file system and if found in a zip file instead produce strange errors. The
   default is now to store packages in the file system but a method is
   available to place packages in the zip file if they are known to behave
   properly when placed there. (`Issue #73`_)
#) Added support for untranslatable characters on Windows in the path where a
   frozen executable is located. (`Issue #29`_)
#) Use volume label to name the DMG file (`Issue #97`_)
#) Significantly simplified startup code.
#) Added logging statements for improved debugging.
#) Updated samples to handle recent updates to packages.
#) Avoid infinite loop for deferred imports which are cycles of one another.

.. _Issue #29: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/29
.. _Issue #32: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/32
.. _Issue #73: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/73
.. _Issue #97: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/97
.. _Issue #127: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/127
.. _Issue #183: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/183
.. _Issue #185: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/185
.. _Issue #204: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/204
.. _PR #49: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/49
.. _PR #60: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/60
.. _PR #63: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/63
.. _PR #64: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/64
.. _PR #65: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/65
.. _PR #66: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/66
.. _PR #67: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/67
.. _PR #68: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/68
.. _PR #70: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/70
.. _PR #76: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/76
.. _PR #77: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/77
.. _PR #78: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/78
.. _PR #79: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/79
.. _PR #81: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/81
.. _PR #86: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/86
.. _PR #87: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/87
.. _PR #89: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/89
.. _PR #94: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/94
.. _PR #95: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/95


Version 4.3.4 (December 2014)
-----------------------------

.. note:: This version supports Python 2.6 and above.

#) Rebuilt for Python 3.4.2. Dropped support for Python versions less than 2.6.
#) Correct stale comment. (`PR #50`_)
#) Fix processing path specs from config when targets are not explicit.
   (`PR #53`_)
#) Tweaks to improve compiling with MSVC 10 (2010) on Windows. (`PR #54`_)
#) Added support for using the --deep and --resource-rules options when code
   signing through cx_Freeze on OS X. (`PR #55`_)
#) Catch error if GetDependentFiles() is called on a non-library (`PR #56`_)
#) Added FAQ entry on single file executables (`PR #58`_)
#) Only look one level deep for implicit relative imports (`PR #59`_)
#) Removed statement that was filtering out the ntpath module. (`PR #74`_)

.. _PR #50: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/50
.. _PR #53: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/53
.. _PR #54: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/54
.. _PR #55: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/55
.. _PR #56: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/56
.. _PR #58: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/58
.. _PR #59: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/59
.. _PR #74: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/74


Version 4.3.3 (May 2014)
------------------------

.. note:: This version supports Python 2.4 and above.

#) Added support for release version of 3.4 (`PR #47`_, `PR #48`_)
#) Added support for code signing in bdist_mac (`PR #40`_)
#) Added custom Info.plist and Framework suport to bdist_mac (`PR #33`_)
#) Added support for resolving dependencies on OS X where paths are relative
   (`PR #35`_)
#) Added hook for QtWebKit module (`PR #36`_)
#) Added support for finding packages inside zip files (`PR #38`_)
#) Ensure that syntax errors in code do not prevent freezing from taking place
   but simply ignore those modules (`PR #44`_, `PR #45`_)
#) Init scripts now use code that works in both Python 2 and 3 (`PR #42`_)
#) Simplify service sample (`PR #41`_)
#) Fix documentation for bdist_dmg (`PR #34`_)
#) All options that accept multiple values are split on commas as documented
   (`PR #39`_)
#) Truncated names in Python tracebacks (`Issue #52`_)
#) install_name_tool doesn't set relative paths for files added using
   include_files option (`Issue #31`_)

.. _Issue #31: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/31
.. _Issue #52: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/52
.. _PR #33: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/33
.. _PR #34: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/34
.. _PR #35: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/35
.. _PR #36: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/36
.. _PR #38: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/38
.. _PR #39: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/39
.. _PR #40: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/40
.. _PR #41: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/41
.. _PR #42: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/42
.. _PR #44: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/44
.. _PR #45: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/45
.. _PR #47: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/47
.. _PR #48: https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/48


Version 4.3.2 (October 2013)
----------------------------

#) Added support for Python 3.4.
#) Added hooks for PyQt4, PyQt5 and PySide to handle their plugins.
#) Added support for creating a shortcut/alias to the Applications directory
   within distributed DMG files for OS X.
#) Improve missing modules output.
#) Avoid polluting the extension module namespace when using the bootstrap
   module to load the extension.
#) Added support for using setuptools and pip if such tools are available.
#) Added first tests; nose and mock are required to run them.
#) Remove --bundle-iconfile in favor of --iconfile as a more generic method
   of including the icon for bdist_mac.
#) Documentation improved and FAQ added.
#) Converted samples to follow PEP 8.
#) cxfreeze-quickstart failed if the default base was not used
#) scripts frozen with Python 3 fail with an ImportError trying to import the
   re module
#) fix bug where after a first attempt to find a module failed, the second
   attempt would erroneously succeed
#) stop attempting to load a module by a name that is not a valid Python
   identifier


Version 4.3.1 (November 2012)
-----------------------------

.. note:: This version supports Python 2.4 and above. If you need Python 2.3
   support, please use cx_Freeze 4.2.3.

#) Added support for the final release of Python 3.3.
#) Added support for copying the MSVC runtime DLLs and manifest if desired by
   using the --include-msvcr switch. Thanks to Almar Klein for the initial
   patch.
#) Clarified the documentation on the --replace-paths option. Thanks to Thomas
   Kluyver for the patch.
#) Producing a Mac distribution failed with a variable reference.
#) Freezing a script using PyQt on a Mac failed with a type error.
#) Version number reported was incorrect. (`Issue #7`_)
#) Correct paths during installation on Windows. (`Issue #11`_)

.. _Issue #7: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/7
.. _Issue #11: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/11


Version 4.3 (July 2012)
-----------------------

.. note:: This version supports Python 2.4 and above. If you need Python 2.3
   support, please use cx_Freeze 4.2.3.

#) Added options to build Mac OS X application bundles and DMG packages using
   ``bdist_mac`` and ``bdist_dmg`` distutils commands. Written by Rob Reilink.
#) The documentation is now using Sphinx, and is `available on ReadTheDocs.org
   <https://cx_freeze.readthedocs.org/en/latest/index.html>`_.
#) Added support for Python 3.3 which uses a different compiled file format
   than earlier versions of Python.
#) Added support for Windows services which start automatically and which are
   capable of monitoring changes in sessions such as lock and unlock.
#) New ``cxfreeze-quickstart`` wizard to create a basic ``setup.py`` file.
   Initially written by Thomas Kluyver.
#) Included files under their original name can now be passed to
   ``include_files`` as a tuple with an empty second element. Written by
   r_haritonov.
#) File inclusions/exclusions can now be specified using a full path, or a
   shared library name with a version number suffix.
#) Messagebox display of certain errors in Windows GUI applications with Python
   3.
#) Running Windows GUI applications in a path containing non-ASCII characters.
#) Calculate the correct filename for the Python shared library in Python 3.2.
#) Including a package would not include the packages within that package, only
   the modules within that package. (`Issue #3`_)

.. _Issue #3: https://bitbucket.org/anthony_tuininga/cx_freeze/issues/3


Version 4.2.3 (March 2011)
--------------------------

#) Added support for Python 3.2.
#) Added hook for datetime module which implicitly imports the time module.
#) Fixed hook for tkinter in Python 3.x.
#) Always include the zlib module since the zipimport module requires it,
   even when compression is not taking place.
#) Added sample for a tkinter application.


Version 4.2.2 (December 2010)
-----------------------------

#) Added support for namespace packages which are loaded implicitly upon
   startup by injection into sys.modules.
#) Added support for a Zope sample which makes use of namespace packages.
#) Use the Microsoft compiler on Windows for Python 2.6 and up as some
   strange behaviors were identified with Python 2.7 when compiled using
   mingw32.
#) Eliminate warning about -mwindows when using the Microsoft compiler for
   building the Win32GUI base executable.
#) Added support for creating version resources on Windows.
#) Ensure that modules that are not truly required for bootstrapping are not
   included in the frozen modules compiled in to the executable; otherwise,
   some packages and modules (such as the logging package) cannot be found at
   runtime. This problem only seems to be present in Python 2.7.1 but it is a
   good improvement for earlier releases of Python as well.
#) Added support for setting the description for Windows services.
#) Added hook for using the widget plugins which are part of the PyQt4.uic
   package.
#) Added additional hooks to remove spurious errors about missing modules
   and to force inclusion of implicitly imported modules (twitter module
   and additional submodules of the PyQt4 package).
#) Fixed support for installing frozen executables under Python 3.x on
   Windows.
#) Removed optional import of setuptools which is not a complete drop-in
   replacement for distutils and if found, replaces distutils with itself,
   resulting in some distutils features not being available; for those who
   require or prefer the use of setuptools, import it in your setup.py.


Version 4.2.1 (October 2010)
----------------------------

#) Added support for specifying bin_path_includes and bin_path_excludes in
   setup scripts.
#) Added support for compiling Windows services with the Microsoft compiler
   and building for 64-bit Windows.
#) When installing Windows services, use the full path for both the executable
   and the configuration file if specified.
#) Eliminate duplicate files for each possible version of Python when building
   MSI packages for Python 2.7.
#) Fix declaration of namespace packages.
#) Fix check for cx_Logging import library directory.
#) Added hooks for the python-Xlib package.
#) Added hooks to ignore the _scproxy module when not on the Mac platform and
   the win32gui and pyHook modules on platforms other than Windows.
#) When copying files, copy the stat() information as well as was done in
   earlier versions of cx_Freeze.
#) Added documentation for the shortcutName and shortcutDir parameters for
   creating an executable.


Version 4.2 (July 2010)
-----------------------

#) Added support for Python 2.7.
#) Improved support for Python 3.x.
#) Improved support for Mac OS X based on feedback from some Mac users.
#) Improved hooks for the following modules: postgresql, matplotlib, twisted,
   zope, PyQt4.
#) Improved packaging of MSI files by enabling support for creating shortcuts
   for the executables, for specifying the initial target directory and for
   adding other arbitrary configuration to the MSI.
#) Added support for namespace packages such as those distributed for zope.
#) The name of the generated MSI packages now includes the architecture in
   order to differentiate between 32-bit and 64-bit builds.
#) Removed use of LINKFORSHARED on the Mac which is not necessary and for
   Python 2.6 at least causes an error to be raised.
#) Turn off filename globbing on Windows as requested by Craig McQueen.
#) Fixed bug that prevented hooks from successfully including files in the
   build (as is done for the matplotlib sample).
#) Fixed bug that prevented submodules from being included in the build if the
   format of the import statement was from . import <name>.
#) Reverted bug fix for threading shutdown support which has been fixed
   differently and is no longer required in Python 2.6.5 and up (in fact an
   error is raised if the threading module is used in a frozen executable and
   this code is retained).
#) Fixed bug which resulted in attempts to compile .pyc and .pyo files from
   the initscripts directory.
#) Fixed selection of "Program Files" directory on Windows in 64-bit MSI
   packages built by cx_Freeze.


Version 4.1.2 (January 2010)
----------------------------

#) Fix bug that caused the util extension to be named improperly.
#) Fix bug that prevented freezing from taking place if a packaged submodule
   was missing.
#) Fix bug that prevented freezing from taking place in Python 3.x if the
   encoding of the source file wasn't compatible with the encoding of the
   terminal performing the freeze.
#) Fix bug that caused the base modules to be included in the library.zip as
   well as the base executables.


Version 4.1.1 (December 2009)
-----------------------------

#) Added support for Python 3.1.
#) Added support for 64-bit Windows.
#) Ensured that setlocale() is called prior to manipulating file names so
   that names that are not encoded in ASCII can still be used.
#) Fixed bug that caused the Python shared library to be ignored and the
   static library to be required or a symbolic link to the shared library
   created manually.
#) Added support for renaming attributes upon import and other less
   frequently used idioms in order to avoid as much as possible spurious
   errors about modules not being found.
#) Force inclusion of the traceback module in order to ensure that errors are
   reported in a reasonable fashion.
#) Improved support for the execution of ldd on the Solaris platform as
   suggested by Eric Brunel.
#) Added sample for the PyQt4 package and improved hooks for that package.
#) Enhanced hooks further in order to perform hidden imports and avoid errors
   about missing modules for several additional commonly used packages and
   modules.
#) Readded support for the zip include option.
#) Avoid the error about digest mismatch when installing RPMs by modifying
   the spec files built with cx_Freeze.
#) Ensure that manifest.txt is included in the source distribution.


Version 4.1 (July 2009)
-----------------------

#) Added support for Python 3.x.
#) Added support for services on Windows.
#) Added command line option --silent (-s) as requested by Todd Templeton.
   This option turns off all normal output including the report of the modules
   that are included.
#) Added command line option --icon as requested by Tom Brown.
#) Ensure that Py_Finalize() is called even when exceptions take place so that
   any finalization (such as __del__ calls) are made prior to the executable
   terminating.
#) Ensured that empty directories are created as needed in the target as
   requested by Clemens Hermann.
#) The encodings package and any other modules required to bootstrap the
   Python runtime are now automatically included in the frozen executable.
#) Ensured that if a target name is specified, that the module name in the zip
   file is also changed. Thanks to Clemens Hermann for the initial patch.
#) Enabled support for compiling on 64-bit Windows.
#) If an import error occurs during the load phase, treat that as a bad module
   as well. Thanks to Tony Meyer for pointing this out.
#) As suggested by Todd Templeton, ensured that the include files list is
   copied, not simply referenced so that further uses of the list do not
   inadvertently cause side effects.
#) As suggested by Todd Templeton, zip files are now closed properly in order
   to avoid potential corruption.
#) As suggested by Todd Templeton, data files are no longer copied when the
   copy dependent files flag is cleared.
#) Enabled better support of setup.py scripts that call other setup.py
   scripts such as the ones used by cx_OracleTools and cx_OracleDBATools.
#) On Solaris, ldd outputs tabs instead of spaces so expand them first before
   looking for the separator. Thanks to Eric Brunel for reporting this and
   providing the solution.
#) On Windows, exclude the Windows directory and the side-by-side installation
   directory when determining DLLs to copy since these are generally
   considered part of the system.
#) On Windows, use %* rather than the separated arguments in the generated
   batch file in order to avoid problems with the very limited argument
   processor used by the command processor.
#) For the Win32GUI base executable, add support for specifying the caption to
   use when displaying error messages.
#) For the Win32GUI base executable, add support for calling the excepthook
   for top level exceptions if one has been specified.
#) On Windows, ensure that the MSI packages that are built are per-machine
   by default as otherwise strange things can happen.
#) Fixed bug in the calling of readlink() that would occasionally result in
   strange behavior or segmentation faults.
#) Duplicate warnings about libraries not found by ldd are now suppressed.
#) Tweaked hooks for a number of modules based on feedback from others or
   personal experience.


Version 4.0.1 (October 2008)
----------------------------

#) Added support for Python 2.6. On Windows a manifest file is now required
   because of the switch to using the new Microsoft C runtime.
#) Ensure that hooks are run for builtin modules.


Version 4.0 (September 2008)
----------------------------

#) Added support for copying files to the target directory.
#) Added support for a hook that runs when a module is missing.
#) Added support for binary path includes as well as excludes; use sequences
   rather than dictionaries as a more convenient API; exclude the standard
   locations for 32-bit and 64-bit libaries in multi-architecture systems.
#) Added support for searching zip files (egg files) for modules.
#) Added support for handling system exit exceptions similarly to what Python
   does itself as requested by Sylvain.
#) Added code to wait for threads to shut down like the normal Python
   interpreter does. Thanks to Mariano Disanzo for discovering this
   discrepancy.
#) Hooks added or modified based on feedback from many people.
#) Don't include the version name in the display name of the MSI.
#) Use the OS dependent path normalization routines rather than simply use the
   lowercase value as on Unix case is important; thanks to Artie Eoff for
   pointing this out.
#) Include a version attribute in the cx_Freeze package and display it in the
   output for the --version option to the script.
#) Include build instructions as requested by Norbert Sebok.
#) Add support for copying files when modules are included which require data
   files to operate properly; add support for copying the necessary files for
   the Tkinter and matplotlib modules.
#) Handle deferred imports recursively as needed; ensure that from lists do
   not automatically indicate that they are part of the module or the deferred
   import processing doesn't actually work!
#) Handle the situation where a module imports everything from a package and
   the __all__ variable has been defined but the package has not actually
   imported everything in the __all__ variable during initialization.
#) Modified license text to more closely match the Python Software Foundation
   license as was intended.
#) Added sample script for freezing an application using matplotlib.
#) Renamed freeze to cxfreeze to avoid conflict with another package that uses
   that executable as requested by Siegfried Gevatter.


Version 4.0b1 (September 2007)
------------------------------

#) Added support for placing modules in library.zip or in a separate zip file
   for each executable that is produced.
#) Added support for copying binary dependent files (DLLs and shared
   libraries)
#) Added support for including all submodules in a package
#) Added support for including icons in Windows executables
#) Added support for constants module which can be used for determining
   certain build constants at runtime
#) Added support for relative imports available in Python 2.5 and up
#) Added support for building Windows installers (Python 2.5 and up) and
   RPM packages
#) Added support for distutils configuration scripts
#) Added support for hooks which can force inclusion or exclusion of modules
   when certain modules are included
#) Added documentation and samples
#) Added setup.py for building the cx_Freeze package instead of a script
   used to build only the frozen bases
#) FreezePython renamed to a script called freeze in the Python distribution
#) On Linux and other platforms that support it set LD_RUN_PATH to include
   the directory in which the executable is located


Version 3.0.3 (July 2006)
-------------------------

#) In Common.c, used MAXPATHLEN defined in the Python OS independent include
   file rather than the PATH_MAX define which is OS dependent and is not
   available on IRIX as noted by Andrew Jones.
#) In the initscript ConsoleSetLibPath.py, added lines from initscript
   Console.py that should have been there since the only difference between
   that script and this one is the automatic re-execution of the executable.
#) Added an explicit "import encodings" to the initscripts in order to handle
   Unicode encodings a little better. Thanks to Ralf Schmitt for pointing out
   the problem and its solution.
#) Generated a meaningful name for the extension loader script so that it is
   clear which particular extension module is being loaded when an exception
   is being raised.
#) In MakeFrozenBases.py, use distutils to figure out a few more
   platform-dependent linker flags as suggested by Ralf Schmitt.


Version 3.0.2 (December 2005)
-----------------------------

#) Add support for compressing the byte code in the zip files that are
   produced.
#) Add better support for the win32com package as requested by Barry Scott.
#) Prevent deletion of target file if it happens to be identical to the
   source file.
#) Include additional flags for local modifications to a Python build as
   suggested by Benjamin Rutt.
#) Expanded instructions for building cx_Freeze from source based on a
   suggestion from Gregg Lind.
#) Fix typo in help string.


Version 3.0.1 (December 2004)
-----------------------------

#) Added option --default-path which is used to specify the path used when
   finding modules. This is particularly useful when performing cross
   compilations (such as for building a frozen executable for Windows CE).
#) Added option --shared-lib-name which can be used to specify the name of
   the shared library (DLL) implementing the Python runtime that is required
   for the frozen executable to work. This option is also particularly useful
   when cross compiling since the normal method for determining this
   information cannot be used.
#) Added option --zip-include which allows for additional files to be added
   to the zip file that contains the modules that implement the Python
   script. Thanks to Barray Warsaw for providing the initial patch.
#) Added support for handling read-only files properly. Thanks to Peter
   Grayson for pointing out the problem and providing a solution.
#) Added support for a frozen executable to be a symbolic link. Thanks to
   Robert Kiendl for providing the initial patch.
#) Enhanced the support for running a frozen executable that uses an existing
   Python installation to locate modules it requires. This is primarily of
   use for embedding Python where the interface is C but the ability to run
   from source is still desired.
#) Modified the documentation to indicate that building from source on
   Windows currently requires the mingw compiler (https://www.mingw.org).
#) Workaround the problem in Python 2.3 (fixed in Python 2.4) which causes a
   broken module to be left in sys.modules if an ImportError takes place
   during the execution of the code in that module. Thanks to Roger Binns
   for pointing this out.


Version 3.0 (September 2004)
----------------------------

#) Ensure that ldd is only run on extension modules.
#) Allow for using a compiler other than gcc for building the frozen base
   executables by setting the environment variable CC.
#) Ensure that the import lock is not held while executing the main script;
   otherwise, attempts to import a module within a thread will hang that
   thread as noted by Roger Binns.
#) Added support for replacing the paths in all frozen modules with something
   else (so that for example the path of the machine on which the freezing
   was done is not displayed in tracebacks)


Version 3.0 beta3 (September 2004)
----------------------------------

#) Explicitly include the warnings module so that at runtime warnings are
   suppressed as when running Python normally.
#) Improve the extension loader so that an ImportError is raised when the
   dynamic module is not located; otherwise an error about missing attributes
   is raised instead.
#) Extension loaders are only created when copying dependencies since the
   normal module should be loadable in the situation where a Python
   installation is available.
#) Added support for Python 2.4.
#) Fixed the dependency checking for wxPython to be a little more
   intelligent.


Version 3.0 beta2 (July 2004)
-----------------------------

#) Fix issues with locating the initscripts and bases relative to the
   directory in which the executable was started.
#) Added new base executable ConsoleKeepPath which is used when an existing
   Python installation is required (such as for FreezePython itself).
#) Forced the existence of a Python installation to be ignored when using the
   standard Console base executable.
#) Remove the existing file when copying dependent files; otherwise, an error
   is raised when attempting to overwrite read-only files.
#) Added option -O (or -OO) to FreezePython to set the optimization used when
   generating bytecode.


Version 3.0 beta1 (June 2004)
-----------------------------

#) cx_Freeze now requires Python 2.3 or higher since it takes advantage of
   the ability of Python 2.3 and higher to import modules from zip files.
   This makes the freezing process considerably simpler and also allows for
   the execution of multiple frozen packages (such as found in COM servers or
   shared libraries) without requiring modification to the Python modules.
#) All external dependencies have been removed. cx_Freeze now only requires
   a standard Python distribution to do its work.
#) Added the ability to define the initialization scripts that cx_Freeze uses
   on startup of the frozen program. Previously, these scripts were written
   in C and could not easily be changed; now they are written in Python and
   can be found in the initscripts directory (and chosen with the
   new --init-script option to FreezePython).
#) The base executable ConsoleSetLibPath has been removed and replaced with
   the initscript ConsoleSetLibPath.
#) Removed base executables for Win32 services and Win32 COM servers. This
   functionality will be restored in the future but it is not currently in a
   state that is ready for release. If this functionality is required, please
   use py2exe or contact me for my work in progress.
#) The attribute sys.frozen is now set so that more recent pywin32 modules
   work as expected when frozen.
#) Added option --include-path to FreezePython to allow overriding of
   sys.path without modifying the environment variable PYTHONPATH.
#) Added option --target-dir/--install-dir to specify the directory in which
   the frozen executable and its dependencies will be placed.
#) Removed the option --shared-lib since it was used for building shared
   libraries and can be managed with the initscript SharedLib.py.
#) MakeFrozenBases.py now checks the platform specific include directory as
   requested by Michael Partridge.


Version 2.2 (August 2003)
-------------------------

#) Add option (--ext-list-file) to FreezePython to write the list of
   extensions copied to the installation directory to a file. This option is
   useful in cases where multiple builds are performed into the same
   installation directory.
#) Pass the arguments on the command line through to Win32 GUI applications.
   Thanks to Michael Porter for pointing this out.
#) Link directly against the python DLL when building the frozen bases on
   Windows, thus eliminating the need for building an import library.
#) Force sys.path to include the directory in which the script to be frozen
   is found.
#) Make sure that the installation directory exists before attempting to
   copy the target binary into it.
#) The Win32GUI base has been modified to display fatal errors in message
   boxes, rather than printing errors to stderr, since on Windows the
   standard file IO handles are all closed.


Version 2.1 (July 2003)
-----------------------

#) Remove dependency on Python 2.2. Thanks to Paul Moore for not only
   pointing it out but providing patches.
#) Set up the list of frozen modules in advance, rather than doing it after
   Python is initialized so that implicit imports done by Python can be
   satisfied. The bug in Python 2.3 that demonstrated this issue has been
   fixed in the first release candidate. Thanks to Thomas Heller for pointing
   out the obvious in this instance!
#) Added additional base executable (ConsoleSetLibPath) to support setting
   the LD_LIBRARY_PATH variable on Unix platforms and restarting the
   executable to put the new setting into effect. This is primarily of use
   in distributing wxPython applications on Unix where the shared library
   has an embedded RPATH value which can cause problems.
#) Small improvements of documentation based on feedback from several people.
#) Print information about the files written or copied during the freezing
   process.
#) Do not copy extensions when freezing if the path is being overridden since
   it is expected that a full Python installation is available to the target
   users of the frozen binary.
#) Provide meaningful error message when the wxPython library cannot be
   found during the freezing process.


Version 2.0
-----------

#) Added support for in process (DLL) COM servers using PythonCOM.
#) Ensured that the frozen flag is set prior to determining the full path for
   the program in order to avoid warnings about Python not being found on
   some platforms.
#) Added include file and resource file to the source tree to avoid the
   dependency on the Wine message compiler for Win32 builds.
#) Dropped the option --copy-extensions; this now happens automatically since
   the resulting binary is useless without them.
#) Added a sample for building a Win32 service.
#) Make use of improved modules from Python 2.3 (which function under 2.2)


Version 1.1
-----------

#) Fixed import error with C extensions in packages; thanks to Thomas Heller
   for pointing out the solution to this problem.
#) Added options to FreezePython to allow for the inclusion of modules which
   will not be found by the module finder (--include-modules) and the
   exclusion of modules which will be found by the module finder but should
   not be included (--exclude-modules).
#) Fixed typo in README.txt.
