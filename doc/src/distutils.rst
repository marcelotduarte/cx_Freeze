.. _distutils:

distutils setup script
======================

In order to make use of distutils a setup script must be created. This is
called ``setup.py`` by convention, although it can have any name. It looks
something like this::

    import sys
    from cx_Freeze import setup, Executable

    # Dependencies are automatically detected, but it might need fine tuning.
    build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

    # GUI applications require a different base on Windows (the default is for a
    # console application).
    base = None
    if sys.platform == "win32":
        base = "Win32GUI"

    setup(  name = "guifoo",
            version = "0.1",
            description = "My GUI application!",
            options = {"build_exe": build_exe_options},
            executables = [Executable("guifoo.py", base=base)])

There are more examples in the ``samples/`` directory of `the source
<https://github.com/anthony-tuininga/cx_Freeze/tree/master/cx_Freeze/samples>`_.

The script is invoked as follows::

    python setup.py build

This command will create a subdirectory called ``build`` with a further
subdirectory starting with the letters ``exe.`` and ending with the typical
identifier for the platform that distutils uses. This allows for multiple
platforms to be built without conflicts.

On Windows, you can build a simple installer containing all the files cx_Freeze
includes for your application, by running the setup script as::

    python setup.py bdist_msi

On Mac OS X, you can use ``bdist_dmg`` to build a Mac disk image.

distutils commands
------------------

cx_Freeze creates four new commands and subclasses four others in order to
provide the ability to both build and install executables. In typical distutils
fashion they can be provided in the setup script, on the command line or in
a ``setup.cfg`` configuration file. They are described in further detail below.

To specify options in the script, use underscores in the name. For example::

    setup(...
          options = {'build_exe': {'init_script':'Console'}} )

To specify the same options on the command line, use dashes, like this::

    python setup.py build_exe --init-script Console

Some options also have a short form to use on the command line. These are given in brackets below.

build
`````

This command is a standard command which has been modified by cx_Freeze to
build any executables that are defined. The following options were added to
the standard set of options for the command:

.. list-table::
   :header-rows: 1
   :widths: 200 600

   * - option name
     - description
   * - build_exe (-b)
     - directory for built executables and dependent files, defaults to
       ``build/``

.. _distutils_build_exe:

build_exe
`````````

This command performs the work of building an executable or set of executables.
It can be further customized:

.. list-table::
   :header-rows: 1
   :widths: 200 600

   * - option name
     - description
   * - build_exe (-b)
     - directory for built executables and dependent files, defaults to
       ``build/``
   * - optimize (-o)
     - optimization level, one of 0 (disabled), 1 or 2
   * - excludes (-e)
     - comma separated list of names of modules to exclude
   * - includes (-e)
     - comma separated list of names of modules to include
   * - packages (-p)
     - comma separated list of packages to include, which includes all
       submodules in the package
   * - namespace_packages
     - comma separated list of packages to be treated as namespace packages
       (path is extended using pkgutil)
   * - replace_paths
     - Modify filenames attached to code objects, which appear in tracebacks.
       Pass a comma separated list of paths in the form <search>=<replace>. The
       value * in the search portion will match the directory containing the
       entire package, leaving just the relative path to the module.
   * - path
     - comma separated list of paths to search; the default value is sys.path
   * - no_compress
     - create a zipfile with no compression
   * - constants
     - comma separated list of constant values to include in the constants
       module called BUILD_CONSTANTS in the form <name>=<value>
   * - include_files
     - list containing files to be copied to the target directory; it is
       expected that this list will contain strings or 2-tuples for the source
       and destination; the source can be a file or a directory (in which case
       the tree is copied except for .svn and CVS directories); the target must
       not be an absolute path
   * - include_msvcr
     - include the Microsoft Visual C runtime DLLs and (if necessary) the
       manifest file required to run the executable without needing the
       redistributable package installed
   * - zip_includes
     - list containing files to be included in the zip file directory; it is
       expected that this list will contain strings or 2-tuples for the source
       and destination
   * - bin_includes
     - list of names of files to include when determining dependencies of
       binary files that would normally be excluded; note that version numbers
       that normally follow the shared object extension are stripped prior
       to performing the comparison
   * - bin_excludes
     - list of names of files to exclude when determining dependencies of
       binary files that would normally be included; note that version numbers
       that normally follow the shared object extension are stripped prior to
       performing the comparison
   * - bin_path_includes
     - list of paths from which to include files when determining dependencies
       of binary files
   * - bin_path_excludes
     - list of paths from which to exclude files when determining dependencies
       of binary files
   * - zip_include_packages
     - list of packages which should be included in the zip file; the default
       is for all packages to be placed in the file system, not the zip file;
       those packages which are known to work well inside a zip file can be
       included if desired; use * to specify that all packages should be
       included in the zip file
   * - zip_exclude_packages
     - list of packages which should be excluded from the zip file and placed
       in the file system instead; the default is for all packages to be placed
       in the file system since a number of packages assume that is where they
       are found and will fail when placed in a zip file; use * to specify that
       all packages should be placed in the file system and excluded from the
       zip file (the default)
   * - silent (-s)
     - suppress all output except warnings


install
```````

This command is a standard command which has been modified by cx_Freeze to
install any executables that are defined. The following options were added to
the standard set of options for the command:

.. list-table::
   :header-rows: 1
   :widths: 200 600

   * - option name
     - description
   * - install_exe
     - directory for installed executables and dependent files


install_exe
```````````

This command performs the work installing an executable or set of executables.
It can be used directly but most often is used when building Windows installers
or RPM packages. It can be further customized:

