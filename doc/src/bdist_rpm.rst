bdist_rpm
=========

Creating RPM packages
---------------------

The RPM format is used by many popular Linux distributions, including Red Hat,
Fedora, and AlmaLinux.  If one of these (or any of the other RPM-based Linux
distributions) is your usual environment, creating RPM packages for other users
of that same distribution is trivial. Depending on the complexity of your
module distribution and differences between Linux distributions, you may also
be able to create RPMs that work on different RPM-based distributions.

The usual way to create an RPM of your module distribution is to run the
:command:`bdist_rpm` command:

   .. tab:: pyproject.toml

      .. code-block:: console

        cxfreeze bdist_rpm

   .. tab:: setup.py

      .. code-block:: console

        python setup.py bdist_rpm

The command allows you to specify RPM-specific options:

   .. tab:: pyproject.toml

      .. code-block:: console

        cxfreeze bdist_rpm --packager="John Doe <jdoe@example.org>"

   .. tab:: setup.py

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
   * - .. option:: long-description
     - %description (section)

Additionally, there are many options in :file:`.spec` files that don't have
corresponding options in the setup script.  Most of these are handled through
options to the :command:`bdist_rpm` command as follows:

.. option:: bdist-base

    base directory for creating built distributions

.. option:: rpm-base

    directory for creating RPM
    [default: "rpm" under :option:`bdist-base`]

.. option:: dist-dir

    directory to put final RPM file in (and .spec file if
    :option:`spec-only` is used)
    [default: "dist"]

.. option:: spec-only

   only regenerate spec file

.. option:: distribution-name

   name of the (Linux) distribution to which this
   RPM applies (*not* the name of the module distribution!)
   [default: none]
   RPM :file:`.spec` file option or section: Distribution

.. option:: group

   package classification
   [default: "Development/Libraries"]
   RPM :file:`.spec` file option or section: Group

.. option:: release

   RPM release number [default: "1"]
   RPM :file:`.spec` file option or section: Release

.. option:: serial

   RPM serial number [default: "1"]
   RPM :file:`.spec` file option or section: Serial

.. option:: vendor

   RPM "vendor" (eg. "Joe Blow <joe@example.com>")
   [default: maintainer or author from setup script]
   RPM :file:`.spec` file option or section: Vendor

.. option:: packager

   RPM packager (eg. "Jane Doe <jane@example.net>
   [default: same as vendor]
   RPM :file:`.spec` file option or section: Packager

.. option:: doc-files

   list of documentation files (space or comma-separated)
   RPM :file:`.spec` file option or section: %doc

.. option:: changelog

   RPM changelog
   RPM :file:`.spec` file option or section: %changelog

.. option:: icon

   name of icon file [default: none]
   RPM :file:`.spec` file option or section: Icon

.. option:: provides

   capabilities provided by this package [default: none]
   RPM :file:`.spec` file option or section: Provides

.. option:: requires

   capabilities required by this package [default: none]
   RPM :file:`.spec` file option or section: Requires

.. option:: conflicts

   capabilities which conflict with this package
   [default: none]
   RPM :file:`.spec` file option or section: Conflicts

.. option:: build-requires

   capabilities required to build this package[default: none]
   RPM :file:`.spec` file option or section: BuildRequires

.. option:: obsoletes

   capabilities made obsolete by this package
   [default: none]
   RPM :file:`.spec` file option or section: Obsoletes

.. % FIXME: describe the remaining options

Obviously, supplying even a few of these options on the command line would be
tedious and error-prone, so it's usually best to put them in the
``pyproject.toml`` configuration file \ --- see section :doc:`setup_script`.

.. % FIXME: ---see section :doc:`setup_script`.

There are three steps to building a binary RPM package, all of which are
handled automatically by the cx_Freeze:

#. create a :file:`.spec` file, which describes the package (analogous to the
   cx_Freeze setup script; in fact, much of the information in the setup script
   winds up in the :file:`.spec` file).

#. build an executable or set of executables

#. create the "binary" RPM

.. % FIXME: define title to explain :option:`spec-only` option

If you wish, you can separate these three steps.  You can use the
:option:`spec-only` option to make :command:`bdist_rpm` just create the
:file:`.spec` file and exit; in this case, the :file:`.spec` file will be
written to the "distribution directory" ---normally :file:`dist/`, but
customizable with the :option:`dist-dir` option.  (Normally, the :file:`.spec`
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
