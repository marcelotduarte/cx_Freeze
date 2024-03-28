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


.. _bdist_rpm:

bdist_rpm: Creating RPM packages
================================

The RPM format is used by many popular Linux distributions, including Red Hat,
SuSE, and Mandrake.  If one of these (or any of the other RPM-based Linux
distributions) is your usual environment, creating RPM packages for other users
of that same distribution is trivial. Depending on the complexity of your module
distribution and differences between Linux distributions, you may also be able
to create RPMs that work on different RPM-based distributions.

The usual way to create an RPM of your module distribution is to run the
:command:`bdist_rpm` command:

  .. code-block:: console

    python setup.py bdist_rpm

The command allows you to specify RPM-specific options:

  .. code-block:: console

    python setup.py bdist_rpm --packager="John Doe <jdoe@example.org>"

Creating RPM packages is driven by a :file:`.spec` file, much as using the
cx_Freeze is driven by the setup script.  To make your life easier, the
:command:`bdist_rpm` command normally creates a :file:`.spec` file based on the
information you supply in the setup script, on the command line, and in any
cx_Freeze configuration files.  Various options and sections in the
:file:`.spec` file are derived from options in the setup script as follows:

.. list-table::
   :header-rows: 1
   :widths: 200 300
   :width: 100%

   * - cx_Freeze setup script option
     - RPM :file:`.spec` file option or section
   * - .. option:: name
     - Name
   * - .. option:: description
     - Summary (in preamble)
   * - .. option:: version
     - Version
   * - .. option:: license
     - Copyright
   * - .. option:: url
     - Url
   * - .. option:: long_description
     - %description (section)

Additionally, there are many options in :file:`.spec` files that don't have
corresponding options in the setup script.  Most of these are handled through
options to the :command:`bdist_rpm` command as follows:

.. list-table::
   :header-rows: 1
   :widths: 200 300 300
   :width: 100%

   * - :command:`bdist_rpm` option
     - RPM :file:`.spec` file option or section
     - default value
   * - .. option:: distribution_name
     - Distribution
     - (none)
   * - .. option:: group
     - Group
     - "Development/Libraries"
   * - .. option:: release
     - Release
     - "1"
   * - .. option:: serial
     - Serial
     - "1"
   * - .. option:: vendor
     - Vendor
     - maintainer or author from setup script
   * - .. option:: packager
     - Packager
     - (none)
   * - .. option:: provides
     - Provides
     - (none)
   * - .. option:: requires
     - Requires
     - (none)
   * - .. option:: conflicts
     - Conflicts
     - (none)
   * - .. option:: obsoletes
     - Obsoletes
     - (none)
   * - .. option:: build_requires
     - BuildRequires
     - (none)
   * - .. option:: icon
     - Icon
     - (none)

Obviously, supplying even a few of these options on the command-line would be
tedious and error-prone, so it's usually best to put them in the
``pyproject.toml`` configuration file \ ---see section :ref:`setup-config`.

.. % FIXME

There are three steps to building a binary RPM package, all of which are
handled automatically by the cx_Freeze:

#. create a :file:`.spec` file, which describes the package (analogous to the
   cx_Freeze setup script; in fact, much of the information in the setup script
   winds up in the :file:`.spec` file).

#. build an executable or set of executables

#. create the "binary" RPM

If you wish, you can separate these three steps.  You can use the
:option:`!--spec-only` option to make :command:`bdist_rpm` just create the
:file:`.spec` file and exit; in this case, the :file:`.spec` file will be
written to the "distribution directory"---normally :file:`dist/`, but
customizable with the :option:`!--dist-dir` option.  (Normally, the :file:`.spec`
file winds up deep in the "build tree," in a temporary directory created by
:command:`bdist_rpm`.)

.. % \ begin{verbatim}
.. % > python setup.py bdist_rpm --spec-only
.. % # ...edit dist/FooBar-1.0.spec
.. % > python setup.py bdist_rpm --spec-file=dist/FooBar-1.0.spec
.. % \ end{verbatim}
.. %
.. % (Although a better way to do this is probably to override the standard
.. % \command{bdist\_rpm} command with one that writes whatever else you want
.. % to the \file{.spec} file.)
