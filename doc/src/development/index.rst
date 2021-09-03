
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

The source code can be found on
`Github <https://github.com/marcelotduarte/cx_Freeze>`_.

You can use ``git`` to clone the repository:

  .. code-block:: console

      git clone https://github.com/marcelotduarte/cx_Freeze
      cd cx_Freeze
      pip install -e .

.. note::

   #. Please check the requirements for python and for your system
      (see :doc:`../installation`).
   #. ``python setup.py develop`` can be used, but ``pip install -e .`` is
      better, because it installs the requirements.


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
