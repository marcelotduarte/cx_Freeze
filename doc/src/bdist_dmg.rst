bdist_dmg
`````````

This command is available on Mac OS X systems; it creates an application
bundle, then packages it into a DMG disk image suitable for distribution and
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
     - Boolean for whether to include shortcut to Applications in the DMG disk
       image
   * - .. option:: silent (-s)
     - suppress all output except warnings

This is the equivalent help to specify the same options on the command line:

  .. code-block:: console

    python setup.py bdist_dmg --help
