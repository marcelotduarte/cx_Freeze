bdist_msi
=========

This command is a standard command in Python 2.5 and higher which has been
modified by cx_Freeze to handle installing executables and their dependencies.
The following options were added to the standard set of options for the
command:

.. list-table::
   :header-rows: 1
   :widths: 250 550
   :width: 100%

   * - option name
     - description
   * - .. option:: add_to_path
     - add the target directory to the PATH environment variable; the default
       value is True if there are any console-based executables and False
       otherwise.
   * - .. option:: all_users
     - install for all users; the default value is False and results in an
       installation for just the installing user.
   * - .. option:: data
     - dictionary of arbitrary MSI data indexed by table name; for each table,
       a list of tuples should be provided, representing the rows that should
       be added to the table. For binary values (e.g. Icon.Data), pass the path
       to the file containing the data.
   * - .. option:: summary_data
     - dictionary of data to include in MSI summary information stream
       (allowable keys are "author", "comments", and "keywords").
   * - .. option:: directories
     - list of directories that should be created during installation.
   * - .. option:: environment_variables
     - list of environment variables that should be added to the system during
       installation.
   * - .. option:: initial_target_dir
     - defines the initial target directory supplied to the user during
       installation; to specify a target directory of "XYZ" in the
       default program directory use "[ProgramFiles64Folder]\XYZ" or
       "[ProgramFilesFolder]\XYZ" (for the default 64-bit or non-64-bit
       locations, respectively).
   * - .. option:: install_icon
     - path of icon to use for the add/remove programs window that pops up
       during installation.
   * - .. option:: product_code
     - define the product code for the package that is created.
   * - .. option:: target_name
     - specifies the name of the file that is to be created; if the name
       ends with ".msi" then it is used verbatim, otherwise, information
       about the program version and platform will be added to the installer
       name.
   * - .. option:: upgrade_code
     - define the GUID of the upgrade code for the package that is created;
       this is used to force the removal of any packages created with the same
       upgrade code before the installation of this one; the valid format for
       a GUID is {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX} where X is a hex digit.
       Refer to `Windows GUID
       <https://docs.microsoft.com/en-us/windows/win32/api/guiddef/ns-guiddef-guid>`_.
   * - .. option:: extensions
     - list of dictionaries specifying the extensions that the installed program
       handles. Each extension needs to specify at least the extension, a verb,
       and an executable. Additional allowed keys are `argument` to specify
       the invocation of the executable, `mime` for the extension’s mime type,
       and `context` for the context menu text.
   * - .. option:: license-file
     - path to an rtf formmated file to be used as the license agreement.

.. versionadded:: 6.7
    ``extensions`` option.


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
            copyright="Copyright (C) 2024 cx_Freeze",
            base="gui",
            icon="icon.ico",
            shortcut_name="My Program Name",
            shortcut_dir="MyProgramMenu",
        )
    ]

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
There are more examples in the :repository:`samples <tree/main/samples/>`
directory.

.. seealso:: `Windows Installer
   <https://docs.microsoft.com/en-us/windows/win32/msi/windows-installer-portal>`_
