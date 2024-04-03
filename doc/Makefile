# Makefile to generate cx_Freeze documentation using Sphinx

SPHINXOPTS    = -d ../build/doc/.doctrees -j auto -T -W --keep-going -n
SPHINXBUILD   = python -m sphinx
SOURCEDIR     = src
BUILDDIR      = ../build/doc
BUILDDIRHTML  = ../build/doc/html

.PHONY: html
html:
	@$(SPHINXBUILD) $(SOURCEDIR) $(BUILDDIRHTML) $(SPHINXOPTS) -b html

.PHONY: epub
epub:
	@$(SPHINXBUILD) $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS) -b epub

.PHONY: pdf
pdf:
	@$(SPHINXBUILD) $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS) -b latexpdf

.PHONY: test
test:
	(cd $(BUILDDIRHTML) && python -m webbrowser -t index.html)

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)
