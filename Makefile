# Makefile to automate some tools
SHELL=/bin/bash
PATH := $(shell python -c "import sysconfig; print(sysconfig.get_path('scripts'))"):$(PATH)

PY_PLATFORM := $(shell python -c "import sysconfig; print(sysconfig.get_platform())")
PRE_COMMIT_OPTIONS := --show-diff-on-failure --color=always --all-files --hook-stage=manual --no-progress

COV_TMPDIR := $(shell mktemp -d)

.PHONY: all
all: install

.PHONY: prek
prek: install
	@(prek run $(PRE_COMMIT_OPTIONS) || true) | more
	@prek cache gc -q

.PHONY: pylint
pylint:
	uvx pylint cx_Freeze

.PHONY: clean
clean: uninstall
	@$(MAKE) -C doc clean
	@rm -f .coverage* || true
	@rm -rf build dist wheelhouse
	@prek cache clean -q

.PHONY: install
install:
	./ci/install-tools.sh --dev
	if ! [ -f .git/hooks/pre-commit ]; then\
		prek install --install-hooks --overwrite -t pre-commit;\
	fi

.PHONY: uninstall
uninstall:
	@prek uninstall -q
	@rm -f .git/hooks/pre-commit

.PHONY: upgrade
upgrade: install
	prek auto-update
	$(MAKE) prek

.PHONY: html
html:
	@if [ -f .git/hooks/pre-commit ]; then\
		prek run blacken-docs $(PRE_COMMIT_OPTIONS);\
		prek run build-docs $(PRE_COMMIT_OPTIONS);\
	else\
		$(MAKE) -C doc html;\
	fi

.PHONY: htmltest
htmltest:
	$(MAKE) -C doc test

.PHONY: doc
doc:
	$(MAKE) -C doc html
	$(MAKE) -C doc epub
	$(MAKE) -C doc pdf

.PHONY: wheel
wheel:
	./ci/build-wheel.sh --install

.PHONY: tests
tests: wheel
	./ci/install-tools.sh --tests
	cp pyproject.toml $(COV_TMPDIR)/
	cp -a samples $(COV_TMPDIR)/
	cp -a tests $(COV_TMPDIR)/
	cd $(COV_TMPDIR) && pytest --dist=loadfile -nauto -v -rpfEsXx tests|| true

.PHONY: cov
cov: wheel
	./ci/install-tools.sh --tests
	@rm -rf build/coverage_html_report
	cp pyproject.toml $(COV_TMPDIR)/
	cp -a samples $(COV_TMPDIR)/
	cp -a tests $(COV_TMPDIR)/
	cd $(COV_TMPDIR) && coverage run ||true
	coverage combine --keep --quiet -a $(COV_TMPDIR)/
	coverage report
	coverage html

.PHONY: release
release:
	uv version
	@echo "Run:"
	@echo "  uv version <new-version>"
	@echo "--or--"
	@echo "  uv version --bump <major|minor|patch>"
	@echo "--then--"
	@echo "  git push origin `git branch --show-current`"
	@echo "  git push origin `git branch --show-current` --tags"

.PHONY: release-dev
release-dev:
	git checkout -B release main
	if (uv version --short | grep -q "\.dev"); then\
		uv version --bump dev;\
	else\
		uv version --bump patch --bump dev=0;\
	fi
	git commit -m "Bump dev version: `uv version --short` [ci skip]" -a
	git push origin `git branch --show-current`
	git push origin `git branch --show-current` --tags
	git log -1
