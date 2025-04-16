# Makefile to generate cx_Freeze documentation using Sphinx

ifeq ($(origin READTHEDOCS_OUTPUT), undefined)
	BUILDDIR = ../build/doc
	SPHINXBUILD = uvx -p 3.12 --with-requirements=requirements.txt --from sphinx sphinx-build
else
	BUILDDIR = $READTHEDOCS_OUTPUT
	SPHINXBUILD = uv run -p .venv/bin/python -m sphinx
endif
BUILDDIRHTML = $(BUILDDIR)/html
SOURCEDIR    = src
SPHINXOPTS   = -d $(BUILDDIR)/.doctrees -j auto -T -W --keep-going -n

.PHONY: html
html: install
	@$(SPHINXBUILD) $(SOURCEDIR) $(BUILDDIRHTML) $(SPHINXOPTS) -b html

.PHONY: epub
epub: install
	@$(SPHINXBUILD) $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS) -b epub

.PHONY: pdf
pdf: install
	@$(SPHINXBUILD) $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS) -b latexpdf

.PHONY: test
test: install
	(cd $(BUILDDIRHTML) && python -m webbrowser -t index.html)

install:
ifeq ($(origin READTHEDOCS_OUTPUT), environment)
	uv sync -p 3.12 --no-install-project --extra doc
endif

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)
