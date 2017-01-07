
Release notes
=============

5.x releases
############

Development version
-------------------

.. note:: This version supports Python 2.7 and above.


Version 5.0.1 (January 2017)
----------------------------

1)  Added support for Python 3.6.

2)  Corrected hooks for the pythoncom and pywintypes modules.

3)  Use realpath() to get the absolute path of the executable; this resolves
    symbolic links and ensures that changing the path before all imports are
    complete does not result in the executable being unable to find modules.

4)  Correct issue with usage of 'if __main__ == "__main__"'.
    (`Issue #211 <https://bitbucket.org/anthony_tuininga/cx_freeze/issues/211>`_)

5)  Correct handling of the zip_include_packages option.
    (`Issue #208 <https://bitbucket.org/anthony_tuininga/cx_freeze/issues/208>`_)

6)  Correct logic regarding importing of submodules.
    (`Issue #219 <https://bitbucket.org/anthony_tuininga/cx_freeze/issues/219>`_)


Version 5.0 (November 2016)
---------------------------

.. note:: This version supports Python 2.7 and above.

1)  Added support for Python 3.5.

2)  Switched from using C compiled frozen modules which embed part of the
    standard library to using the default named zip file and library file
    locations. This eliminates the need to recompile cx_Freeze for each new
    Python version as no parts of the standard library are included in the
    installation now. This also implies that appending a zip file to the
    executable is no longer supported since the standard name and location are
    used.

3)  Removed unnecessary options and parameters from cx_Freeze.
    (`PR #60 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/60>`_)
    (`PR #67 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/67>`_)

4)  Added support for Win32Service base with Python 3.x.
    (`PR #49 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/49>`_)

5)  Add __version__ as an alias to version.
    (`PR #65 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/65>`_)

6)  Updated hooks for PyQt, h5py.
    (`PR #68 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/68>`_)
    (`PR #64 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/64>`_)
    (`PR #70 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/70>`_)

7)  Set copyDependentFiles = True for include files.
    (`PR #66 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/66>`_)

8)  Reallow including modules with non-identifier names.
    (`PR #79 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/79>`_)

9)  Fix missing space in Windows installer.
    (`PR #81 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/81>`_)

10) Use pattern "not in string" isntead of "string.find(pattern)"
    (`PR #76 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/76>`_)

11) Fix --add-to-path writing to the per-user instead of system environment
    (`PR #86 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/86>`_)

12) Fix documentation
    (`PR #77 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/77>`_)
    (`PR #78 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/78>`_)

13) Do not import excluded submodules.
    (`PR #89 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/89>`_)

14) Correct distribution files for bdist_msi
    (`PR #95 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/95>`_)

15) Allow proper handling of Unicode command line parameters under Windows
    (`PR #87 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/87>`_)

16) Add pyzmq hook
    (`PR #63 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/63>`_)

17) Add copyright and trademarks to version information
    (`PR #94 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/94>`_)

18) Fix compilation on Ubuntu
    (`Issue #52 <https://bitbucket.org/anthony_tuininga/cx_freeze/issues/32>`_)

19) Set defaults in class directly, rather than as defaults in the function
    signature.
    (`Issue #185 <https://bitbucket.org/anthony_tuininga/cx_freeze/issues/185>`_)

20) Correct relative import of builtin module (cx_Freeze was incorrectly
    considering it an extension found within a package).
    (`Issue #127 <https://bitbucket.org/anthony_tuininga/cx_freeze/issues/127>`_)

21) Ensure that included files are added relative to the executable, not to the
    location of the zip file.
    (`Issue #183 <https://bitbucket.org/anthony_tuininga/cx_freeze/issues/183>`_)

22) Prevent infinite loop while using cx_Freeze installed in a prefix.
    (`Issue #204 <https://bitbucket.org/anthony_tuininga/cx_freeze/issues/204>`_)

23) Added support for storing packages in the file system instead of in the zip
    file. There are a number of packages that assume that they are found in the
    file system and if found in a zip file instead produce strange errors. The
    default is now to store packages in the file system but a method is
    available to place packages in the zip file if they are known to behave
    properly when placed there.
    (`Issue #73 <https://bitbucket.org/anthony_tuininga/cx_freeze/issues/73>`_)

24) Added support for untranslatable characters on Windows in the path where a
    frozen executable is located.
    (`Issue #29 <https://bitbucket.org/anthony_tuininga/cx_freeze/issues/29>`_)

