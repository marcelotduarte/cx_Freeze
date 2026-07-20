Setup script
============

cx_Freeze creates four new commands and subclasses for others to provide the
ability to build and install executables. In typical setuptools fashion they
can be provided in the setup script (it is called ``setup.py`` by convention,
although it can have any name), in a ``pyproject.toml`` configuration file,
in a ``setup.cfg`` configuration file, or on the command line.
They are described in detail below.

Example
-------

Assuming you have a script called ``hello.py`` which you want to turn into an
executable, this can be done using one of the following methods:

   .. tab:: pyproject.toml

      .. code-block:: toml

        [project]
        name = "hello"
        version = "0.1"
        description = "My GUI application!"

        [tool.cxfreeze]
        executables = [
            {script = "hello.py", base = "gui"}
        ]

        [tool.cxfreeze.build_exe]
        excludes = ["tkinter"]
        zip-include-packages = ["PySide6", "shiboken6"]

   .. tab:: setup.py

      .. code-block:: python

        from cx_Freeze import setup

        # Dependencies are automatically detected, but they might need fine-tuning.
        build_exe_options = {
            "excludes": ["tkinter"],
            "zip_include_packages": ["PySide6", "shiboken6"],
        }

        setup(
            name="hello",
            version="0.1",
            description="My GUI application!",
            options={"build_exe": build_exe_options},
            executables=[{"script": "hello.py", "base": "gui"}],
        )

   .. tab:: setup.cfg

      .. code-block:: ini

        [metadata]
        name = hello
        version = 0.1
        description = My GUI application!

        [build_exe]
        excludes = tkinter
        zip_include_packages = PySide6,shiboken6

      Minimum required file: ``setup.py``, to pass the `executables`.

      .. code-block:: python

        from cx_Freeze import setup

        setup(executables=[{"script": "hello.py", "base": "gui"}])

   .. tab:: cxfreeze command line

      See :doc:`cxfreeze script <script>`.

   .. tab:: setup script command line

      Minimum required file: ``setup.py``, in which the command-line options
      either complement or override them.

      .. code-block:: python

        from cx_Freeze import setup

        setup(executables=[{"script": "hello.py", "base": "gui"}])

The script is invoked as follows:

   .. tab:: pyproject.toml

      .. code-block:: console

        cxfreeze build

   .. tab:: setup.py

      .. code-block:: console

        python setup.py build

   .. tab:: setup.cfg

      .. code-block:: console

        python setup.py build

   .. tab:: cxfreeze command line

      .. code-block:: console

        cxfreeze --script=hello.py --base=gui --excludes=tkinter --zip-include-packages=PySide6,shiboken6

   .. tab:: setup script command line

      .. code-block:: console

        python setup.py build_exe --excludes=tkinter --zip-include-packages=PySide6,shiboken6

.. seealso::

   :doc:`setup() keywords <keywords>`.

   :packaging:`Declaring project metadata <specifications/declaring-project-metadata/>`

   :ref:`cx_freeze_executable`

.. note:: There are more examples in the :repository:`samples
   <tree/main/samples/>` directory.

This command will create a subdirectory called ``build`` with a further
subdirectory starting with the letters ``exe.`` and ending with the typical
identifier for the platform and Python version. This allows for multiple
platforms to be built without conflicts.

As can be seen in the previous examples, while using `pyproject.toml` the code
snippet:

  .. code-block:: toml

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter"]
    zip-include-packages = ["PySide6", "shiboken6"]

To specify options in the script, underscores are used:

  .. code-block:: python

    # ...
    build_exe_options = {
        "excludes": ["tkinter"],
        "zip_include_packages": ["PySide6", "shiboken6"],
    }

While on the command line, to specify the same options, dashes are used:

  .. code-block:: console

    python setup.py build_exe --excludes=tkinter --zip-include-packages=PySide6,shiboken6

On Windows, you can build a simple installer containing all the files cx_Freeze
includes for your application, by running the setup script as:

  .. code-block:: console

    python setup.py bdist_msi

On macOS, you can use ``bdist_mac`` to create a Mac application bundle or
``bdist_dmg`` to build a Mac disk image.


Commands
--------

.. _cx_freeze_build:

build
`````

This command is a standard command which has been modified by cx_Freeze to
build any executables that are defined.

.. deprecated:: 6.14
    ``build_exe`` option. Removed in version 7.0.

This is the equivalent help to specify the same options on the command line:

  .. code-block:: console

    python setup.py build --help
    Options for 'build' command:
      --build-base (-b)  base directory for build library
      (...)
      --compiler (-c)    specify the compiler type
      --help-compiler    list available compilers


.. _cx_freeze_build_exe:

build_exe
`````````

This command performs the work of building an executable or set of executables.
It can be further customized:

.. option:: build-exe

    directory for built executables and dependent files, defaults to a
    directory of the form ``build/exe.[platform identifier].[python version]``

.. option:: includes

    comma-separated list of names of modules to include

.. option:: excludes

    comma-separated list of names of modules to exclude

