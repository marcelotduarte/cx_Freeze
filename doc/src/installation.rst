
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

- cx_Logging 3.0 - installed automatically on Windows;
- importlib-metadata - installed automatically;
- setuptools - installing from source requires ``setuptools`` (installed
  automatically in virtual environments).

Requirement for all SO
----------------------

- C compiler - if installing from sources.

Requirement for Linux
---------------------

- patchelf

To install patchelf in debian/ubuntu:

  .. code-block:: console

    sudo apt install patchelf

Pipenv
------

Using pipenv, install or update by issuing one of the folowing commanda:

  .. code-block:: console

    pipenv install cx_Freeze
    pipenv update cx_Freeze

Anaconda / Miniconda
--------------------

  .. code-block:: console

    conda install -c conda-forge cx_freeze

Download tarball or wheels
--------------------------

Download directly from `PyPI <https://pypi.org/project/cx_Freeze>`_.


Download the source code
------------------------

You can download and extract the source code found on
`Github <https://github.com/marcelotduarte/cx_Freeze>`__
to do a a manual installation.

In the source directory, use one of the command:

  .. code-block:: console

    pip install .

or

  .. code-block:: console

    python setup.py develop


Issue tracking on `Github <https://github.com/marcelotduarte/cx_Freeze/issues>`_.
