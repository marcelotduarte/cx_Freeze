****************************
Creating Built Distributions
****************************

A "built distribution" is what you're probably used to thinking of either as a
"binary package" or an "installer" (depending on your background).  It's not
necessarily binary, though, because it might contain bytecode.  (And
"installer" is a term specific to the world of mainstream desktop systems.)

A built distribution is how you make life as easy as possible for installers of
your module distribution: for users of RPM-based Linux systems, it's a binary
RPM; for Windows users, it's an executable installer; for Debian-based Linux
users, it's a Debian package; and so forth.

The available commands for built distributions are:

.. toctree::
   :maxdepth: 2
   :hidden:

   bdist_appimage.rst
   bdist_deb.rst
   bdist_dmg.rst
   bdist_mac.rst
   bdist_msi.rst
   bdist_rpm.rst

+-----------------------+---------------------------------------+-----------+
| Command               | Description                           | Notes     |
+=======================+=======================================+===========+
| :doc:`bdist_appimage` | AppImage application bundle           | \(1)      |
|                       | (:file:`.AppImage`)                   |           |
+-----------------------+---------------------------------------+-----------+
| :doc:`bdist_deb`      | DEB distribution (:file:`.deb`)       | \(2) \(3) |
+-----------------------+---------------------------------------+-----------+
| :doc:`bdist_dmg`      | DMG disk image (:file:`.dmg`)         |           |
+-----------------------+---------------------------------------+-----------+
| :doc:`bdist_mac`      | Mac application bundle (:file:`.app`) |           |
+-----------------------+---------------------------------------+-----------+
| :doc:`bdist_msi`      | Windows installer (:file:`.msi`)      |           |
+-----------------------+---------------------------------------+-----------+
| :doc:`bdist_rpm`      | RPM distribution (:file:`.rpm`)       | \(3)      |
+-----------------------+---------------------------------------+-----------+

.. versionadded:: 7.0
   Support for the ``bdist_appimage`` and ``bdist_deb`` commands.

.. note::

   #. requires external :program:`AppImageKit`
      (the latest version is downloaded if not specified or not found).

   #. requires external :program:`alien` and :program:`fakeroot` utilities.

   #. requires external :program:`rpm` utility, version 3.0.4 or better
      (use ``rpm --version`` to find out which version you have).
