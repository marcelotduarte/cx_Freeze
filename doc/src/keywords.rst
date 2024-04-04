========
Keywords
========

The following are keywords ``cx_Freeze.setup()`` accepts, some of them are
inherited from ``setuptools.setup()``.
They allow configuring the build process for a Python distribution or adding
metadata via a ``setup.py`` script placed at the root of your project.

The keyword ``executables`` is required, while all inherited keywords are
optional; you do not have to supply them unless you need the associated
``cx_Freeze`` feature.

Metadata and configuration supplied via ``setup()`` is complementary to (and
may be overwritten by) the information present in ``setup.cfg`` and
``pyproject.toml``.
Some important metadata, such as ``name`` and ``version``, may assume
a default *degenerate* value if not specified.

.. warning::
   cx_Freeze inherits keywords, metadata and configuration from setuptools,
   but it is a software layer on top, to generate executables.

Users are strongly encouraged to use a declarative config via
:setuptools:`pyproject.toml <userguide/pyproject_config.html>`.

.. _keyword/executables:

``executables``
    A list of :ref:`cx_freeze_executable`, a mapping list (with the same
    key/value as Executable), or a list of strings (with only the script key of
    Executable). Required.

    .. note::
       When using declarative configs via ``setup.cfg``, executables
       metadata isn't recognized.

.. _keyword/name:

``name``
    A string specifying the name of the package.

.. _keyword/version:

``version``
    A string specifying the version number of the package.

.. _keyword/description:

``description``
    A string describing the package in a single line.

.. _keyword/long_description:

``long_description``
    A string providing a longer description of the package.

.. _keyword/long_description_content_type:

``long_description_content_type``
    A string specifying the content type is used for the ``long_description``
    (e.g. ``text/markdown``)

.. _keyword/author:

``author``
    A string specifying the author of the package.

.. _keyword/author_email:

``author_email``
    A string specifying the email address of the package author.

.. _keyword/maintainer:

``maintainer``
    A string specifying the name of the current maintainer, if different from
    the author. Note that if the maintainer is provided, setuptools will use it
    as the author in ``PKG-INFO``.

.. _keyword/maintainer_email:

``maintainer_email``
    A string specifying the email address of the current maintainer, if
    different from the author.

.. _keyword/url:

``url``
    A string specifying the URL for the package homepage.

.. _keyword/download_url:

``download_url``
    A string specifying the URL to download the package.

.. _keyword/options:

``options``
    A dictionary providing the default options for the setup script.

.. _keyword/license:

``license``
    A string specifying the license of the package.

.. _keyword/license_files:

``license_files``
    A list of glob patterns for license-related files that should be included.
    If neither ``license_file`` nor ``license_files`` is specified, this option
    defaults to ``LICEN[CS]E*``, ``COPYING*``, ``NOTICE*``, and ``AUTHORS*``.

.. _keyword/keywords:

``keywords``
    A list of strings or a comma-separated string providing descriptive
    meta-data.

.. _keyword/project_urls:

``project_urls``
    An arbitrary map of URL names to hyperlinks, allowing more extensible
    documentation of where various resources can be found than the simple
    ``url`` and ``download_url`` options provide.
