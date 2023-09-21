
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

The source code can be found on |Github_main|.

.. |Github_main| raw:: html

   <a href="https://github.com/marcelotduarte/cx_Freeze" target="_blank">Github</a>

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
      (see :doc:`../installation`).

Building redistributable binary wheels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When ``python -m build`` or ``pip wheel`` is used to build a cx_Freeze wheel,
that wheel will rely on external shared libraries. Such wheels
therefore will only run on the system on which they are built. See
`the pypackaging-native content under "Building and installing or uploading
artifacts" <https://pypackaging-native.github.io/meta-topics/build_steps_conceptual/#building-and-installing-or-uploading-artifacts>`__ for more context on that.

A wheel like that is therefore an intermediate stage to producing a binary that
can be distributed. That final binary may be a wheel - in that case, run
``auditwheel`` (Linux) or ``delocate`` (macOS) to vendor the required shared
libraries into the wheel.

To reach this, cx_Freeze's binary wheels is built using :pypi:`cibuildwheel`.

For instance, in a Linux environment, Python 3.10, to build locally, run:

  .. code-block:: console

      pip install --upgrade cibuildwheel
      CIBW_BUILD=cp310-manylinux_x86_64 cibuildwheel --platform linux

.. note::

   #. Please read `Run cibuildwheel locally
      <https://cibuildwheel.readthedocs.io/en/stable/setup/#local>`_.
   #. To run a Linux build on your development machine, Docker or Podman should
      be installed. To use podman, set `CIBW_CONTAINER_ENGINE
      <https://cibuildwheel.readthedocs.io/en/stable/options/#container-engine>`_.


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
    # declare SDKROOT or CONDA_BUILD_SYSROOT (for python 3.9+ in macOS)
    # for example, in Github Actions CI, macOS:
    export SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX11.1.sdk

An example for Linux:

  .. code-block:: console

    conda create -n cx39conda -c conda-forge python=3.9 -y
    conda activate cx39conda
    conda install -c conda-forge c-compiler patchelf -y
    pip install --upgrade --no-binary=cx_Freeze --pre cx_Freeze -v

Contributing
-------------

Submitting pull requests
~~~~~~~~~~~~~~~~~~~~~~~~

Submit pull requests against the ``main`` branch, providing a good
description of what you're doing and why. You must have legal permission to
distribute any code you contribute to cx_Freeze and it must be available under
the PSF License.
Any pull request must consider and work on the supported platforms.

Pull Requests should be small to facilitate review. Keep them self-contained,
and limited in scope. `Studies have shown
<https://www.kessler.de/prd/smartbear/BestPracticesForPeerCodeReview.pdf>`_
that review quality falls off as patch size grows. Sometimes this will result
in many small PRs to land a single large feature. In particular, pull requests
must not be treated as "feature branches", with ongoing development work
happening within the PR. Instead, the feature should be broken up into smaller,
independent parts which can be reviewed and merged individually.

Additionally, avoid including "cosmetic" changes to code that is unrelated to
your change, as these make reviewing the PR more difficult. Examples include
re-flowing text in comments or documentation, or addition or removal of blank
lines or whitespace within lines. Such changes can be made separately, as a
"formatting cleanup" PR, if needed.

Contents:

.. toctree::
   :maxdepth: 2

   code_layout.rst
