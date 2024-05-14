# Makefile to automate some tools
SHELL=/bin/bash
PATH := $(shell python -c "import sysconfig; print(sysconfig.get_path('scripts'))"):$(PATH)

BUILDDIR := ./build
EXT_SUFFIX := $(shell python -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))")
ARCH := $(shell python -c "import platform; print(platform.machine().lower())")
PY_PLATFORM := $(shell python -c "import sysconfig; print(sysconfig.get_platform())")
PY_VERSION_NODOT := $(shell python -c "import sysconfig; print(sysconfig.get_config_var('py_version_nodot'))")
COVERAGE_FILE := $(BUILDDIR)/.coverage-$(PY_VERSION_NODOT)-$(PY_PLATFORM)
PRE_COMMIT_OPTIONS := --show-diff-on-failure --color=always --all-files --hook-stage=manual
CIBW_ONLY := cp$(PY_VERSION_NODOT)-manylinux_$(ARCH)

.PHONY: all
all: install

.PHONY: pre-commit
pre-commit: install
	@(pre-commit run $(PRE_COMMIT_OPTIONS) || true) | more
	@pre-commit gc

.PHONY: pylint
pylint:
	@if ! which pylint; then uv pip install --upgrade pylint; fi
	@pylint cx_Freeze

.PHONY: clean
clean: uninstall
	@if which pre-commit && [ -f .git/hooks/pre-commit ]; then\
		pre-commit clean;\
		pre-commit uninstall;\
		rm -f .git/hooks/pre-commit;\
	fi
	@$(MAKE) -C doc clean
	@if which coverage; then\
		coverage erase --data-file=$(COVERAGE_FILE);\
		coverage erase;\
	fi

.PHONY: install
install:
	if ! which uv; then\
		python -m pip install --upgrade uv --disable-pip-version-check;\
	fi
	if ! which pre-commit || ! [ -f .git/hooks/pre-commit ]; then\
		uv pip install --upgrade --resolution=highest\
			-r requirements.txt \
			-r requirements-dev.txt -r requirements-doc.txt &&\
		uv pip install -e. --no-build-isolation --no-deps &&\
		pre-commit install --install-hooks --overwrite -t pre-commit;\
	fi

.PHONY: uninstall
uninstall:
	@uv pip uninstall cx_Freeze || true
	@# remove editable wheel modules that exist in bases/lib-dynload
	@rm -rf cx_Freeze/bases/lib-dynload/*$(EXT_SUFFIX)

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
		uv pip install -r requirements-doc.txt --upgrade --resolution=highest &&\
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
install_test: uninstall
	if ! which pytest; then\
		uv pip install --upgrade --resolution=highest\
		-r requirements.txt -r requirements-dev.txt -r requirements-test.txt;\
	fi
	uv pip install -e. --no-build-isolation --no-deps

.PHONY: test
test: install_test
	pytest -nauto --no-cov

.PHONY: cov
cov: install_test
	@rm -rf $(BUILDDIR)/coverage
	pytest -nauto --cov="cx_Freeze" --cov-report=html
	coverage report
	@python -m webbrowser -t $(BUILDDIR)/coverage/index.html

.PHONY: cov2
cov2: install_test
	coverage erase
	COVERAGE_FILE=$(COVERAGE_FILE) coverage erase
	COVERAGE_FILE=$(COVERAGE_FILE) pytest -nauto --cov="cx_Freeze" || true
ifeq ($(PY_PLATFORM),win-amd64)
	# Extra coverage for Windows
	# to test lief < 0.14
	uv pip install "lief==0.13.2"
	COVERAGE_FILE=$(COVERAGE_FILE)-1 pytest -nauto --cov="cx_Freeze" \
		tests/test_command_build.py tests/test_command_build_exe.py \
		tests/test_winversioninfo.py
	# to test without lief (LIEF_DISABLED)
	CX_FREEZE_BIND=imagehlp \
	COVERAGE_FILE=$(COVERAGE_FILE)-2 pytest -nauto --cov="cx_Freeze" \
		tests/test_command_build.py tests/test_command_build_exe.py \
		tests/test_winversioninfo.py
	# to coverage winversioninfo using pywin32
	uv pip install --upgrade pywin32
	COVERAGE_FILE=$(COVERAGE_FILE)-3 pytest -nauto --cov="cx_Freeze" \
		tests/test_winversioninfo.py
	uv pip uninstall pywin32
	uv pip install "lief>0.13.2"
endif
ifeq ($(PY_PLATFORM),linux-x86_64)
	if ! ls wheelhouse/cx_Freeze-$(bump-my-version show current_version|sed 's/-/./')-cp$(PY_VERSION_NODOT)-cp$(PY_VERSION_NODOT)-manylinux_*_$(ARCH).whl 1> /dev/null 2>&1 \
	&& which podman; then\
		CIBW_CONTAINER_ENGINE=podman cibuildwheel --only $(CIBW_ONLY);\
	fi
	$(MAKE) uninstall
	uv pip install cx_Freeze --no-index --no-deps -f wheelhouse
	COVERAGE_FILE=$(COVERAGE_FILE)-4 pytest -nauto --cov="cx_Freeze" || true
endif
	coverage combine --keep $(BUILDDIR)/.coverage-*
	@rm -rf $(BUILDDIR)/coverage
	coverage html
	coverage report
	@python -m webbrowser -t $(BUILDDIR)/coverage/index.html

.PHONY: release
release:
	@echo "# Run:\n"\
	"bump-my-version bump release\n"\
	"git push origin `git branch --show-current` --tags"

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
