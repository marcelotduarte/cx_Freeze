.. _bdist_appimage:

bdist_appimage
``````````````

This command is available on Linux systems, to create a AppImage application
bundle (a .AppImage file); bdist_appimage automates the process.

An AppImage is a downloadable file for Linux that contains an application and
everything the application needs to run (e.g., libraries, icons, fonts,
translations, etc.) that cannot be reasonably expected to be part of each
target system.

.. versionadded:: 7.0

.. list-table::
   :header-rows: 1
   :widths: 240 560
   :width: 100%

   * - option name
     - description
   * - .. option:: appimagekit
     - path to AppImageKit (download the latest version if not specified).
   * - .. option:: bdist_dir
     - temporary directory for creating the distribution
   * - .. option:: dist_dir (-d)
     - directory to put final built distributions in (default: dist)
   * - .. option:: skip_build
     - skip rebuilding everything (for testing/debugging)
   * - .. option:: target_name
     - name of the file to create
   * - .. option:: target_version
     - version of the file to create
   * - .. option:: silent (-s)
     - suppress all output except warnings

This is the equivalent help to specify the same options on the command line:

  .. code-block:: console

    python setup.py bdist_appimage --help

.. seealso::
  `AppImage | Linux apps that run anywhere <https://appimage.org/>`_

  `AppImage documentation <https://docs.appimage.org/>`_
