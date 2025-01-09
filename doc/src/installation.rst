
Installation
============

Pip
---

You should install the latest version of :pypi:`cx_Freeze` using :pypi:`pip`:

  .. code-block:: console

    pip install --upgrade cx_Freeze

.. note::
  The recommended way to use cx_Freeze is in a
  :pythondocs:`virtual environment <library/venv.html>`.
  If you're unfamiliar with Python virtual environments, check out the
  :packaging:`packaging user guide <guides/installing-using-pip-and-virtual-environments>`.

.. important::
  Please note that some operating systems might be equipped with the python3
  and pip3 commands instead of python and pip (but they should be equivalent).

Pipenv
------

Using pipenv, install or update by issuing one of the following commands:

  .. code-block:: console

    pipenv install cx_Freeze
    pipenv update cx_Freeze

Conda-forge
-----------

Directly from the conda-forge channel:

  .. code-block:: console

    conda install conda-forge::cx_freeze

.. seealso:: `cx_freeze-feedstock
   <https://github.com/conda-forge/cx_freeze-feedstock#installing-cx_freeze>`_.

Python requirements
-------------------

Python requirements are installed automatically by pip, pipenv, or conda.

  .. code-block:: console

   packaging >= 24
   setuptools >= 65.6.3        (setuptools >= 70.1 to build)
   importlib_metadata >= 6     (Python 3.8-3.10.2)
   tomli >= 2.0.1              (Python 3.8-3.10)
   typing_extensions >= 4.10.0 (Python 3.8-3.9)
   cx_Logging >= 3.1           (Windows only)
   lief >= 0.13.2              (Windows only)
   filelock >=3.12.3           (Linux)
   patchelf >= 0.14            (Linux)
   dmgbuild >= 1.6.1           (macOS)
   C compiler                  (required only if installing from sources)

.. note:: If you have trouble with patchelf, check :ref:`patchelf`.

Download the source code
------------------------

You can download and extract the source code found on :repository:`Github <>`
to do a manual installation. Check :doc:`development/index`.

Issue tracking
--------------

Bug report and issue tracking on :repository:`Github issues <issues>`.
