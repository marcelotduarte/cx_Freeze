# Makefile to automate some tools
SHELL=/bin/bash

BUILDDIR := ./build
EXT_SUFFIX := $(shell python -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))")
ARCH := $(shell python -c "import platform; print(platform.machine().lower())")
PY_PLATFORM := $(shell python -c "import sysconfig; print(sysconfig.get_platform())")
PY_VERSION_NODOT := $(shell python -c "import sysconfig; print(sysconfig.get_config_var('py_version_nodot'))")
COVERAGE_FILE := $(BUILDDIR)/.coverage-$(PY_VERSION_NODOT)-$(PY_PLATFORM)
PRE_COMMIT_OPTIONS := --show-diff-on-failure --color=always --all-files --hook-stage=manual
CIBW_ONLY := cp$(PY_VERSION_NODOT)-manylinux_$(ARCH)
CX_FREEZE_VERSION := $(shell bump-my-version show current_version|sed 's/-/./')
CX_FREEZE_WHEEL := $(shell ls wheelhouse/cx_Freeze-$(CX_FREEZE_VERSION)-cp$(PY_VERSION_NODOT)-cp$(PY_VERSION_NODOT)-manylinux_*_$(ARCH).whl)

.PHONY: all
all: install

.PHONY: pre-commit
pre-commit: install
	@SKIP=pylint pre-commit run $(PRE_COMMIT_OPTIONS) || true
	@pre-commit gc

.PHONY: pre-commit-all
pre-commit-all: install
	@pre-commit run $(PRE_COMMIT_OPTIONS) || true
	@pre-commit gc

.PHONY: pylint
pylint:
	@if ! which pylint; then pip install --upgrade pylint; fi
	@pre-commit run pylint $(PRE_COMMIT_OPTIONS)

.PHONY: clean
clean:
	@if which pre-commit && [ -f .git/hooks/pre-commit ]; then\
		pre-commit clean;\
		pre-commit uninstall;\
		rm -f .git/hooks/pre-commit;\
	fi
	@$(MAKE) -C doc clean
	@COVERAGE_FILE=$(COVERAGE_FILE) coverage erase
	@coverage erase

.PHONY: install
install:
	if ! which pre-commit || ! [ -f .git/hooks/pre-commit ]; then\
		python -m pip install --upgrade pip &&\
		pip install -e .[dev,doc] --no-build-isolation &&\
		pre-commit install --install-hooks --overwrite -t pre-commit;\
	fi

.PHONY: upgrade
upgrade: clean
	@rm -f .git/hooks/pre-commit || true
	pip uninstall -y cx_Freeze || true
	pip install --upgrade pre-commit
	pre-commit autoupdate
	$(MAKE) pre-commit

.PHONY: html
html: install
	@if which pre-commit && [ -f .git/hooks/pre-commit ]; then\
		pre-commit run blacken-docs $(PRE_COMMIT_OPTIONS);\
		pre-commit run build-docs $(PRE_COMMIT_OPTIONS);\
	else\
		pip install -e .[doc] --no-build-isolation &&\
		$(MAKE) -C doc html;\
	fi

.PHONY: htmltest
htmltest:
	$(MAKE) -C doc test

.PHONY: doc
doc: html
	$(MAKE) -C doc epub
	$(MAKE) -C doc pdf

.PHONY: install_test
install_test:
	if ! which pytest; then pip install -e .[test]; else pip install -e .; fi

.PHONY: test
test: install_test
	python -m pytest -nauto --no-cov

.PHONY: cov
cov: install_test
	python -m pytest -nauto --cov="cx_Freeze" --cov-report=html
	python -m webbrowser -t $(BUILDDIR)/coverage/index.html

.PHONY: cov2
cov2: install_test
	coverage erase
	COVERAGE_FILE=$(COVERAGE_FILE) coverage erase
	COVERAGE_FILE=$(COVERAGE_FILE) python -m pytest -nauto --cov="cx_Freeze"
ifeq ($(PY_PLATFORM),win-amd64)
	# Extra coverage for Windows
	# to test lief < 0.14
	pip install "lief==0.13.2"
	COVERAGE_FILE=$(COVERAGE_FILE)-1 python -m pytest -nauto --cov="cx_Freeze" \
		tests/test_command_build.py tests/test_command_build_exe.py \
		tests/test_winversioninfo.py
	# to test without lief (LIEF_DISABLED)
	CX_FREEZE_BIND=imagehlp \
	COVERAGE_FILE=$(COVERAGE_FILE)-2 python -m pytest -nauto --cov="cx_Freeze" \
		tests/test_command_build.py tests/test_command_build_exe.py \
		tests/test_winversioninfo.py
	# to coverage winversioninfo using pywin32
	pip install --upgrade pywin32
	COVERAGE_FILE=$(COVERAGE_FILE)-3 python -m pytest -nauto --cov="cx_Freeze" \
		tests/test_winversioninfo.py
	pip uninstall -y pywin32
	pip install "lief>0.13.2"
endif
ifeq ($(PY_PLATFORM),linux-x86_64)
	if [ -z "$(CX_FREEZE_WHEEL)" ] && which podman; then\
		CIBW_CONTAINER_ENGINE=podman cibuildwheel --only $(CIBW_ONLY);\
	fi
	unzip -q -o $(CX_FREEZE_WHEEL) \
		"cx_Freeze/bases/*" -x "*.py"
	COVERAGE_FILE=$(COVERAGE_FILE)-4 python -m pytest -nauto --cov="cx_Freeze" \
		tests/test_command_build.py tests/test_command_build_exe.py
endif
	coverage combine --keep $(BUILDDIR)/.coverage-*
	rm -rf $(BUILDDIR)/coverage
	coverage html
	python -m webbrowser -t $(BUILDDIR)/coverage/index.html

.PHONY: release
release:
	@echo "# Run:\n"\
	"bump-my-version bump release\n"\
	"git push origin main --tags"

.PHONY: release-patch
release-patch:
	@echo "# Run:\n"\
	"bump-my-version bump patch --new-version=X.XX.X\n"\
	"git push origin `git branch --show-current` --tags"

.PHONY: release-dev
release-dev:
	if (grep "current_version" pyproject.toml | grep -q "\-dev"); then\
		bump-my-version bump --allow-dirty --no-tag build;\
	else\
		bump-my-version bump --allow-dirty --no-tag minor;\
	fi
