# Makefile to generate cx_Freeze documentation using Sphinx

SPHINXOPTS    = -d ../build/doc/.doctrees -j auto -T -W --keep-going
SPHINXBUILD   = python -m sphinx
SOURCEDIR     = src
BUILDDIR      = ../build/doc

.PHONY: html
html:
	@$(SPHINXBUILD) $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS) -b html

.PHONY: epub
epub:
	@$(SPHINXBUILD) $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS) -b epub

.PHONY: pdf
pdf:
	@$(SPHINXBUILD) $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS) -b latexpdf

.PHONY: test
test:
	(cd $(BUILDDIR)/html && python -m webbrowser -t index.html)

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)