25) Use volume label to name the DMG file
    (`Issue #97 <https://bitbucket.org/anthony_tuininga/cx_freeze/issues/97>`_)

26) Significantly simplified startup code.

27) Added logging statements for improved debugging.

28) Updated samples to handle recent updates to packages.

29) Avoid infinite loop for deferred imports which are cycles of one another.


Version 4.3.4 (December 2014)
-----------------------------

.. note:: This version supports Python 2.6 and above.

1)  Rebuilt for Python 3.4.2. Dropped support for Python versions less than 2.6.

2)  Correct stale comment.
    (`PR #50 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/50>`_)

3)  Fix processing path specs from config when targets are not explicit.
    (`PR #53 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/53>`_)

4)  Tweaks to improve compiling with MSVC 10 (2010) on Windows.
    (`PR #54 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/54>`_)

5)  Added support for using the --deep and --resource-rules options when code
    signing through cx_Freeze on OS X.
    (`PR #55 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/55>`_)

6)  Catch error if GetDependentFiles() is called on a non-library
    (`PR #56 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/56>`_)

7)  Added FAQ entry on single file executables
    (`PR #58 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/58>`_)

8)  Only look one level deep for implicit relative imports
    (`PR #59 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/59>`_)

9)  Removed statement that was filtering out the ntpath module.
    (`PR #74 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/74>`_)


Version 4.3.3 (May 2014)
------------------------

.. note:: This version supports Python 2.4 and above.

1)  Added support for release version of 3.4
    (`PR #47 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/47>`_)
    (`PR #48 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/48>`_)

2)  Added support for code signing in bdist_mac
    (`PR #40 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/40>`_)
3)  Added custom Info.plist and Framework suport to bdist_mac
    (`PR #33 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/33>`_)
4)  Added support for resolving dependencies on OS X where paths are relative
    (`PR #35 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/35>`_)
5)  Added hook for QtWebKit module
    (`PR #36 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/36>`_)
6)  Added support for finding packages inside zip files
    (`PR #38 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/38>`_)
7)  Ensure that syntax errors in code do not prevent freezing from taking place
    but simply ignore those modules
    (`PR #44 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/44>`_)
    (`PR #45 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/45>`_)
8)  Init scripts now use code that works in both Python 2 and 3
    (`PR #42 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/42>`_)
9)  Simplify service sample
    (`PR #41 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/41>`_)
10) Fix documentation for bdist_dmg
    (`PR #34 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/34>`_)
11) All options that accept multiple values are split on commas as documented
    (`PR #39 <https://bitbucket.org/anthony_tuininga/cx_freeze/pull-request/39>`_)

Bugs fixed:

* Truncated names in Python tracebacks
  (`Issue #52 <https://bitbucket.org/anthony_tuininga/cx_freeze/issue/52/truncated-names-in-python-tracebacks-of>`_)
* install_name_tool doesn't set relative paths for files added using
  include_files option 
  (`Issue #31 <https://bitbucket.org/anthony_tuininga/cx_freeze/issue/31/install_name_tool-doesnt-set-relative>`_)


Version 4.3.2 (October 2013)
----------------------------

1) Added support for Python 3.4.
2) Added hooks for PyQt4, PyQt5 and PySide to handle their plugins.
3) Added support for creating a shortcut/alias to the Applications directory
   within distributed DMG files for OS X.
4) Improve missing modules output.
5) Avoid polluting the extension module namespace when using the bootstrap
   module to load the extension.
6) Added support for using setuptools and pip if such tools are available.
7) Added first tests; nose and mock are required to run them.
8) Remove --bundle-iconfile in favor of --iconfile as a more generic method
   of including the icon for bdist_mac.
9) Documentation improved and FAQ added.
10) Converted samples to follow PEP 8.

Bugs fixed:

* cxfreeze-quickstart failed if the default base was not used
* scripts frozen with Python 3 fail with an ImportError trying to import the
  re module
* fix bug where after a first attempt to find a module failed, the second
  attempt would erroneously succeed
* stop attempting to load a module by a name that is not a valid Python
  identifier


Version 4.3.1 (November 2012)
-----------------------------

.. note:: This version supports Python 2.4 and above. If you need Python 2.3
   support, please use cx_Freeze 4.2.3.

1) Added support for the final release of Python 3.3.
2) Added support for copying the MSVC runtime DLLs and manifest if desired by
   using the --include-msvcr switch. Thanks to Almar Klein for the initial
   patch.