.. option:: packages

    comma-separated list of packages to include, which includes all
    submodules in the package

.. option:: replace-paths

    comma-separated list of paths to replace in the code object of
    included modules, using the form <search>=<replace>; search can be *
    which means all paths not already specified, leaving just the
    relative path to the module; multiple values are separated by the
    standard path separator

.. option:: path

    comma-separated list of paths to search for modules
    (use only if you know what you are doing)
    [default: `sys.path`]

.. option:: include-path

    comma-separated list of paths to modify the search for modules

.. option:: constants

    comma-separated list of constant values to include in the constants
    module called BUILD_CONSTANTS in the form <name>=<value>

.. option:: bin-includes

    list of files to include when determining dependencies of binary files
    that would normally be excluded, using first the full file name, then
    just the base file name, then the file name without any version numbers
    (the version numbers that normally follow the shared object extension
    are stripped before performing the comparison)

.. option:: bin-excludes

    list of files to exclude when determining dependencies of binary files
    that would normally be included, using first the full file name, then
    just the base file name, then the file name without any version numbers
    (the version numbers that normally follow the shared object extension
    are stripped before performing the comparison)

.. option:: bin-path-includes

    list of paths from which to include files when determining dependencies
    of binary files

.. option:: bin-path-excludes

    list of paths from which to exclude files when determining dependencies
    of binary files

.. option:: include-files

    list containing files to be copied to the target directory; it is
    expected that this list will contain strings or 2-tuples for the source
    and destination; the source can be a file or a directory (in which case
    the tree is copied except for .git, .svn and CVS directories);
    the target must not be an absolute path

.. option:: zip-includes

    list containing files to be included in the zip file directory; it is
    expected that this list will contain strings or 2-tuples for the source
    and destination

.. option:: zip-include-packages

    list of packages which should be included in the zip file; the default
    is for all packages to be placed in the file system, not the zip file;
    those packages which are known to work well inside a zip file can be
    included if desired; use * to specify that all packages should be
    included in the zip file

.. option:: zip-exclude-packages

    list of packages to exclude from the zip file and place in the file
    system instead; the default is for all packages to be placed in the
    file system since several packages assume that is where they
    are found and will fail when placed in a zip file; use * to specify that
    all packages should be placed in the file system and excluded from the
    zip file [default: \*]

.. option:: zip-filename

    filename for the shared zip file (.zip)
    [default: "library.zip" or None if :option:`no-compress` is used]

.. option:: no-compress

    create a zip file with no compression (See also :option:`zip-filename`)

.. option:: optimize

    optimization level, one of 0 (disabled), 1 or 2

.. option:: silent

    suppress all output except warnings
    (equivalent to :option:`silent-level` = 1)

.. option:: silent-level

    suppress output from the freeze process; can provide a value to specify
    what messages should be suppressed, with the possible values being:

    0. do not suppress any output [default];
    1. suppress information messages;
    2. also suppress missing-module warning messages;
    3. also suppress all other warning messages.

.. option:: include-msvcr

    include the Microsoft Visual C++ Redistributable
    files without needing the redistributable package
    installed (equivalent to :option:`include-msvcr-version` = 17)

.. option:: include-msvcr-version

    like :option:`include-msvcr` but the version can be set
    with one of the following values: 15, 16 or 17
    (version 15 includes UCRT for Windows 8.1 and below)

.. versionchanged:: 6.0
   Replaced the ``compressed`` option with the :option:`no-compress` option.

.. versionadded:: 6.7
    :option:`silent-level` option.

.. versionadded:: 7.1
    :option:`zip-filename` option used in conjunction with :option:`no-compress`.

.. versionadded:: 8.0
    :option:`include-msvcr-version` option.

This is the equivalent help to specify the same options on the command line:

  .. code-block:: console

    python setup.py build_exe --help
    Options for 'build_exe' command:
      --build-exe (-b)        directory for built executables and dependent files
      --includes (-i)         comma-separated list of modules to include
      --excludes (-e)         comma-separated list of modules to exclude
      --packages (-p)         comma-separated list of packages to include, which
                              includes all submodules in the package
      --replace-paths         comma-separated list of paths to replace in included
                              modules, using the form <search>=<replace>
      --path                  comma-separated list of paths to search for modules
                              (use only if you know what you are doing)
                              [default: sys.path]
      --include-path          comma-separated list of paths to modify the search
                              for modules
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
      --zip-filename          filename for the shared zipfile (.zip) [default:
                              "library.zip" or None if --no-compress is used]
      --no-compress           create a zip file with no compression (See also --
                              zip-filename)
      --optimize (-O)         optimization level: -O1 for "python -O", -O2 for
                              "python -OO" and -O0 to disable [default: -O0]
      --silent (-s)           suppress all output except warnings (equivalent to
                              --silent-level=1)
      --silent-level          suppress output from build_exe command. level 0: get
                              all messages; [default] level 1: suppress
                              information messages, but still get warnings;
                              (equivalent to --silent) level 2: suppress missing
                              missing-module warnings level 3: suppress all
                              warning messages
      --include-msvcr         include the Microsoft Visual C++ Redistributable
                              files without needing the redistributable package
                              installed (equivalent to --include-msvcr-version=17)
      --include-msvcr-version like --include-msvcr but the version can be set
                              with one of the following values: 15, 16 or 17
                              (version 15 includes UCRT for Windows 8.1 and below)


