
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

Using pipenv, install or update by issuing one of the folowing command:

  .. code-block:: console

    pipenv install cx_Freeze
    pipenv update cx_Freeze

Conda-forge
-----------

Directly from the conda-forge channel:

  .. code-block:: console

    conda install conda-forge::cx_freeze

.. seealso:: `cx_freeze-feedstock <https://github.com/conda-forge/cx_freeze-feedstock#installing-cx_freeze>`_.

Python requirements
-------------------

Python requirements are installed automatically by pip, pipenv or conda.

  .. code-block:: console

   setuptools >= 62.6
   cx_Logging >= 3.1           (Windows only)
   lief >= 0.12.0              (Windows only)
   patchelf >= 0.14            (Linux)
   C compiler                  (required only if installing from sources)

.. note:: If you have any trouble with patchelf, check :ref:`patchelf`.

Download the source code
------------------------

You can download and extract the source code found on :repository:`Github <>`
to do a manual installation. Check :doc:`development/index`.

Issue tracking
--------------

Bug report and issue tracking on :repository:`Github issues <issues>`.