.. list-table::
   :header-rows: 1
   :widths: 200 600

   * - option name
     - description
   * - install_dir (-d)
     - directory to install executables to; this defaults to a subdirectory
       called <name>-<version> in the "Program Files" directory on Windows and
       <prefix>/lib on other platforms; on platforms other than Windows
       symbolic links are also created in <prefix>/bin for each executable.
   * - build_dir (-b)
     - build directory (where to install from); this defaults to the build_dir
       from the build command
   * - force (-f)
     - force installation, overwriting existing files
   * - skip_build
     - skip the build steps


bdist_msi
`````````

This command is a standard command in Python 2.5 and higher which has been
modified by cx_Freeze to handle installing executables and their dependencies.
The following options were added to the standard set of options for the
command:

.. list-table::
   :header-rows: 1
   :widths: 200 600

   * - option_name
     - description
   * - add_to_path
     - add the target directory to the PATH environment variable; the default
       value is True if there are any console based executables and False
       otherwise
   * - upgrade_code
     - define the upgrade code for the package that is created; this is used to
       force removal of any packages created with the same upgrade code prior
       to the installation of this one
   * - environment_variables
     - add any environment variables to MSI package; those variables will be
       added to system environment variables at installation time
       ::

          'bdist_msi': {
              'upgrade_code': upgrade_code,
              'add_to_path': True,
                  'environment_variables': [
                      ("E_MYAPP_VAR", "=-*MYAPP_VAR", "1", "TARGETDIR")
                  ]
          }

bdist_rpm
`````````

This command is a standard command which has been modified by cx_Freeze to
ensure that packages are created with the proper architecture for the platform.
The standard command assumes that the package should be architecture
independent if it cannot find any extension modules.

bdist_mac
`````````

This command is available on Mac OS X systems, to create a Mac application
bundle (a .app directory).

.. list-table::
   :header-rows: 1
   :widths: 200 600

   * - option_name
     - description
   * - iconfile
     - Path to an icns icon file for the application. This will be copied into
       the bundle.
   * - qt_menu_nib
     - Path to the qt-menu.nib file for Qt applications. By default, it will be
       auto-detected.
   * - bundle_name
     - File name for the bundle application without the .app extension.
   * - custom_info_plist
     - File to be used as the Info.plist in the app bundle. A basic one will be
       generated by default.
   * - include_frameworks
     - A list of Framework directories to include in the app bundle.
   * - include_resources
     - A list of tuples of additional files to include in the app bundle's
       resources directory, with the first element being the source, and second
       the destination file or directory name.
   * - codesign_identity
     - The identity of the key to be used to sign the app bundle.
   * - codesign_entitlements
     - The path to an entitlements file to use for your application's code
       signature.
   * - codesign_deep
     - Boolean for whether to codesign using the --deep option.
   * - codesign_resource_rules
     - Plist file to be passed to codesign's --resource-rules option.
   * - absolute_reference_path
     - Path to use for all referenced libraries instead of @executable_path
   * - rpath_lib_folder
     - replace @rpath with given folder for any files

.. versionadded:: 4.3

.. versionchanged:: 4.3.2
    Added the ``iconfile`` and ``bundle_name`` options.

.. versionchanged:: 4.3.3
    Added the ``include_frameworks``, ``custom_info_plist``,
    ``codesign_identity`` and ``codesign_entitlements`` options.

.. versionchanged:: 4.3.4
    Added the ``codesign_deep`` and ``codesign_resource_rules`` options.

.. versionchanged:: 6.0
    Added the ``environment_variables``, ``include_resources``,
    ``absolute_reference_path`` and ``rpath_lib_folder`` options. Replaced the
    ``compressed`` option with the ``no_compress`` option.


bdist_dmg
`````````

This command is available on Mac OS X systems; it creates an application bundle,
then packages it into a DMG disk image suitable for distribution and
installation.

.. list-table::
   :header-rows: 1
   :widths: 200 600

   * - option_name
     - description
   * - volume_label
     - Volume label of the DMG disk image
   * - applications_shortcut
     - Boolean for whether to include shortcut to Applications in the DMG disk
       image

.. versionadded:: 4.3

.. versionchanged:: 4.3.2
    Added the ``applications_shortcut`` option.


cx_Freeze.Executable
--------------------

The options for the `build_exe` command are the defaults for any executables
that are created. The options for the `Executable` class allow specification of
the values specific to a particular executable. The arguments to the
constructor are as follows:

.. list-table::
   :header-rows: 1
   :widths: 200 600

   * - argument name
     - description
   * - script
     - the name of the file containing the script which is to be frozen
   * - initScript
     - the name of the initialization script that will be executed before the
       actual script is executed; this script is used to set up the environment
       for the executable; if a name is given without an absolute path the
       names of files in the initscripts subdirectory of the cx_Freeze package
       is searched
   * - base
     - the name of the base executable; if a name is given without an absolute
       path the names of files in the bases subdirectory of the cx_Freeze
       package is searched
   * - targetName
     - the name of the target executable; the default value is the name of the
       script with the extension exchanged with the extension for the base
       executable
     - if specified without extension, one will be added (Windows only).
   * - icon
     - name of icon which should be included in the executable itself on
       Windows or placed in the target directory for other platforms
   * - shortcutName
     - the name to give a shortcut for the executable when included in an MSI
       package (Windows only).
   * - shortcutDir
     - the directory in which to place the shortcut when being installed by an
       MSI package; see the MSI Shortcut table documentation for more
       information on what values can be placed here (Windows only).
   * - copyright
     - the copyright value to include in the version resource associated with
       executable (Windows only).
   * - trademarks
     - the trademarks value to include in the version resource associated with
       the executable (Windows only).

