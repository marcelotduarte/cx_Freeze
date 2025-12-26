# Makefile to automate some tools
SHELL=/bin/bash
PATH := $(shell python -c "import sysconfig; print(sysconfig.get_path('scripts'))"):$(PATH)

PY_PLATFORM := $(shell python -c "import sysconfig; print(sysconfig.get_platform())")
PRE_COMMIT_OPTIONS := --show-diff-on-failure --color=always --all-files --hook-stage=manual

COV_TMPDIR := $(shell mktemp -d)

.PHONY: all
all: install

.PHONY: pre-commit
pre-commit: install
	@(pre-commit run $(PRE_COMMIT_OPTIONS) || true) | more
	@pre-commit gc

.PHONY: pylint
pylint:
	uvx pylint cx_Freeze

.PHONY: clean
clean: uninstall
	@$(MAKE) -C doc clean
	@rm -f .coverage* || true

.PHONY: install
install:
	./ci/install-tools.sh --dev
	if ! [ -f .git/hooks/pre-commit ]; then\
		pre-commit install --install-hooks --overwrite -t pre-commit;\
	fi

.PHONY: uninstall
uninstall:
	@if [ -f .git/hooks/pre-commit ]; then\
		pre-commit clean;\
		pre-commit uninstall;\
		rm -f .git/hooks/pre-commit;\
	fi

.PHONY: upgrade
upgrade: clean install
	pre-commit autoupdate
	$(MAKE) pre-commit

.PHONY: html
html:
	@if [ -f .git/hooks/pre-commit ]; then\
		pre-commit run blacken-docs $(PRE_COMMIT_OPTIONS);\
		pre-commit run build-docs $(PRE_COMMIT_OPTIONS);\
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
	./ci/build-wheel.sh

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
	bump-my-version show-bump 2>/dev/null
	@echo "Run:"
	@echo "  bump-my-version bump <option>"
	@echo "--or--"
	@echo "  bump-my-version bump patch --new-version=X.XX.X"
	@echo "--then--"
	@echo "  git push origin `git branch --show-current`"
	@echo "  git push origin `git branch --show-current` --tags"

.PHONY: release-dev
release-dev:
	if (grep "current_version" pyproject.toml | grep -q "\-dev"); then\
		bump-my-version bump --allow-dirty --no-tag build;\
	else\
		bump-my-version bump --allow-dirty --no-tag minor;\
	fi
	git log -1
