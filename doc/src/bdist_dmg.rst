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
     - Format of the DMG disk image Default is UDZO
   * - .. option:: filesystem
     - Filesystem of the DMG disk image Default is HFS+
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
       to an image, or the words 'builtin-arrow'. Default is None.
   * - .. option:: show-status-bar
     - Show the status bar in the Finder window. Default is False.
   * - .. option:: show-tab-view
     - Show the tab view in the Finder window. Default is False.
   * - .. option:: show-path-bar
     - Show the path bar in the Finder window. Default is False.
   * - .. option:: show-sidebar
     - Show the sidebar in the Finder window. Default is False.
   * - .. option:: sidebar-width
     - Width of the sidebar in the Finder window. Default is None.
   * - .. option:: windows-rect
     - Window rectangle in the form x,y,width,height"
       The position of the window in ((x, y), (w, h)) format, with y co-ordinates
       running from bottom to top. The Finder makes sure that the window will be
       on the user's display, so if you want your window at the top left of the
       display you could use (0, 100000) as the x, y co-ordinates. Unfortunately
       it doesn't appear to be possible to position the window relative to the top
       left or relative to the centre of the user's screen.
   * - .. option:: icon-locations
     - A dictionary specifying the co-ordinates of items in the root directory of
       the disk image, where the keys are filenames and the values are (x, y)
       tuples. For example, 
       icon-locations = { "Applications": (100, 100), "README.txt": (200, 100) }
   * - .. option:: default-view
     - The default view of the Finder window. Possible values are
       "icon-view", "list-view", "column-view", "coverflow".
   * - .. option:: show-icon-preview
     - Show icon preview in the Finder window. Default is False.
   * - .. option:: license
     - Dictionary specifying license details with 'default-language', 'licenses', and
       'buttons'.

       default-language: Language code (e.g., 'en_US') if no matching system
       language.
       licenses: Map of language codes to license file paths
       (e.g., {'en_US': 'path/to/license_en.txt'}).
       buttons: Map of language codes to UI strings
       ([language, agree, disagree, print, save, instruction]).
       Example: {'default-language': 'en_US', 'licenses': {'en_US': 'path/to/license_en.txt'},
       'buttons': {'en_US': ['English', 'Agree', 'Disagree', 'Print', 'Save',
       'Instruction text']}}


This is the equivalent help to specify the same options on the command line:

  .. code-block:: console

    python setup.py bdist_dmg --help