3) Clarified the documentation on the --replace-paths option. Thanks to Thomas
   Kluyver for the patch.

Bugs fixed:

* Producing a Mac distribution failed with a variable reference.
* Freezing a script using PyQt on a Mac failed with a type error.
* Version number reported was incorrect.
  (`Issue #7 <https://bitbucket.org/anthony_tuininga/cx_freeze/issue/7/bad-version-for-43>`_)
* Correct paths during installation on Windows.
  (`Issue #11 <https://bitbucket.org/anthony_tuininga/cx_freeze/issue/11/incorrect-paths-in-installed-cxfreeze#comment-2425986>`_)


Version 4.3 (July 2012)
-----------------------

.. note:: This version supports Python 2.4 and above. If you need Python 2.3
   support, please use cx_Freeze 4.2.3.

1) Added options to build Mac OS X application bundles and DMG packages using
   ``bdist_mac`` and ``bdist_dmg`` distutils commands. Written by Rob Reilink.
2) The documentation is now using Sphinx, and is `available on ReadTheDocs.org
   <http://cx_freeze.readthedocs.org/en/latest/index.html>`_.
3) Added support for Python 3.3 which uses a different compiled file format
   than earlier versions of Python.
4) Added support for Windows services which start automatically and which are
   capable of monitoring changes in sessions such as lock and unlock.
5) New ``cxfreeze-quickstart`` wizard to create a basic ``setup.py`` file.
   Initially written by Thomas Kluyver.
6) Included files under their original name can now be passed to
   ``include_files`` as a tuple with an empty second element. Written by
   r_haritonov.
7) File inclusions/exclusions can now be specified using a full path, or a
   shared library name with a version number suffix.

Bugs fixed:

* Messagebox display of certain errors in Windows GUI applications with Python 3.
  (`Issue 3486872 <http://sourceforge.net/tracker/?func=detail&aid=3486872&group_id=84937&atid=574390>`_)
* Running Windows GUI applications in a path containing non-ASCII characters.
* Calculate the correct filename for the Python shared library in Python 3.2.
  (`Issue 3411270 <http://sourceforge.net/tracker/?func=detail&aid=3411270&group_id=84937&atid=574390>`_)
* Including a package would not include the packages within that package, only
  the modules within that package.
  (`Issue #3 <https://bitbucket.org/anthony_tuininga/cx_freeze/issue/3/subpackages-on-windows>`_)


Version 4.2.3 (March 2011)
--------------------------

1) Added support for Python 3.2.
2) Added hook for datetime module which implicitly imports the time module.
3) Fixed hook for tkinter in Python 3.x.
4) Always include the zlib module since the zipimport module requires it,
   even when compression is not taking place.
5) Added sample for a tkinter application.


Version 4.2.2 (December 2010)
-----------------------------

1) Added support for namespace packages which are loaded implicitly upon
   startup by injection into sys.modules.
2) Added support for a Zope sample which makes use of namespace packages.
3) Use the Microsoft compiler on Windows for Python 2.6 and up as some
   strange behaviors were identified with Python 2.7 when compiled using
   mingw32.
4) Eliminate warning about -mwindows when using the Microsoft compiler for
   building the Win32GUI base executable.
5) Added support for creating version resources on Windows.
6) Ensure that modules that are not truly required for bootstrapping are not
   included in the frozen modules compiled in to the executable; otherwise,
   some packages and modules (such as the logging package) cannot be found at
   runtime. This problem only seems to be present in Python 2.7.1 but it is a
   good improvement for earlier releases of Python as well.
7) Added support for setting the description for Windows services.
8) Added hook for using the widget plugins which are part of the PyQt4.uic
   package.
9) Added additional hooks to remove spurious errors about missing modules
   and to force inclusion of implicitly imported modules (twitter module
   and additional submodules of the PyQt4 package).
10) Fixed support for installing frozen executables under Python 3.x on
    Windows.
11) Removed optional import of setuptools which is not a complete drop-in
    replacement for distutils and if found, replaces distutils with itself,
    resulting in some distutils features not being available; for those who
    require or prefer the use of setuptools, import it in your setup.py.


Version 4.2.1 (October 2010)
----------------------------

1) Added support for specifying bin_path_includes and bin_path_excludes in
   setup scripts.
