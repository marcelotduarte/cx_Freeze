.. _setup_script:

setup script
============

In order to make use of this method, a setup script must be created. This is
called ``setup.py`` by convention, although it can have any name. It looks
something like this:

  .. code-block:: python

    import sys
    from cx_Freeze import setup, Executable

    # Dependencies are automatically detected, but it might need fine tuning.
    # "packages": ["os"] is used as example only
    build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

    # base="Win32GUI" should be used only for Windows GUI app
    base = None
    if sys.platform == "win32":
        base = "Win32GUI"

    setup(
        name = "guifoo",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("guifoo.py", base=base)]
    )

There are more examples in the ``samples/`` directory of `the source
<https://github.com/marcelotduarte/cx_Freeze/tree/main/cx_Freeze/samples>`_.

The script is invoked as follows:

  .. code-block:: console

    python setup.py build

This command will create a subdirectory called ``build`` with a further
subdirectory starting with the letters ``exe.`` and ending with the typical
identifier for the platform and python version. This allows for multiple
platforms to be built without conflicts.

On Windows, you can build a simple installer containing all the files cx_Freeze
includes for your application, by running the setup script as:

  .. code-block:: console

    python setup.py bdist_msi

On Mac OS X, you can use ``bdist_dmg`` to build a Mac disk image.

commands
--------

cx_Freeze creates four new commands and subclasses four others in order to
provide the ability to both build and install executables. In typical
setuptools fashion they can be provided in the setup script, on the command
line or in a ``setup.cfg`` configuration file. They are described in further
detail below.

To specify options in the script, use underscores in the name. For example:

  .. code-block:: python

    setup(
         #...
          options = {"build_exe": {"zip_include_packages": ["encodings"]}}
         )

To specify the same options on the command line, use dashes, like this:

  .. code-block:: console

    python setup.py build_exe --zip-include-packages=encodings


build
`````

This command is a standard command which has been modified by cx_Freeze to
build any executables that are defined. The following options were added to
the standard set of options for the command:

.. list-table::
   :header-rows: 1
   :widths: 200 600
   :width: 100%

   * - option name
     - description
   * - .. option:: build_exe
     - directory for built executables and dependent files, defaults to a
       directory of the form ``build/exe.[platform identifier].[python version]``

This is the equivalent help to specify the same options on the command line:

  .. code-block:: console

    python setup.py build --help
    Options for 'build' command:
      --build-exe        build directory for executables
      --compiler (-c)    specify the compiler type
      --help-compiler    list available compilers

.. _cx_freeze_build_exe:

build_exe
`````````

This command performs the work of building an executable or set of executables.
It can be further customized:

.. list-table::
   :header-rows: 1
   :widths: 200 600
   :width: 100%

   * - option name
     - description
   * - .. option:: build_exe
     - directory for built executables and dependent files, defaults to
       the value of the "build_exe" option on the build command (see
       above); note that using this option (instead of the corresponding
       option on the build command) may break bdist_msi, bdist_mac, and
       other commands
   * - .. option:: optimize
     - optimization level, one of 0 (disabled), 1 or 2
   * - .. option:: excludes
     - comma-separated list of names of modules to exclude
   * - .. option:: includes
     - comma-separated list of names of modules to include
   * - .. option:: packages
     - comma-separated list of packages to include, which includes all
       submodules in the package
   * - .. option:: replace_paths
     - comma-separated list of paths to replace in the code object of
       included modules, using the form <search>=<replace>; search can be *
       which means all paths not already specified, leaving just the
       relative path to the module; multiple values are separated by the
       standard path separator
   * - .. option:: path
     - comma-separated list of paths to search; the default value is sys.path
   * - .. option:: no_compress
     - create a zipfile with no compression
   * - .. option:: constants
     - comma-separated list of constant values to include in the constants
       module called BUILD_CONSTANTS in the form <name>=<value>
   * - .. option:: bin_includes
     - list of files to include when determining dependencies of binary files
       that would normally be excluded, using first the full file name, then
       just the base file name, then the file name without any version numbers
       (the version numbers that normally follow the shared object extension
       are stripped prior to performing the comparison)
   * - .. option:: bin_excludes
     - list of files to exclude when determining dependencies of binary files
       that would normally be included, using first the full file name, then
       just the base file name, then the file name without any version numbers
       (the version numbers that normally follow the shared object extension
       are stripped prior to performing the comparison)
   * - .. option:: bin_path_includes
     - list of paths from which to include files when determining dependencies
       of binary files
   * - .. option:: bin_path_excludes
     - list of paths from which to exclude files when determining dependencies
       of binary files
   * - .. option:: include_files
     - list containing files to be copied to the target directory; it is
       expected that this list will contain strings or 2-tuples for the source
       and destination; the source can be a file or a directory (in which case
       the tree is copied except for .svn and CVS directories); the target must
       not be an absolute path
   * - .. option:: zip_includes
     - list containing files to be included in the zip file directory; it is
       expected that this list will contain strings or 2-tuples for the source
       and destination
   * - .. option:: zip_include_packages
     - list of packages which should be included in the zip file; the default
       is for all packages to be placed in the file system, not the zip file;
       those packages which are known to work well inside a zip file can be
       included if desired; use * to specify that all packages should be
       included in the zip file
   * - .. option:: zip_exclude_packages
     - list of packages which should be excluded from the zip file and placed
       in the file system instead; the default is for all packages to be placed
       in the file system since a number of packages assume that is where they
       are found and will fail when placed in a zip file; use * to specify that
       all packages should be placed in the file system and excluded from the
       zip file (the default)
   * - .. option:: silent
     - suppress all output except warnings (equivalent to silent_level=1)
   * - .. option:: silent_level
     - suppress output from freeze process; can provide a value to specify
       what messages should be suppressed, with the possible values being:

       0. do not suppress any output [default];
       1. suppress information messages;
       2. also suppress missing-module warning messages;
       3. also suppress all other warning messages.
   * - .. option:: include_msvcr
     - include the Microsoft Visual C runtime files without needing the
       redistributable package installed

