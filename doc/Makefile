# Makefile to generate cx_Freeze documentation using Sphinx

SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = src
BUILDDIR      = ../build/doc

.PHONY: html
html:
	pip install --upgrade -r requirements.txt
	@$(SPHINXBUILD) -M html $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS)

.PHONY: epub
epub:
	@$(SPHINXBUILD) -M epub $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS)

.PHONY: pdf
pdf:
	@$(SPHINXBUILD) -M latexpdf $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS)

.PHONY: test
test:
	(cd $(BUILDDIR)/html && python -m webbrowser -t index.html)

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)
