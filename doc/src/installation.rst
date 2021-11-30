
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

- cx_Logging >=3.0 (Windows only)
- importlib-metadata
- setuptools

Others requirements
-------------------

- C compiler - if installing from sources.
- patchelf - in unix-like systems (Linux, FreeBSD, etc), except macOS.

To install patchelf in debian/ubuntu:

  .. code-block:: console

    sudo apt-get install patchelf

To install patchelf in fedora:

  .. code-block:: console

    dnf install patchelf

Or install patchelf from |patchelf_sources|:

.. |patchelf_sources| raw:: html

   <a href="https://github.com/NixOS/patchelf#compiling-and-testing" target="_blank">sources</a>

  .. code-block:: console

    git clone -b 0.13 --single-branch https://github.com/NixOS/patchelf.git
    cd patchelf
    ./bootstrap.sh
    ./configure
    make
    make check
    sudo make install


Pipenv
------

Using pipenv, install or update by issuing one of the folowing commanda:

  .. code-block:: console

    pipenv install cx_Freeze
    pipenv update cx_Freeze

Miniconda3
----------

Directly from the conda-forge channel:

  .. code-block:: console

    conda install -c conda-forge cx_freeze

If you are installing a pre-release or from sources, install the requirements
using the same channel:

- python
- c-compiler
- libpython-static (for python >=3.8 in linux and macOS)
- importlib-metadata
- patchelf (optional if already installed in the Linux system)
- declare SDKROOT or CONDA_BUILD_SYSROOT (for python 3.9 in macOS)

An example using Miniconda3:

  .. code-block:: console

    # If using python 3.9 or higer in Github Actions CI, macOS, use this:
    export SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX11.1.sdk

    # For macOS and Linux
    conda create -n cx39conda -c conda-forge python=3.9 libpython-static -y
    conda activate cx39conda
    conda install -c conda-forge c-compiler importlib-metadata -y
    pip install --no-binary :all: --pre cx_Freeze -v

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