2) Added support for compiling Windows services with the Microsoft compiler
   and building for 64-bit Windows.
3) When installing Windows services, use the full path for both the executable
   and the configuration file if specified.
4) Eliminate duplicate files for each possible version of Python when building
   MSI packages for Python 2.7.
5) Fix declaration of namespace packages.
6) Fix check for cx_Logging import library directory.
7) Added hooks for the python-Xlib package.
8) Added hooks to ignore the _scproxy module when not on the Mac platform and
   the win32gui and pyHook modules on platforms other than Windows.
9) When copying files, copy the stat() information as well as was done in
   earlier versions of cx_Freeze.
10) Added documentation for the shortcutName and shortcutDir parameters for
    creating an executable.


Version 4.2 (July 2010)
-----------------------

1) Added support for Python 2.7.
2) Improved support for Python 3.x.
3) Improved support for Mac OS X based on feedback from some Mac users.
4) Improved hooks for the following modules: postgresql, matplotlib, twisted,
   zope, PyQt4.
5) Improved packaging of MSI files by enabling support for creating shortcuts
   for the executables, for specifying the initial target directory and for
   adding other arbitrary configuration to the MSI.
6) Added support for namespace packages such as those distributed for zope.
7) The name of the generated MSI packages now includes the architecture in
   order to differentiate between 32-bit and 64-bit builds.
8) Removed use of LINKFORSHARED on the Mac which is not necessary and for
   Python 2.6 at least causes an error to be raised.
9) Turn off filename globbing on Windows as requested by Craig McQueen.
10) Fixed bug that prevented hooks from successfully including files in the
    build (as is done for the matplotlib sample).
11) Fixed bug that prevented submodules from being included in the build if the
    format of the import statement was from . import <name>.
12) Reverted bug fix for threading shutdown support which has been fixed
    differently and is no longer required in Python 2.6.5 and up (in fact an
    error is raised if the threading module is used in a frozen executable and
    this code is retained).
13) Fixed bug which resulted in attempts to compile .pyc and .pyo files from
    the initscripts directory.
14) Fixed selection of "Program Files" directory on Windows in 64-bit MSI
    packages built by cx_Freeze.


Version 4.1.2 (January 2010)
----------------------------

1) Fix bug that caused the util extension to be named improperly.
2) Fix bug that prevented freezing from taking place if a packaged submodule
   was missing.
3) Fix bug that prevented freezing from taking place in Python 3.x if the
   encoding of the source file wasn't compatible with the encoding of the
   terminal performing the freeze.
4) Fix bug that caused the base modules to be included in the library.zip as
   well as the base executables.


Version 4.1.1 (December 2009)
-----------------------------

1) Added support for Python 3.1.
2) Added support for 64-bit Windows.
3) Ensured that setlocale() is called prior to manipulating file names so
   that names that are not encoded in ASCII can still be used.
4) Fixed bug that caused the Python shared library to be ignored and the
   static library to be required or a symbolic link to the shared library
   created manually.
5) Added support for renaming attributes upon import and other less
   frequently used idioms in order to avoid as much as possible spurious
   errors about modules not being found.
6) Force inclusion of the traceback module in order to ensure that errors are
   reported in a reasonable fashion.
7) Improved support for the execution of ldd on the Solaris platform as
   suggested by Eric Brunel.
8) Added sample for the PyQt4 package and improved hooks for that package.
9) Enhanced hooks further in order to perform hidden imports and avoid errors
   about missing modules for several additional commonly used packages and
   modules.
10) Readded support for the zip include option.
11) Avoid the error about digest mismatch when installing RPMs by modifying
    the spec files built with cx_Freeze.
12) Ensure that manifest.txt is included in the source distribution.


Version 4.1 (July 2009)
-----------------------

1) Added support for Python 3.x.
2) Added support for services on Windows.
3) Added command line option --silent (-s) as requested by Todd Templeton.
   This option turns off all normal output including the report of the modules
   that are included.
4) Added command line option --icon as requested by Tom Brown.
5) Ensure that Py_Finalize() is called even when exceptions take place so that
   any finalization (such as __del__ calls) are made prior to the executable
   terminating.
6) Ensured that empty directories are created as needed in the target as
   requested by Clemens Hermann.
7) The encodings package and any other modules required to bootstrap the
   Python runtime are now automatically included in the frozen executable.
8) Ensured that if a target name is specified, that the module name in the zip
   file is also changed. Thanks to Clemens Hermann for the initial patch.
