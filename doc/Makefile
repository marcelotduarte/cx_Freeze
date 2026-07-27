# Makefile to generate cx_Freeze documentation using Sphinx

TOP_DIR=$(shell (cd .. && pwd))
ifeq ($(origin READTHEDOCS_OUTPUT), undefined)
	BUILDDIR = $(TOP_DIR)/build/doc
else
	BUILDDIR = $(READTHEDOCS_OUTPUT)
endif

SOURCEDIR    = src
SPHINXBUILD  = sphinx-build
SPHINXOPTS   = --color -j auto --fail-on-warning --nitpicky --show-traceback

.PHONY: all
all: html

.PHONY: install
install:
	@$(TOP_DIR)/ci/install-tools.sh --doc

.PHONY: html
html: install
	@$(SPHINXBUILD) -M html $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS)

.PHONY: epub
epub: install
	@$(SPHINXBUILD) -M epub $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS)

.PHONY: pdf
pdf: install
	@$(SPHINXBUILD) -M latexpdf $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS)

.PHONY: test
test: install
	(cd $(BUILDDIR)/html && python -m webbrowser -t index.html)

.PHONY: clean
clean:
	@rm -rf $(BUILDDIR)
	@uv tool uninstall sphinx || true
