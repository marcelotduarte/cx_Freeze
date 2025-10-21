Welcome to cx_Freeze's documentation!
=====================================

**cx_Freeze**
creates standalone executables from Python scripts with the same performance
as the original script. It is cross-platform and should work on any platform
that Python runs on.

The current version of **cx_Freeze** is |version|
that supports Python_ 3.10 to 3.14,
providing on pypi, wheels for Linux (x86_64, aarch64, ppc64le),
macOS (universal2) and Windows (win32, win_amd64, win_arm64).

.. versionadded:: 8.0
   Python 3.13 support on all popular systems and architectures.
.. versionadded:: 8.0
   Python 3.13t support (experimental free-threading) on
   Linux (x86_64, aarch64) and macOS (universal2).
.. versionadded:: 8.3
   Support Python 3.11 to 3.13 on Windows ARM64 (win_arm64).
.. versionchanged:: 8.3
   Support for Python 3.11 to 3.13 on lesser-known Linux platforms
   (aarch64, ppc64le) and musl variants.

**cx_Freeze** is distributed under an open-source :ref:`PSF license <license>`.

Contents:

.. toctree::
   :maxdepth: 2

   installation.rst
   overview.rst
   script.rst
   setup_script.rst
   keywords.rst
   builtdist.rst
   faq.rst
   releasenotes.rst
   versions.rst
   development/index.rst
   license.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _py2exe: https://pypi.org/project/py2exe/
.. _py2app: https://pypi.org/project/py2app/
.. _Python: https://www.python.org/