9) Enabled support for compiling on 64-bit Windows.
10) If an import error occurs during the load phase, treat that as a bad module
    as well. Thanks to Tony Meyer for pointing this out.
11) As suggested by Todd Templeton, ensured that the include files list is
    copied, not simply referenced so that further uses of the list do not
    inadvertently cause side effects.
12) As suggested by Todd Templeton, zip files are now closed properly in order
    to avoid potential corruption.
13) As suggested by Todd Templeton, data files are no longer copied when the
    copy dependent files flag is cleared.
14) Enabled better support of setup.py scripts that call other setup.py
    scripts such as the ones used by cx_OracleTools and cx_OracleDBATools.
15) On Solaris, ldd outputs tabs instead of spaces so expand them first before
    looking for the separator. Thanks to Eric Brunel for reporting this and
    providing the solution.
16) On Windows, exclude the Windows directory and the side-by-side installation
    directory when determining DLLs to copy since these are generally
    considered part of the system.
17) On Windows, use %* rather than the separated arguments in the generated
    batch file in order to avoid problems with the very limited argument
    processor used by the command processor.
18) For the Win32GUI base executable, add support for specifying the caption to
    use when displaying error messages.
19) For the Win32GUI base executable, add support for calling the excepthook
    for top level exceptions if one has been specified.
20) On Windows, ensure that the MSI packages that are built are per-machine
    by default as otherwise strange things can happen.
21) Fixed bug in the calling of readlink() that would occasionally result in
    strange behavior or segmentation faults.
22) Duplicate warnings about libraries not found by ldd are now suppressed.
23) Tweaked hooks for a number of modules based on feedback from others or
    personal experience.


Version 4.0.1 (October 2008)
----------------------------

1) Added support for Python 2.6. On Windows a manifest file is now required
   because of the switch to using the new Microsoft C runtime.
2) Ensure that hooks are run for builtin modules.


Version 4.0 (September 2008)
----------------------------

1) Added support for copying files to the target directory.
2) Added support for a hook that runs when a module is missing.
3) Added support for binary path includes as well as excludes; use sequences
   rather than dictionaries as a more convenient API; exclude the standard
   locations for 32-bit and 64-bit libaries in multi-architecture systems.
4) Added support for searching zip files (egg files) for modules.
5) Added support for handling system exit exceptions similarly to what Python
   does itself as requested by Sylvain.
6) Added code to wait for threads to shut down like the normal Python
   interpreter does. Thanks to Mariano Disanzo for discovering this
   discrepancy.
7) Hooks added or modified based on feedback from many people.
8) Don't include the version name in the display name of the MSI.
9) Use the OS dependent path normalization routines rather than simply use the
   lowercase value as on Unix case is important; thanks to Artie Eoff for
   pointing this out.
10) Include a version attribute in the cx_Freeze package and display it in the
    output for the --version option to the script.
11) Include build instructions as requested by Norbert Sebok.
12) Add support for copying files when modules are included which require data
    files to operate properly; add support for copying the necessary files for
    the Tkinter and matplotlib modules.
13) Handle deferred imports recursively as needed; ensure that from lists do
    not automatically indicate that they are part of the module or the deferred
    import processing doesn't actually work!
14) Handle the situation where a module imports everything from a package and
    the __all__ variable has been defined but the package has not actually
    imported everything in the __all__ variable during initialization.
15) Modified license text to more closely match the Python Software Foundation
    license as was intended.
16) Added sample script for freezing an application using matplotlib.
17) Renamed freeze to cxfreeze to avoid conflict with another package that uses
    that executable as requested by Siegfried Gevatter.


Version 4.0b1 (September 2007)
------------------------------

1) Added support for placing modules in library.zip or in a separate zip file
   for each executable that is produced.
2) Added support for copying binary dependent files (DLLs and shared
   libraries)
3) Added support for including all submodules in a package
4) Added support for including icons in Windows executables
5) Added support for constants module which can be used for determining
   certain build constants at runtime
6) Added support for relative imports available in Python 2.5 and up
7) Added support for building Windows installers (Python 2.5 and up) and
   RPM packages
8) Added support for distutils configuration scripts
9) Added support for hooks which can force inclusion or exclusion of modules
   when certain modules are included
10) Added documentation and samples
11) Added setup.py for building the cx_Freeze package instead of a script
    used to build only the frozen bases
