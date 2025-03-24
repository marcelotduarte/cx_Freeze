cxfreeze script
===============

The ``cxfreeze`` script is included with other Python scripts. On Windows and
the Mac this is in the ``Scripts`` subdirectory of your Python installation
whereas on Unix platforms this is in the bin directory of the prefix where
Python is installed.

Assuming you have a script called ``hello.py`` which you want to turn into an
executable, this can be accomplished by this command:

  .. code-block:: console

    cxfreeze --script hello.py --target-dir dist

Further customization can be done using the following options:

.. option:: --script=NAME

    script which will be turned into an executable

.. option:: --init-script=NAME

    script which will be executed upon startup; if the
    name of the file is not an absolute file name, the
    subdirectory initscripts (rooted in the directory in
    which the **cx_Freeze** package is found) will be searched
    for a file matching the name

.. option:: --base=NAME, --base-name=NAME

    the name of the base executable; the pre-defined values are:
    "console", "gui" and "service"; a user-defined base is accepted
    if it is given with an absolute path name [default: "console"]

.. option:: --target-name=NAME

    the name of the target executable; the default value is the
    name of the script; it is recommended NOT to use an extension
    (automatically added on Windows); target-name with version is
    supported; if specified a path, raise an error

.. option:: --target-dir=DIR

    directory for built executables and dependent files

.. option:: --icon=ICON

    name of icon which should be included in the executable itself
    on Windows (ignored by Python app from Microsoft Store) or placed
    in the target directory for other platforms; it is recommended
    NOT to use an extension (automatically added ".ico" on Windows,
    ".icns" on macOS and ".png" or ".svg" on Linux and others)

.. option:: --manifest=NAME

    the name of manifest which should be included in the executable itself
    (Windows only - ignored by Python app from Microsoft Store)

.. option:: --uac-admin

    creates a manifest for an application that will request elevation
    (Windows only - ignored by Python app from Microsoft Store)

.. option:: --uac-uiaccess

    changes the application manifest to bypass user interface control
    (Windows only - ignored by Python app from Microsoft Store)

.. option:: --shortcut-name=NAME

    the name to give a shortcut for the executable when included in
    an MSI package (Windows only)

.. option:: --shortcut-dir=DIR

    the directory in which to place the shortcut when being
    installed by an MSI package; see the MSI Shortcut table documentation
    for more information on what values can be placed here (Windows only)

.. option:: --copyright

    the copyright value to include in the version resource
    associated with executable (Windows only)

.. option:: --trademarks

    the trademarks value to include in the version resource
    associated with the executable (Windows only)

.. option:: --debug

    print debug information

.. option:: --verbose

    run verbosely

.. option:: --version

   show program's version number and exit

.. option:: -h, --help

   show this help message and exit

.. versionadded:: 6.10
    ``manifest`` and ``uac-admin`` options.

.. versionadded:: 7.0
    ``uac-uiaccess`` option.

.. versionadded:: 8.0
    ``debug`` and  ``verbose`` options.
