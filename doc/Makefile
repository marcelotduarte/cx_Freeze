# Makefile to generate cx_Freeze documentation using Sphinx

ifeq ($(origin READTHEDOCS_OUTPUT), undefined)
	BUILDDIR = ../build/doc
else
	BUILDDIR = $(READTHEDOCS_OUTPUT)
endif
BUILDDIRHTML = $(BUILDDIR)/html
SOURCEDIR    = src
SPHINXBUILD = uvx -p 3.12 --with-requirements=requirements.txt --from sphinx sphinx-build
SPHINXOPTS   = -d $(BUILDDIR)/.doctrees -j auto -T -W --keep-going -n

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