12) FreezePython renamed to a script called freeze in the Python distribution
13) On Linux and other platforms that support it set LD_RUN_PATH to include
    the directory in which the executable is located


Older versions
##############


Version 3.0.3 (July 2006)
-------------------------

1) In Common.c, used MAXPATHLEN defined in the Python OS independent include
   file rather than the PATH_MAX define which is OS dependent and is not
   available on IRIX as noted by Andrew Jones.
2) In the initscript ConsoleSetLibPath.py, added lines from initscript
   Console.py that should have been there since the only difference between
   that script and this one is the automatic re-execution of the executable.
3) Added an explicit "import encodings" to the initscripts in order to handle
   Unicode encodings a little better. Thanks to Ralf Schmitt for pointing out
   the problem and its solution.
4) Generated a meaningful name for the extension loader script so that it is
   clear which particular extension module is being loaded when an exception
   is being raised.
5) In MakeFrozenBases.py, use distutils to figure out a few more
   platform-dependent linker flags as suggested by Ralf Schmitt.


Version 3.0.2 (December 2005)
-----------------------------

1) Add support for compressing the byte code in the zip files that are
   produced.
2) Add better support for the win32com package as requested by Barry Scott.
3) Prevent deletion of target file if it happens to be identical to the
   source file.
4) Include additional flags for local modifications to a Python build as
   suggested by Benjamin Rutt.
5) Expanded instructions for building cx_Freeze from source based on a
   suggestion from Gregg Lind.
6) Fix typo in help string.


Version 3.0.1 (December 2004)
-----------------------------

1) Added option --default-path which is used to specify the path used when
   finding modules. This is particularly useful when performing cross
   compilations (such as for building a frozen executable for Windows CE).
2) Added option --shared-lib-name which can be used to specify the name of
   the shared library (DLL) implementing the Python runtime that is required
   for the frozen executable to work. This option is also particularly useful
   when cross compiling since the normal method for determining this
   information cannot be used.
3) Added option --zip-include which allows for additional files to be added
   to the zip file that contains the modules that implement the Python
   script. Thanks to Barray Warsaw for providing the initial patch.
4) Added support for handling read-only files properly. Thanks to Peter
   Grayson for pointing out the problem and providing a solution.
5) Added support for a frozen executable to be a symbolic link. Thanks to
   Robert Kiendl for providing the initial patch.
6) Enhanced the support for running a frozen executable that uses an existing
   Python installation to locate modules it requires. This is primarily of
   use for embedding Python where the interface is C but the ability to run
   from source is still desired.
7) Modified the documentation to indicate that building from source on
   Windows currently requires the mingw compiler (http://www.mingw.org).
8) Workaround the problem in Python 2.3 (fixed in Python 2.4) which causes a
   broken module to be left in sys.modules if an ImportError takes place
   during the execution of the code in that module. Thanks to Roger Binns
   for pointing this out.


Version 3.0 (September 2004)
----------------------------

1) Ensure that ldd is only run on extension modules.
2) Allow for using a compiler other than gcc for building the frozen base
   executables by setting the environment variable CC.
3) Ensure that the import lock is not held while executing the main script;
   otherwise, attempts to import a module within a thread will hang that
   thread as noted by Roger Binns.
4) Added support for replacing the paths in all frozen modules with something
   else (so that for example the path of the machine on which the freezing
   was done is not displayed in tracebacks)


Version 3.0 beta3 (September 2004)
----------------------------------

1) Explicitly include the warnings module so that at runtime warnings are
   suppressed as when running Python normally.
2) Improve the extension loader so that an ImportError is raised when the
   dynamic module is not located; otherwise an error about missing attributes
   is raised instead.
3) Extension loaders are only created when copying dependencies since the
   normal module should be loadable in the situation where a Python
   installation is available.
4) Added support for Python 2.4.
5) Fixed the dependency checking for wxPython to be a little more
   intelligent.


Version 3.0 beta2 (July 2004)
-----------------------------

1) Fix issues with locating the initscripts and bases relative to the
   directory in which the executable was started.
2) Added new base executable ConsoleKeepPath which is used when an existing
   Python installation is required (such as for FreezePython itself).
3) Forced the existence of a Python installation to be ignored when using the
   standard Console base executable.
4) Remove the existing file when copying dependent files; otherwise, an error
   is raised when attempting to overwrite read-only files.
5) Added option -O (or -OO) to FreezePython to set the optimization used when
   generating bytecode.


