bdist_appimage
==============

AppImage
--------

An `AppImage <https://docs.appimage.org/>`_ is a downloadable file for Linux
[1]_ that contains an application and everything the application needs to run
(e.g., libraries, icons, fonts, translations, etc.) that cannot be reasonably
expected to be part of each target system.

AppImages are simple to understand. Every AppImage is a regular file, and every
AppImage contains exactly one app with all its dependencies. Once the AppImage
is made executable, a user can just run it, either by double clicking it in
their desktop environment’s file manager, by running it from the console etc.

It is crucial to understand that AppImage is merely a format for distributing
applications. In this regard, AppImage is like a :file:`.zip` file or an
:file:`.iso` file.

.. seealso::
  `AppImage | Linux apps that run anywhere <https://appimage.org/>`_

bdist_appimage command options
------------------------------

When :program:`cx_Freeze` calls :program:`appimagetool` to create an AppImage
application bundle, it builds a read-only image of a :ref:`cx_freeze_build_exe`
directory, then prepends the runtime file, the entrypoint, a desktop file,
icon from :option:`Executable.icon <icon>` option (or a default icon)
and an optional update information, and finally marks the :file:`.AppImage`
file as executable.

The following options were added to the standard set of options for the
command:

.. tabs::

   .. group-tab:: pyproject.toml

      .. code-block:: console

        cxfreeze bdist_appimage

   .. group-tab:: setup.py

      .. code-block:: console

        python setup.py bdist_appimage

.. list-table::
   :header-rows: 1
   :widths: 350 600
   :width: 100%

   * - option name, command line equivalent
     - description
   * - .. option:: appimagetool, --appimagetool
     - path to appimagetool [default: the latest version is downloaded]
   * - .. option:: runtime_file, --runtime-file
     - path to type2 runtime [default: the latest version is downloaded]
   * - .. option:: sign, --sign
     - Sign with gpg or gpg2
   * - .. option:: sign_key, --sign-key
     - Key ID to use for gpg/gpg2 signatures
   * - .. option:: updateinformation, --updateinformation
     - Embed update information STRING (or 'guess') and generate zsync file;
   * - .. option:: target_name, --target-name
     - name of the file to create; if the name ends with ".AppImage"
       then it is used verbatim, otherwise, information about the
       program version and platform will be added to the installer name
       [default: metadata name or the name of the first executable]
   * - .. option:: target_version, --target-version
     - version of the file to create [default: metadata version if available]
   * - .. option:: bdist_base, --bdist-base
     - base directory for creating built distributions
   * - .. option:: build_dir, --build-dir, -b
     - directory of built executables and dependent files
   * - .. option:: dist_dir, --dist-dir, -d
     - directory to put final built distributions in [default: "dist"]
   * - .. option:: skip_build, --skip-build
     - skip rebuilding everything (for testing/debugging)
   * - .. option:: silent, --silent, -s
     - suppress all output except warnings

.. versionadded:: 7.0
   :doc:`bdist_appimage` command.
.. versionchanged:: 8.5
   Renamed the ``appimagekit`` option to :option:`appimagetool` option.
.. versionadded:: 8.5
   :option:`runtime_file`, :option:`sign`, :option:`sign_key` and
   :option:`updateinformation` options.

Signing AppImages
-----------------

AppImages can be digitally signed by the person that who produced the AppImage,
who at creation time uses :option:`sign` or :option:`sign_key` options.

.. seealso::
  `Signing AppImages <https://docs.appimage.org/packaging-guide/optional/signatures.html>`_

Making AppImages updateable
---------------------------

.. % https://docs.appimage.org/packaging-guide/optional/updates.html#making-appimages-updateable-via-external-tools

To make an AppImage updateable, you need to embed information that describes
where to check for updates and how into the AppImage. The update information
always travels alongside the application, so that the end user does not have
to do anything special in order to be able to check for updates.

.. % https://docs.appimage.org/packaging-guide/optional/updates.html#using-appimagetool

Use :option:`updateinformation` to embed update information (as specified in
the AppImageSpec) and generate the corresponding :file:`.zsync` file you can
upload to the place mentioned in the update information.
A special value **guess** can be used to guess update information based on
GitHub or GitLab environment variables.


Here is an example of usage:

.. tabs::

   .. group-tab:: pyproject.toml

      .. code-block:: toml

        [tool.cxfreeze.bdist_appimage]
        updateinformation = "zsync|https://example.com/path/simple/simple.AppImage.zsync"


   .. group-tab:: setup.py

      .. code-block:: python

        TODO

The string "zsync|..." is called the *update information*.

.. seealso::
  `AppImageSpec | update-information <https://github.com/AppImage/AppImageSpec/blob/master/draft.md#update-information>`_


------------------

.. [1] AppImage is for Linux (and compatible systems such as Windows with
   WSL2 and FreeBSD with the Linuxulator).
