# Makefile to generate cx_Freeze documentation using Sphinx

SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = src
BUILDDIR      = build

.PHONY: html
html:
	pip install -U sphinx
	@$(SPHINXBUILD) -M html $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS)

.PHONY: epub
epub:
	@$(SPHINXBUILD) -M epub $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS)

.PHONY: pdf
pdf:
	@$(SPHINXBUILD) -M latexpdf $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS)

.PHONY: test
test:
	firefox build/html/index.html &

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/*