.. versionadded:: 6.7
    ``silent_level`` option.

This is the equivalent help to specify the same options on the command line:

  .. code-block:: console

    python setup.py build_exe --help
    Options for 'build_exe' command:
    --build-exe (-b)        directory for built executables and dependent files
    --optimize (-O)         optimization level: -O1 for "python -O", -O2 for
                            "python -OO" and -O0 to disable [default: -O0]
    --excludes (-e)         comma-separated list of modules to exclude
    --includes (-i)         comma-separated list of modules to include
    --packages (-p)         comma-separated list of packages to include, which
                            includes all submodules in the package
    --namespace-packages    [DEPRECATED]
    --replace-paths         comma-separated list of paths to replace in included
                            modules, using the form <search>=<replace>
    --path                  comma-separated list of paths to search
    --no-compress           create a zipfile with no compression
    --constants             comma-separated list of constants to include
    --bin-includes          list of files to include when determining
                            dependencies of binary files that would normally be
                            excluded
    --bin-excludes          list of files to exclude when determining
                            dependencies of binary files that would normally be
                            included
    --bin-path-includes     list of paths from which to include files when
                            determining dependencies of binary files
    --bin-path-excludes     list of paths from which to exclude files when
                            determining dependencies of binary files
    --include-files (-f)    list of tuples of additional files to include in
                            distribution
    --zip-includes          list of tuples of additional files to include in zip
                            file
    --zip-include-packages  comma-separated list of packages to include in the
                            zip file (or * for all) [default: none]
    --zip-exclude-packages  comma-separated list of packages to exclude from the
                            zip file and place in the file system instead (or *
                            for all) [default: *]
    --silent (-s)           suppress all output except warnings (equivalent to
                            --silent-level=1)
    --silent-level          suppress output from build_exe command. level 0: get
                            all messages; [default] level 1: suppress
                            information messages, but still get warnings;
                            (equivalent to --silent) level 2: suppress missing
                            missing-module warnings level 3: suppress all
                            warning messages
    --include-msvcr         include the Microsoft Visual C runtime files

install
```````

This command is a standard command which has been modified by cx_Freeze to
install any executables that are defined. The following options were added to
the standard set of options for the command:

.. list-table::
   :header-rows: 1
   :widths: 200 600
   :width: 100%

   * - option name
     - description
   * - .. option:: install_exe
     - directory for installed executables and dependent files


install_exe
```````````

This command performs the work installing an executable or set of executables.
It can be used directly but most often is used when building Windows installers
or RPM packages. It can be further customized:

.. list-table::
   :header-rows: 1
   :widths: 200 600
   :width: 100%

   * - option name
     - description
   * - .. option:: install_dir
     - directory to install executables to; this defaults to a subdirectory
       called <name>-<version> in the "Program Files" directory on Windows and
       <prefix>/lib on other platforms; on platforms other than Windows
       symbolic links are also created in <prefix>/bin for each executable.
   * - .. option:: build_dir
     - build directory (where to install from); this defaults to the build_dir
       from the build command
   * - .. option:: force
     - force installation, overwriting existing files
   * - .. option:: skip_build
     - skip the build steps

