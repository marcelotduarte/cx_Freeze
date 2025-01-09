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
	curl -LsSf https://astral.sh/uv/install.sh | \
	env UV_INSTALL_DIR="$(HOME)/bin" INSTALLER_NO_MODIFY_PATH=1 sh
endif
	if ! which pre-commit || ! [ -f .git/hooks/pre-commit ]; then\
		uv pip install --extra dev --extra doc --upgrade -r pyproject.toml &&\
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
	uv pip install --extra doc --upgrade -r pyproject.toml
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

.PHONY: cov2
cov2: install_pytest
	@rm -rf $(BUILDDIR)/coverage_html_report
	@if [ -f .coverage ]; then mv .coverage .backup_coverage; fi
	pytest -nauto --cov="cx_Freeze" || true
ifeq ($(PY_PLATFORM),win-amd64)
	# Extra coverage for Windows
	# test without lief (LIEF_DISABLED)
	CX_FREEZE_BIND=imagehlp \
	pytest -nauto --cov="cx_Freeze" --cov-append \
		tests/test_command_build.py tests/test_command_build_exe.py \
		tests/test_winversioninfo.py || true
	# test lief min version
	uv pip install "lief==0.13.2"
	pytest -nauto --cov="cx_Freeze" --cov-append \
		tests/test_command_build.py tests/test_command_build_exe.py \
		tests/test_winversioninfo.py || true
	# test lief 0.14
	uv pip install "lief==0.14.1"
	pytest -nauto --cov="cx_Freeze" --cov-append \
		tests/test_command_build.py tests/test_command_build_exe.py \
		tests/test_winversioninfo.py || true
	# test lief 0.15
	uv pip install "lief==0.15.1"
	pytest -nauto --cov="cx_Freeze" --cov-append \
		tests/test_command_build.py tests/test_command_build_exe.py \
		tests/test_winversioninfo.py || true
	# test lief 0.16
	uv pip install "lief==0.16.2"
	pytest -nauto --cov="cx_Freeze" --cov-append \
		tests/test_command_build.py tests/test_command_build_exe.py \
		tests/test_winversioninfo.py || true
	# coverage winversioninfo using pywin32
	uv pip install --upgrade pywin32
	pytest -nauto --cov="cx_Freeze" --cov-append \
		tests/test_winversioninfo.py || true
	uv pip uninstall pywin32
	uv pip install lief --upgrade
endif
	@if [ -f .backup_coverage ]; then coverage combine -a .backup_coverage; fi
	coverage report
	coverage html --title="Multiple coverage reports"
	@python -m webbrowser -t $(BUILDDIR)/coverage_html_report/index.html

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
