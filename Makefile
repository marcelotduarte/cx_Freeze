# Makefile to automate some tools
SHELL=/bin/bash
PATH := $(shell python -c "import sysconfig; print(sysconfig.get_path('scripts'))"):$(PATH)

BUILDDIR := ./build
PY_PLATFORM := $(shell python -c "import sysconfig; print(sysconfig.get_platform())")
PRE_COMMIT_OPTIONS := --show-diff-on-failure --color=always --all-files --hook-stage=manual

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
	@rm -f .coverage .backup_coverage || true

.PHONY: install
install:
ifeq ($(PY_PLATFORM),win-amd64)
	if ! which uv; then\
		python -m pip install --upgrade uv --disable-pip-version-check;\
	fi
else
	ci/install-uv.sh
endif
	if ! which pre-commit || ! [ -f .git/hooks/pre-commit ]; then\
		uv pip install --extra dev --upgrade -r pyproject.toml &&\
		pre-commit install --install-hooks --overwrite -t pre-commit;\
	fi

.PHONY: uninstall
uninstall:
	@if which pre-commit && [ -f .git/hooks/pre-commit ]; then\
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
	@if which pre-commit && [ -f .git/hooks/pre-commit ]; then\
		pre-commit run blacken-docs $(PRE_COMMIT_OPTIONS);\
		pre-commit run build-docs $(PRE_COMMIT_OPTIONS);\
	else\
		$(MAKE) -C doc html;\
	fi

.PHONY: htmltest
htmltest:
	$(MAKE) -C doc test

.PHONY: doc
doc: html
	$(MAKE) -C doc epub
	$(MAKE) -C doc pdf

.PHONY: install_pytest
install_pytest:
	uv pip install --extra tests --upgrade -r pyproject.toml
	./ci/build-wheel.sh

.PHONY: tests
tests: install_pytest
	pytest -nauto --no-cov

.PHONY: cov
cov: install_pytest
	@rm -rf $(BUILDDIR)/coverage_html_report
	@if [ -f .coverage ]; then mv .coverage .backup_coverage; fi
	pytest -nauto --cov="cx_Freeze" --cov-report=html
	coverage report
	@python -m webbrowser -t $(BUILDDIR)/coverage_html_report/index.html
	@if [ -f .backup_coverage ]; then coverage combine -a .backup_coverage; fi

.PHONY: release
release:
	bump-my-version show-bump 2>/dev/null
	@echo "Run:"
	@echo "  bump-my-version bump <option>"
	@echo "--or--"
	@echo "  bump-my-version bump patch --new-version=X.XX.X"
	@echo "--then--"
	@echo "  git push origin `git branch --show-current` --tags"

.PHONY: release-dev
release-dev:
	if (grep "current_version" pyproject.toml | grep -q "\-dev"); then\
		bump-my-version bump --allow-dirty --no-tag build;\
	else\
		bump-my-version bump --allow-dirty --no-tag minor;\
	fi
	git log -1
