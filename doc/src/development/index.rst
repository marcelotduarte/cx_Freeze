
Development
===========

Getting started
---------------

**cx_Freeze** is a volunteer maintained open source project and we welcome
contributions of all forms. The sections below will help you get started with
development, testing, and documentation. We’re pleased that you are interested
in working on cx_Freeze. This document is meant to get you setup to work on
cx_Freeze and to act as a guide and reference to the development setup.
If you face any issues during this process, please open an issue about it on
the issue tracker.

Setup
-----

The source code can be found on :repository:`Github <>`.

You can use ``git`` to clone the repository:

  .. code-block:: console

    git clone https://github.com/marcelotduarte/cx_Freeze
    cd cx_Freeze
    make install

If you don't have make installed, run:

  .. code-block:: console

    python -m pip install --upgrade pip
    pip install -e .[dev,doc]
    pre-commit install --install-hooks --overwrite -t pre-commit

.. note::

   #. It is recommended to use a virtual environment.
   #. Please check the requirements for python on your system
      (see :ref:`python_requirements`).

Building redistributable binary wheels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When ``python -m build`` or ``pip wheel`` is used to build a cx_Freeze wheel,
that wheel will rely on external shared libraries. Such wheels
therefore will only run on the system on which they are built. See
`Building and installing or uploading artifacts
<https://pypackaging-native.github.io/meta-topics/build_steps_conceptual/#building-and-installing-or-uploading-artifacts>`_
for more context on that.

A wheel like that is therefore an intermediate stage to producing a binary that
can be distributed. That final binary may be a wheel - in that case, run
``auditwheel`` (Linux) or ``delocate`` (macOS) to vendor the required shared
libraries into the wheel.

To reach this, cx_Freeze's binary wheels is built using :pypi:`cibuildwheel`.

  .. code-block:: console

    pip install --upgrade cibuildwheel

For instance, in a Linux environment, Python 3.10, to build locally, run:

  .. code-block:: console

    cibuildwheel --only cp310-manylinux_x86_64

To run a Linux build on your development machine, Docker or Podman should be
installed. To use podman:

  .. code-block:: console

    CIBW_CONTAINER_ENGINE=podman cibuildwheel --only cp310-manylinux_x86_64

Using macOS:

  .. code-block:: console

    cibuildwheel --only cp310-macosx_universal2

.. note::

   Please read:

   #. `Run cibuildwheel locally
      <https://cibuildwheel.readthedocs.io/en/stable/setup/#local>`_.
   #. `Linux builds
      <https://cibuildwheel.pypa.io/en/stable/setup/#linux-builds>`_.
   #. `macOS / Windows builds
      <https://cibuildwheel.pypa.io/en/stable/setup/#macos-windows-builds>`_.


Building documentation
~~~~~~~~~~~~~~~~~~~~~~

cx_Freeze's documentation is built using :pypi:`Sphinx`. The documentation is
written in reStructuredText. To build it locally, run:

  .. code-block:: console

    make html

The built documentation can be found in the ``build/doc/html`` folder and may
be viewed by opening ``index.html`` within that folder.

  .. code-block:: console

    make htmltest

Conda-forge
-----------

If you are installing a pre-release or from sources, install the requirements
using the conda-forge channel:

  .. code-block:: console

    python
    c-compiler
    py-lief (Windows)
    patchelf (Linux)
    # declare SDKROOT or CONDA_BUILD_SYSROOT (not required in Github Actions)

An example for Linux:

  .. code-block:: console

    git clone https://github.com/marcelotduarte/cx_Freeze
    cd cx_Freeze
    conda create -n cx311conda -c conda-forge python=3.11 c-compiler -y
    conda activate cx311conda
    conda install -c conda-forge patchelf -y
    conda install -c conda-forge --file=requirements-dev.txt
    pre-commit install --install-hooks --overwrite -t pre-commit
    pip install -e. --no-deps --no-build-isolation

.. note::
    ``pip`` should be used in conda only in development mode.

Contributing
-------------

Submitting pull requests
~~~~~~~~~~~~~~~~~~~~~~~~

Submit pull requests against the ``main`` branch providing a good
description of what you are doing and why. You must have legal permission to
distribute any code you contribute to cx_Freeze and it must be available under
the PSF License.
Any pull request should consider that it needs to work on supported platforms.

Pull Requests should be small to facilitate review. Keep them self-contained,
and limited in scope. `Studies have shown
<https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/>`_
that review quality falls off as patch size grows. Sometimes this will result
in many small PRs to land a single large feature. In particular, pull requests
must not be treated as "feature branches", with ongoing development work
within the PR. Instead, the feature should be broken up into smaller,
independent parts which can be reviewed and merged individually.

Additionally, avoid including "cosmetic" changes to code that are unrelated to
your change, as these make reviewing the PR more difficult. Examples include
re-flowing text in comments or documentation or adding or removing blank lines
or whitespace within lines. Such changes can be made separately, as a
"formatting cleanup" PR as required.

Contents:

.. toctree::
   :maxdepth: 2

   code_layout.rst
