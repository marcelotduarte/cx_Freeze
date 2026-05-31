Installation
============

The recommended way to use cx_Freeze is in a virtual environment such as
those provided by :pythondocs:`python -m venv <library/venv.html>`,
`uv venv <https://docs.astral.sh/uv/pip/environments/>`_ or
`conda <https://docs.conda.io/projects/conda/en/stable/>`_.
If you're unfamiliar with Python virtual environments, check out the
:packaging:`packaging user guide
<guides/installing-using-pip-and-virtual-environments>`.

The latest version of cx_Freeze is available on:

PyPI: :pypi:`cx_Freeze`

Conda-forge: `cx_freeze
<https://github.com/conda-forge/cx_freeze-feedstock#installing-cx_freeze>`_

MSYS2: `python-cx-freeze
<https://packages.msys2.org/base/mingw-w64-python-cx-freeze>`_

Choose the Python package manager according to your system. See how the
installation works with the most common ones.

   .. tab:: pip

      .. code-block:: console

         pip install --upgrade cx_Freeze

   .. tab:: uv

      .. code-block:: console

         uv pip install --upgrade cx_Freeze

   .. tab:: conda

      .. code-block:: console

         conda install conda-forge:cx_freeze

   .. tab:: msys2

      .. code-block:: console

         pacman -S --needed --noconfirm $MINGW_PACKAGE_PREFIX-python-cx-freeze

.. important::
  Please note that some operating systems might be equipped with the python3
  and pip3 commands instead of python and pip (but they should be equivalent).

.. _python_requirements:

Python requirements
-------------------

Python requirements are installed automatically by pip, uv, conda or pacman.

  .. code-block:: console

   freeze-core >=0.6.1
   packaging >=25.0
   setuptools >=78.1.1,<83.0
   filelock >=3.20.3           #  Linux
   patchelf >=0.14,<0.18       #  Linux
   dmgbuild >=1.6.1            #  macOS
   lief >=0.16,<0.18           #  Windows
   python-msilib >=0.4.1       #  Python 3.13+ on Windows

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
