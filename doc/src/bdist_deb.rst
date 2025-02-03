bdist_deb
=========

This command is available on Linux systems; It is a simple wrapper around
'alien' that creates an RPM distribution, then converts to a DEB distribution.

.. versionadded:: 7.0

Please check the options on the command line:

.. tabs::

   .. group-tab:: pyproject.toml

      .. code-block:: console

        cxfreeze bdist_deb --help

   .. group-tab:: setup.py

      .. code-block:: console

        python setup.py bdist_deb --help
