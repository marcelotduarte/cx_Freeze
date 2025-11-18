Installation
============

Choose the Python package manager according to your system. See how the
installation works with the most common ones.

.. tabs::

   .. group-tab:: pip

      To install the latest version of :pypi:`cx_Freeze` using :pypi:`pip` into
      a virtual environment:

      .. code-block:: console

         pip install --upgrade cx_Freeze

   .. group-tab:: uv

      .. code-block:: console

         uv pip install --upgrade cx_Freeze

   .. group-tab:: conda

      Installing cx_freeze from the conda-forge channel can be achieved with
      the command:

      .. code-block:: console

         conda install conda-forge:cx_freeze

      .. seealso:: `cx_freeze-feedstock
         <https://github.com/conda-forge/cx_freeze-feedstock#installing-cx_freeze>`_.

.. note::
  The recommended way to use cx_Freeze is in a virtual environment such as
  those provided by :pythondocs:`python -m venv <library/venv.html>`,
  `uv venv <https://docs.astral.sh/uv/pip/environments/>`_ or
  `conda <https://docs.conda.io/projects/conda/en/stable/>`_.
  If you're unfamiliar with Python virtual environments, check out the
  :packaging:`packaging user guide
  <guides/installing-using-pip-and-virtual-environments>`.

.. important::
  Please note that some operating systems might be equipped with the python3
  and pip3 commands instead of python and pip (but they should be equivalent).

.. _python_requirements:

Python requirements
-------------------

Python requirements are installed automatically by pip or conda.

  .. code-block:: console

   freeze-core >= 0.4.0
   packaging >= 24
   setuptools >= 78.1.1,<81
   tomli >= 2.0.1           #  Python 3.10, Python 3.11+ has tomllib
   filelock >= 3.15.3       #  Linux
   patchelf >= 0.14,<0.18   #  Linux
   dmgbuild >= 1.6.1        #  macOS
   lief >= 0.15.1           #  Windows
   python-msilib >= 0.4.1   #  Python 3.13+ on Windows

.. note::

   #. If you have trouble with patchelf, check :ref:`patchelf`.
   #. ``lief`` in conda-forge is named ``py-lief``.

Download the source code
------------------------

You can download and extract the source code found on :repository:`Github <>`
to do a manual installation. Check :doc:`development/index`.

Issue tracking
--------------

Bug report and issue tracking on :repository:`Github issues <issues>`.
