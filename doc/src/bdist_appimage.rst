bdist_appimage
==============

An `AppImage <https://docs.appimage.org/>`_ is a downloadable file for Linux
that contains an application and everything the application needs to run
(e.g., libraries, icons, fonts, translations, etc.) that cannot be reasonably
expected to be part of each target system.

AppImages are simple to understand. Every AppImage is a regular file, and every
AppImage contains exactly one app with all its dependencies. Once the AppImage
is made executable, a user can just run it, either by double clicking it in
their desktop environment’s file manager, by running it from the console etc.

It is crucial to understand that AppImage is merely a format for distributing
applications. In this regard, AppImage is like a `.zip` file or an `.iso` file.

When cx_Freeze calls appimagetool to create an AppImage application bundle
(an :file:`.AppImage` file), it builds a read-only image of a
:ref:`cx_freeze_build_exe` directory, then prepends the runtime, and marks the
file executable.

.. list-table::
   :header-rows: 1
   :widths: 240 560
   :width: 100%

   * - option name
     - description
   * - .. option:: appimagekit
     - path to AppImageKit [default: the latest version is downloaded]
   * - .. option:: bdist_base
     - base directory for creating built distributions
   * - .. option:: build_dir (-b)
     - directory of built executables and dependent files
   * - .. option:: dist_dir (-d)
     - directory to put final built distributions in [default: "dist"]
   * - .. option:: skip_build
     - skip rebuilding everything (for testing/debugging)
   * - .. option:: target_name
     - name of the file to create; if the name ends with ".AppImage"
       then it is used verbatim, otherwise, information about the
       program version and platform will be added to the installer name
       [default: metadata name or the name of the first executable].
   * - .. option:: target_version
     - version of the file to create [default: metadata version if available]
   * - .. option:: silent (-s)
     - suppress all output except warnings

.. versionadded:: 7.0


To specify the same options on the command line, this is the help command that
shows the equivalent options:

.. tabs::

   .. group-tab:: pyproject.toml

      .. code-block:: console

        cxfreeze bdist_appimage --help

   .. group-tab:: setup.py

      .. code-block:: console

        python setup.py bdist_appimage --help

.. seealso::
  `AppImage | Linux apps that run anywhere <https://appimage.org/>`_
