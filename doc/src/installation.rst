
Installation
============

Choose the Python package manager according to your system. See how the
installation works with the most common ones.

.. tabs::

   .. group-tab:: Pip

      To install the latest version of :pypi:`cx_Freeze` using :pypi:`pip` into
      a virtual environment:

      .. code-block:: console

         pip install --upgrade cx_Freeze

   .. group-tab:: Uv

      .. code-block:: console

         uv pip install --upgrade cx_Freeze

   .. group-tab:: Conda

      Installing cx_freeze from the conda-forge channel can be achieved with
      the command:

      .. code-block:: console

         conda install conda-forge:cx_freeze

      .. seealso:: `cx_freeze-feedstock
         <https://github.com/conda-forge/cx_freeze-feedstock#installing-cx_freeze>`_.

.. warning::
  It is not recommended to use ``pip`` in conda environment. See why in
  `Using Pip in a Conda Environment
  <https://www.anaconda.com/blog/using-pip-in-a-conda-environment>`_.

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

   filelock >= 3.12.3
   importlib_metadata >= 6     (Python 3.9-3.10.2)
   packaging >= 24
   setuptools >= 65.6.3        (setuptools >= 70.1 if installing from sources)
   tomli >= 2.0.1              (Python 3.9-3.10)
   typing_extensions >= 4.10.0 (Python 3.9)
   patchelf >= 0.14            (Linux)
   dmgbuild >= 1.6.1           (macOS)
   cabarchive >= 0.2.4         (Windows only)
   cx_Logging >= 3.1           (Windows only)
   lief >= 0.13.2              (Windows only)
   striprtf >= 0.0.26          (Windows only)
   C compiler                  (required only if installing from sources)

.. note:: If you have trouble with patchelf, check :ref:`patchelf`.

Download the source code
------------------------

You can download and extract the source code found on :repository:`Github <>`
to do a manual installation. Check :doc:`development/index`.

Issue tracking
--------------

Bug report and issue tracking on :repository:`Github issues <issues>`.
