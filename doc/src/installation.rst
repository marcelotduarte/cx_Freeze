
Installation
============

In a virtual environment, install by issuing the command:

  .. code-block:: console

    pip install --upgrade cx_Freeze

Without virtual environment, depending on the system:

  .. code-block:: console

    python -m pip install --upgrade cx_Freeze

or

  .. code-block:: console

    python3 -m pip install --upgrade cx_Freeze

Python requirements
-------------------

Python requirements are installed automatically by pip or conda.

  .. code-block:: console

   C compiler                  (required if installing from sources)
   cx_Logging >= 3.1           (Windows only)
   lief >= 0.11.5              (Windows only)
   packaging >= 21.0
   patchelf >= 0.14            (Linux)
   setuptools >= 59.0.1

.. note:: Patchelf

 If you have any trouble with patchelf, check :ref:`patchelf`.

Pipenv
------

Using pipenv, install or update by issuing one of the folowing command:

  .. code-block:: console

    pipenv install cx_Freeze
    pipenv update cx_Freeze

Miniconda3 or Miniforge3
------------------------

Directly from the conda-forge channel:

  .. code-block:: console

    conda install -c conda-forge cx_freeze

If you are installing a pre-release or from sources, install the requirements
using the same channel:

  .. code-block:: console

   python
   c-compiler
   libpython-static (for python >=3.8 in linux and macOS)
   py-lief (Windows)
   patchelf (Linux)
   declare SDKROOT or CONDA_BUILD_SYSROOT (for python 3.9+ in macOS)

An example using Miniconda3:

  .. code-block:: console

    # If using python 3.9 or higer in Github Actions CI, macOS, use this:
    export SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX11.1.sdk

    # For macOS and Linux
    conda create -n cx39conda -c conda-forge python=3.9 libpython-static -y
    conda activate cx39conda
    conda install -c conda-forge c-compiler patchelf -y
    pip install --no-binary=cx_Freeze --pre cx_Freeze -v

Download tarball or wheels
--------------------------

Download directly from |PyPI_link|.

.. |PyPI_link| raw:: html

   <a href="https://pypi.org/project/cx_Freeze" target="_blank">PyPI</a>

Download the source code
------------------------

You can download and extract the source code found on |Github_main| to do a
manual installation.

.. |Github_main| raw:: html

   <a href="https://github.com/marcelotduarte/cx_Freeze" target="_blank">Github</a>

In the source directory, use one of the command:

  .. code-block:: console

    pip install -e .

or

  .. code-block:: console

    python setup.py develop


Issue tracking on |Github_issues|.

.. |Github_issues| raw:: html

   <a href="https://github.com/marcelotduarte/cx_Freeze/issues" target="_blank">Github</a>