This is the equivalent help to specify the same options on the command line:

  .. code-block:: console

    python setup.py install_exe --help
    Options for 'install_exe' command:
      --install-dir (-d)  directory to install executables to
      --build-dir (-b)    build directory (where to install from)
      --force (-f)        force installation (overwrite existing files)
      --skip-build        skip the build steps


bdist_msi
`````````

This command is a standard command in Python 2.5 and higher which has been
modified by cx_Freeze to handle installing executables and their dependencies.
The following options were added to the standard set of options for the
command:

.. list-table::
   :header-rows: 1
   :widths: 200 600
   :width: 100%

   * - option_name
     - description
   * - .. option:: add_to_path
     - add the target directory to the PATH environment variable; the default
       value is True if there are any console based executables and False
       otherwise
   * - .. option:: all_users
     - perform installation for all users; the default value is False and
       results in an installation for just the installing user
   * - .. option:: data
     - dictionary of arbitrary MSI data indexed by table name; for each table,
       a list of tuples should be provided, representing the rows that should
       be added to the table. For binary values (e.g. Icon.Data), pass the path
       to the file containing the data.
   * - .. option:: summary_data
     - dictionary of data to include in MSI summary information stream
       (allowable keys are "author", "comments", "keywords")
   * - .. option:: directories
     - list of directories that should be created during installation
   * - .. option:: environment_variables
     - list of environment variables that should be added to the system during
       installation
   * - .. option:: initial_target_dir
     - defines the initial target directory supplied to the user during
       installation
   * - .. option:: install_icon
     - path of icon to use for the add/remove programs window that pops up
       during installation
   * - .. option:: product_code
     - define the product code for the package that is created
   * - .. option:: target_name
     - specifies the name of the file that is to be created
   * - .. option:: upgrade_code
     - define the GUID of the upgrade code for the package that is created;
       this is used to force removal of any packages created with the same
       upgrade code prior to the installation of this one; the valid format for
       a GUID is {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX} where X is a hex digit.
       Refer to `Windows GUID
       <https://docs.microsoft.com/en-us/windows/win32/api/guiddef/ns-guiddef-guid>`_.
   * - .. option:: extensions
     - list of dictionaries specifying the extensions that the installed program
       handles. Each extension needs to specify at least the extension, a verb,
       and an executable. Additional allowed keys are `argument` to specify
       the invocation of the executable, `mime` for the extension’s mime type,
       and `context` for the context menu text.

.. versionadded:: 6.7
    ``extensions`` options.
    
.. note:: ``extensions`` is supported in python 3.7.4 and up.


This is the equivalent help to specify the same options on the command line:

  .. code-block:: console

    python setup.py bdist_msi --help

For example:

  .. code-block:: python

    directory_table = [
        ("ProgramMenuFolder", "TARGETDIR", "."),
        ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
    ]

    msi_data = {
        "Directory": directory_table,
        "ProgId": [
            ("Prog.Id", None, None, "This is a description", "IconId", None),
        ],
        "Icon": [
            ("IconId", "icon.ico"),
        ],
    }

    bdist_msi_options = {
        "add_to_path": True,
        "data": msi_data,
        "environment_variables": [
            ("E_MYAPP_VAR", "=-*MYAPP_VAR", "1", "TARGETDIR")
        ],
        "upgrade_code": "{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}",
    }

    build_exe_options = {"excludes": ["tkinter"], "include_msvcr": True}

    executables = [
        Executable(
            "hello.py",
            copyright="Copyright (C) 2021 cx_Freeze",
            base=base,
            icon="icon.ico",
            shortcutName="My Program Name",
            shortcutDir="MyProgramMenu",
        ),
    ],

    setup(
        name="hello",
        version="0.1",
        description="Sample cx_Freeze script to test MSI arbitrary data stream",
        executables=executables,
        options={
            "build_exe": build_exe_options,
            "bdist_msi": bdist_msi_options,
        },
    )

Samples:
There are more examples in the ``samples/`` directory of `the source
<https://github.com/marcelotduarte/cx_Freeze/tree/main/cx_Freeze/samples>`_.


