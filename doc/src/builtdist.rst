.. _built_dist:

****************************
Creating Built Distributions
****************************

A "built distribution" is what you're probably used to thinking of either as a
"binary package" or an "installer" (depending on your background).  It's not
necessarily binary, though, because it might contain byte-code.  (And
"installer" is a term specific to the world of mainstream desktop systems.)

A built distribution is how you make life as easy as possible for installers of
your module distribution: for users of RPM-based Linux systems, it's a binary
RPM; for Windows users, it's an executable installer; for Debian-based Linux
users, it's a Debian package; and so forth.

The available commands for built distributions are:

+--------------------+----------------------------------+-----------+
| Command            | Description                      | Notes     |
+====================+==================================+===========+
| ``bdist_appimage`` | AppImage application bundle      | \(1)      |
|                    | (:file:`.AppImage`)              |           |
+--------------------+----------------------------------+-----------+
| ``bdist_deb``      | DEB distribution (:file:`.deb`)  | \(2) \(3) |
+--------------------+----------------------------------+-----------+
| ``bdist_dmg``      | DMG disk image (:file:`.dmg`)    |           |
+--------------------+----------------------------------+-----------+
| ``bdist_mac``      | Mac application bundle           |           |
|                    | (:file:`.app`)                   |           |
+--------------------+----------------------------------+-----------+
| ``bdist_msi``      | Windows installer (:file:`.msi`) |           |
+--------------------+----------------------------------+-----------+
| ``bdist_rpm``      | RPM distribution (:file:`.rpm`)  | \(3)      |
+--------------------+----------------------------------+-----------+

.. versionadded:: 7.0
   Support for the ``bdist_appimage`` and ``bdist_deb`` commands.

.. note::

   #. requires external :program:`AppImageKit`
      (the latest version is downloaded if not specified or not found).

   #. requires external :program:`alien` and :program:`fakeroot` utilities.

   #. requires external :program:`rpm` utility, version 3.0.4 or better
      (use ``rpm --version`` to find out which version you have).

The following sections give details on the individual :command:`bdist_\*`
commands.

.. _bdist_appimage:

.. include:: bdist_appimage.rst

.. _bdist_deb:

.. include:: bdist_deb.rst

.. _bdist_dmg:

.. include:: bdist_dmg.rst

.. _bdist_mac:

.. include:: bdist_mac.rst

.. _bdist_msi:

.. include:: bdist_msi.rst

.. _bdist_rpm:

.. include:: bdist_rpm.rst
