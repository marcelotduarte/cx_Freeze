
Installation
============

cx_Freeze is available on |PyPI_link|.

.. |PyPI_link| raw:: html

   <a href="https://pypi.org/project/cx_Freeze" target="_blank">PyPI</a>

In a virtual environment, install by issuing the command:

  .. code-block:: console

    pip install --upgrade cx_Freeze

Without virtual environment, generally:

  .. code-block:: console

    python3 -m pip install --upgrade cx_Freeze

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

    conda install -c conda-forge cx_freeze

.. note:: Check |cx_freeze-feedstock|.

.. |cx_freeze-feedstock| raw:: html

   <a href="https://github.com/conda-forge/cx_freeze-feedstock#installing-cx_freeze" target="_blank">cx_freeze-feedstock</a>

Python requirements
-------------------

Python requirements are installed automatically by pip, pipenv or conda.

  .. code-block:: console

   setuptools >= 61.2
   packaging >= 21.3
   cx_Logging >= 3.1           (Windows only)
   lief >= 0.12.0              (Windows only)
   patchelf >= 0.14            (Linux)
   C compiler                  (required only if installing from sources)

.. note:: If you have any trouble with patchelf, check :ref:`patchelf`.

Download the source code
------------------------

You can download and extract the source code found on |Github_main| to do a
manual installation. Check :doc:`development/index`.

.. |Github_main| raw:: html

   <a href="https://github.com/marcelotduarte/cx_Freeze" target="_blank">Github</a>

Issue tracking
--------------

Bug report and issue tracking on |Github_issues|.

.. |Github_issues| raw:: html

   <a href="https://github.com/marcelotduarte/cx_Freeze/issues" target="_blank">Github issues</a>
