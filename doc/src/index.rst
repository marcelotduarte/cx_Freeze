Welcome to cx_Freeze's documentation!
=====================================

:program:`cx_Freeze`
creates standalone executables from Python scripts with the same performance
as the original script. It is cross-platform and should work on any platform
that Python runs on.

The current version of :program:`cx_Freeze` is |version|
that supports Python_ 3.10 to 3.14, including free-threading versions.

.. versionchanged:: 8.5
   cx_Freeze was separated into two distinct packages: cx_Freeze and
   freeze-core. Therefore, support for different platforms depends on
   freeze-core.

:program:`cx_Freeze` is distributed under an open-source
:ref:`PSF license <license>`.

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