install
```````

This command is a standard command which has been modified by cx_Freeze to
install any executables that are defined. The following options were added to
the standard set of options for the command:

.. option:: install_exe

    directory for installed executables and dependent files


install_exe
```````````

This command performs the work installing an executable or set of executables.
It can be used directly but most often is used when building Windows installers
or RPM packages. It can be further customized:

.. option:: install-dir

    directory to install executables to; this defaults to a subdirectory
    called <name>-<version> in the "Program Files" directory on Windows and
    <prefix>/lib on other platforms; on platforms other than Windows
    symbolic links are also created in <prefix>/bin for each executable.

.. option:: build-dir

    build directory (where to install from); this defaults to the build-dir
    from the build command

.. option:: force

    force installation, overwriting existing files

.. option:: skip-build

    skip the build steps

This is the equivalent help to specify the same options on the command line:

  .. code-block:: console

    python setup.py install_exe --help
    Options for 'install_exe' command:
      --install-dir (-d)  directory to install executables to
      --build-dir (-b)    build directory (where to install from)
      --force (-f)        force installation (overwrite existing files)
      --skip-build        skip the build steps



.. _cx_freeze_executable:

cx_Freeze.Executable
--------------------

The options for the `build_exe` command are the defaults for any executables
that are created. The options for the `Executable` class allow specification of
the values specific to a particular executable. The arguments to the
constructor are as follows:

.. option:: script

    the name of the file containing the script which is to be frozen

.. option:: init_script

    the name of the initialization script that will be executed before the
    actual script is executed; this script is used to set up the environment
    for the executable; if a name is given without an absolute path the
    names of files in the initscripts subdirectory of the cx_Freeze package
    is searched

.. option:: base

    the name of the base executable; the pre-defined values are:
    "console", "gui", "gui_dgpu" and "service";
    an user-defined base is accepted if it is given with an absolute
    path name [default: "console"]

.. option:: target_name

    the name of the target executable; the default value is the
    name of the script; it is recommended NOT to use an extension
    (automatically added on Windows); target-name with version is
    supported; if specified a path, raise an error

.. option:: icon

    name of icon which should be included in the executable itself
    on Windows (ignored by Python app from Microsoft Store) or placed
    in the target directory for other platforms; it is recommended
    NOT to use an extension (automatically added ".ico" on Windows,
    ".icns" on macOS and ".png" or ".svg" on Linux and others)

.. option:: manifest

    name of manifest which should be included in the executable itself
    (Windows only - ignored by Python app from Microsoft Store)

.. option:: uac_admin

    creates a manifest for an application that will request elevation
    (Windows only - ignored by Python app from Microsoft Store)

.. option:: uac_uiaccess

    changes the application manifest to bypass user interface control
    (Windows only - ignored by Python app from Microsoft Store)

.. option:: shortcut_name

    the name to give a shortcut for the executable when included in an MSI
    package (Windows only)

.. option:: shortcut_dir

    the directory in which to place the shortcut when being installed by an
    MSI package; see the MSI Shortcut table documentation for more
    information on what values can be placed here (Windows only).

.. option:: copyright

    the copyright value to include in the version resource associated with
    executable (Windows only)

.. option:: trademarks

    the trademarks value to include in the version resource associated with
    the executable (Windows only)

.. versionchanged:: 6.5
    Arguments are all snake_case (camelCase removed in 6.15).

.. versionadded:: 6.10
    :option:`manifest` and :option:`uac_admin` options.

.. versionadded:: 7.0
    :option:`uac_uiaccess` option.

.. versionchanged:: 7.0
    :option:`base` option has new pre-defined values: "gui" and "service"
    ("console" remains the default value).

.. versionchanged:: 8.0
    :option:`base` option does not accept the old values
    "Win32GUI" and "Win32Service" in Python 3.13+.

.. versionchanged:: 8.6
    :option:`base` option has a new pre-defined value: "gui_dgpu"
    - this ensures that frozen applications automatically prefer the
    high-performance discrete GPU on Windows systems with hybrid graphics
    (NVIDIA Optimus / AMD PowerXpress)

.. seealso::

   `Windows Manifest
   <https://learn.microsoft.com/en-us/previous-versions/bb756929(v=msdn.10)#application-manifest-schema>`_

   `Important note for uiaccess
   <https://learn.microsoft.com/en-us/previous-versions/bb756929(v=msdn.10)#uiaccess-values>`_

.. note::

   #. ``setup`` accepts a list of `Executable`
   #. target_name has been extended to support version, like
      `target_name="Hello-0.1"` or `target_name="Hello.0.1.exe"`
   #. the name of the target executable can be modified after the build only if
      one Executable is built.