Version 3.0 beta1 (June 2004)
-----------------------------

1) cx_Freeze now requires Python 2.3 or higher since it takes advantage of
   the ability of Python 2.3 and higher to import modules from zip files.
   This makes the freezing process considerably simpler and also allows for
   the execution of multiple frozen packages (such as found in COM servers or
   shared libraries) without requiring modification to the Python modules.
2) All external dependencies have been removed. cx_Freeze now only requires
   a standard Python distribution to do its work.
3) Added the ability to define the initialization scripts that cx_Freeze uses
   on startup of the frozen program. Previously, these scripts were written
   in C and could not easily be changed; now they are written in Python and
   can be found in the initscripts directory (and chosen with the
   new --init-script option to FreezePython).
4) The base executable ConsoleSetLibPath has been removed and replaced with
   the initscript ConsoleSetLibPath.
5) Removed base executables for Win32 services and Win32 COM servers. This
   functionality will be restored in the future but it is not currently in a
   state that is ready for release. If this functionality is required, please
   use py2exe or contact me for my work in progress.
6) The attribute sys.frozen is now set so that more recent pywin32 modules
   work as expected when frozen.
7) Added option --include-path to FreezePython to allow overriding of
   sys.path without modifying the environment variable PYTHONPATH.
8) Added option --target-dir/--install-dir to specify the directory in which
   the frozen executable and its dependencies will be placed.
9) Removed the option --shared-lib since it was used for building shared
   libraries and can be managed with the initscript SharedLib.py.
10) MakeFrozenBases.py now checks the platform specific include directory as
    requested by Michael Partridge.


Version 2.2 (August 2003)
-------------------------

1) Add option (--ext-list-file) to FreezePython to write the list of
   extensions copied to the installation directory to a file. This option is
   useful in cases where multiple builds are performed into the same
   installation directory.
2) Pass the arguments on the command line through to Win32 GUI applications.
   Thanks to Michael Porter for pointing this out.
3) Link directly against the python DLL when building the frozen bases on
   Windows, thus eliminating the need for building an import library.
4) Force sys.path to include the directory in which the script to be frozen
   is found.
5) Make sure that the installation directory exists before attempting to
   copy the target binary into it.
6) The Win32GUI base has been modified to display fatal errors in message
   boxes, rather than printing errors to stderr, since on Windows the
   standard file IO handles are all closed.


Version 2.1 (July 2003)
-----------------------

1) Remove dependency on Python 2.2. Thanks to Paul Moore for not only
   pointing it out but providing patches.
2) Set up the list of frozen modules in advance, rather than doing it after
   Python is initialized so that implicit imports done by Python can be
   satisfied. The bug in Python 2.3 that demonstrated this issue has been
   fixed in the first release candidate. Thanks to Thomas Heller for pointing
   out the obvious in this instance!
3) Added additional base executable (ConsoleSetLibPath) to support setting
   the LD_LIBRARY_PATH variable on Unix platforms and restarting the
   executable to put the new setting into effect. This is primarily of use
   in distributing wxPython applications on Unix where the shared library
   has an embedded RPATH value which can cause problems.
4) Small improvements of documentation based on feedback from several people.
5) Print information about the files written or copied during the freezing
   process.
6) Do not copy extensions when freezing if the path is being overridden since
   it is expected that a full Python installation is available to the target
   users of the frozen binary.
7) Provide meaningful error message when the wxPython library cannot be
   found during the freezing process.


Version 2.0
-----------

1) Added support for in process (DLL) COM servers using PythonCOM.
2) Ensured that the frozen flag is set prior to determining the full path for
   the program in order to avoid warnings about Python not being found on
   some platforms.
3) Added include file and resource file to the source tree to avoid the
   dependency on the Wine message compiler for Win32 builds.
4) Dropped the option --copy-extensions; this now happens automatically since
   the resulting binary is useless without them.
5) Added a sample for building a Win32 service.
6) Make use of improved modules from Python 2.3 (which function under 2.2)


Version 1.1
-----------

1) Fixed import error with C extensions in packages; thanks to Thomas Heller
   for pointing out the solution to this problem.
2) Added options to FreezePython to allow for the inclusion of modules which
   will not be found by the module finder (--include-modules) and the
   exclusion of modules which will be found by the module finder but should
   not be included (--exclude-modules).
3) Fixed typo in README.txt.

