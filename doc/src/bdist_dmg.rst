bdist_dmg
=========

This command is available on Mac OS X systems; it creates an application
bundle, then package it into a DMG disk image suitable for distribution and
installation.

.. list-table::
   :header-rows: 1
   :widths: 240 560
   :width: 100%

   * - option name
     - description
   * - .. option:: volume_label
     - Volume label of the DMG disk image
   * - .. option:: applications_shortcut
     - Boolean for whether to include shortcuts to Applications in the DMG disk
       image
   * - .. option:: silent (-s)
     - suppress all output except warnings
   * - .. option:: format
     - Format of the DMG disk image [default: "UDZO"]
   * - .. option:: filesystem
     - Filesystem of the DMG disk image [default: "HFS+"]
   * - .. option:: size
     - If defined, specifies the size of the filesystem within the image.
       If this is not defined, cx_Freeze (and then dmgbuild) will attempt to
       determine a reasonable size for the image. If you set this, you should
       set it large enough to hold the files you intend to copy into the image.
       The syntax is the same as for the -size argument to hdiutil, i.e. you
       can use the suffixes `b`, `k`, `m`, `g`, `t`, `p` and `e` for bytes,
       kilobytes,megabytes, gigabytes, terabytes, exabytes and petabytes
       respectively.
   * - .. option:: background
     - A rgb color in the form #3344ff, svg named color like goldenrod, a path
       to an image, or the words 'builtin-arrow'. [default: None]
   * - .. option:: show_status_bar
     - Show the status bar in the Finder window. [default: False]
   * - .. option:: show_tab_view
     - Show the tab view in the Finder window. [default: False]
   * - .. option:: show_path_bar
     - Show the path bar in the Finder window. [default: False]
   * - .. option:: show_sidebar
     - Show the sidebar in the Finder window. [default: False]
   * - .. option:: sidebar_width
     - Width of the sidebar in the Finder window. [default: None]
   * - .. option:: windows_rect
     - Window rectangle in the form x, y, width, height. The position of the
       window in ((x, y), (w, h)) format, with y coordinates running from
       bottom to top. The Finder makes sure that the window will be on the
       user's display, so if you want your window at the top left of the
       display you could use (0, 100000) as the x, y coordinates. Unfortunately
       it doesn't appear to be possible to position the window relative to the
       top left or relative to the centre of the user's screen.
   * - .. option:: icon_locations
     - A dictionary specifying the coordinates of items in the root directory
       of the disk image, where the keys are filenames and the values are
       (x, y) tuples. For example,
       icon_locations = {"Applications": (100, 100), "README.txt": (200, 100)}
   * - .. option:: default_view
     - The default view of the Finder window. Possible values are
       "icon-view", "list-view", "column-view", "coverflow".
   * - .. option:: show_icon_preview
     - Show icon preview in the Finder window. [default: False]
   * - .. option:: license
     - Dictionary specifying license details with 'default-language',
       'licenses', and 'buttons'.

       default-language: Language code (e.g., 'en_US') if no matching system
       language.
       licenses: Map of language codes to license file paths
       (e.g., {'en_US': 'path/to/license_en.txt'}).
       buttons: Map of language codes to UI strings
       ([language, agree, disagree, print, save, instruction]).
       Example: {'default-language': 'en_US', 'licenses':
       {'en_US': 'path/to/license_en.txt'},
       'buttons': {'en_US': ['English', 'Agree', 'Disagree', 'Print', 'Save',
       'Instruction text']}}

.. versionadded:: 7.2
    ``format``, ``filesystem``, ``size``, ``background``, ``show_status_bar``,
    ``show_tab_view``, ``show_path_bar``, ``show_sidebar``, ``sidebar_width``,
    ``windows_rect``, ``icon_locations``, ``default_view``, ``show_icon_preview``,
    ``license`` options.

The above options come from the `dmgbuild` package. For more information, see
the `dmgbuild documentation <https://dmgbuild.readthedocs.io/en/latest/>`_.

This is the equivalent help to specify the same options on the command line:

.. tabs::

   .. group-tab:: pyproject.toml

      .. code-block:: console

        cxfreeze bdist_dmg --help

   .. group-tab:: setup.py

      .. code-block:: console

        python setup.py bdist_dmg --help