.. seealso:: `Windows Installer
   <https://docs.microsoft.com/en-us/windows/win32/msi/windows-installer-portal>`_


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
   :width: 100%

   * - option_name
     - description
   * - .. option:: iconfile
     - Path to an icns icon file for the application. This will be copied into
       the bundle.
   * - .. option:: qt_menu_nib
     - Path to the qt-menu.nib file for Qt applications. By default, it will be
       auto-detected.
   * - .. option:: bundle_name
     - File name for the bundle application without the .app extension.
   * - .. option:: plist_items
     - A list of key-value pairs (type: List[Tuple[str, str]]) to be added to
       the app bundle Info.plist file.  Overrides any specific entries set by
       custom_info_plist or be default.
   * - .. option:: custom_info_plist
     - File to be used as the Info.plist in the app bundle. If not specified, A
       basic Info.plist will be generated by default, which specifies
       CFBundleIconFile, CFBundleDevelopmentRegion, CFBundleIdentifier,
       CFBundlePackageType, and NSHighResolutionCapable.
   * - .. option:: include_frameworks
     - A list of Framework directories to include in the app bundle.
   * - .. option:: include_resources
     - A list of tuples of additional files to include in the app bundle's
       resources directory, with the first element being the source, and second
       the destination file or directory name.
   * - .. option:: codesign_identity
     - The identity of the key to be used to sign the app bundle.
   * - .. option:: codesign_entitlements
     - The path to an entitlements file to use for your application's code
       signature.
   * - .. option:: codesign_deep
     - Boolean for whether to codesign using the --deep option.
   * - .. option:: codesign_resource_rules
     - Plist file to be passed to codesign's --resource-rules option.
   * - .. option:: absolute_reference_path
     - Path to use for all referenced libraries instead of @executable_path
   * - .. option:: rpath_lib_folder
     - [DEPRECATED]. Will be removed in next version. (Formerly replaced
       @rpath with given folder for any files.)

.. versionadded:: 6.0
    ``environment_variables``, ``include_resources``,
    ``absolute_reference_path`` and ``rpath_lib_folder`` options.

.. versionchanged:: 6.0
   Replaced the ``compressed`` option with the ``no_compress`` option.

.. deprecated:: 6.5
    ``rpath_lib_folder`` option.

This is the equivalent help to specify the same options on the command line:

  .. code-block:: console

    python setup.py bdist_mac --help


bdist_dmg
`````````

This command is available on Mac OS X systems; it creates an application
bundle, then packages it into a DMG disk image suitable for distribution and
installation.

.. list-table::
   :header-rows: 1
   :widths: 200 600
   :width: 100%

   * - option_name
     - description
   * - .. option:: volume_label
     - Volume label of the DMG disk image
   * - .. option:: applications_shortcut
     - Boolean for whether to include shortcut to Applications in the DMG disk
       image
   * - .. option:: silent (-s)
     - suppress all output except warnings

This is the equivalent help to specify the same options on the command line:

  .. code-block:: console

    python setup.py bdist_dmg --help


cx_Freeze.Executable
--------------------

The options for the `build_exe` command are the defaults for any executables
that are created. The options for the `Executable` class allow specification of
the values specific to a particular executable. The arguments to the
constructor are as follows:

.. list-table::
   :header-rows: 1
   :widths: 200 600
   :width: 100%

   * - argument name
     - description
   * - script
     - the name of the file containing the script which is to be frozen
   * - init_script
     - the name of the initialization script that will be executed before the
       actual script is executed; this script is used to set up the environment
       for the executable; if a name is given without an absolute path the
       names of files in the initscripts subdirectory of the cx_Freeze package
       is searched
   * - base
     - the name of the base executable; if a name is given without an absolute
       path the names of files in the bases subdirectory of the cx_Freeze
       package is searched
   * - target_name
     - the name of the target executable; the default value is the name of the
       script; the extension is optional (automatically added on Windows);
       support for names with version; if specified a pathname, raise an error.
   * - icon
     - name of icon which should be included in the executable itself on
       Windows or placed in the target directory for other platforms
       (ignored in Microsoft Store Python app)
   * - shortcut_name
     - the name to give a shortcut for the executable when included in an MSI
       package (Windows only).
   * - shortcut_dir
     - the directory in which to place the shortcut when being installed by an
       MSI package; see the MSI Shortcut table documentation for more
       information on what values can be placed here (Windows only).
   * - copyright
     - the copyright value to include in the version resource associated with
       executable (Windows only).
   * - trademarks
     - the trademarks value to include in the version resource associated with
       the executable (Windows only).

.. versionchanged:: 6.5
    Arguments are all snake_case (camelCase are still valid up to 7.0)

.. note::

   #. ``setup`` accepts a list of `Executable`
   #. target_name has been extended to support version, like:
      target_name="Hello-1.0"
      target_name="Hello.0.1.exe"
   #. the name of the target executable can be modified after the build only if
      one Executable is built.
