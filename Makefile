# Makefile to automate some tools

BUILDDIR := ./build
EXT_SUFFIX := $(shell python -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))")
PY_VERSION_NODOT := $(shell python -c "import sysconfig; print(sysconfig.get_config_var('py_version_nodot'))")
ARCH := $(shell python -c "import platform; print(platform.machine().lower())")
PY_PLATFORM := $(shell python -c "import sysconfig; print(sysconfig.get_platform())")
COVERAGE_FILE := $(BUILDDIR)/.coverage-$(PY_VERSION_NODOT)-$(PY_PLATFORM)
PRE_COMMIT_OPTIONS := --show-diff-on-failure --color=always --all-files --hook-stage=manual

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
	@make -C doc clean
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
	make pre-commit

.PHONY: html
html: install
	@if which pre-commit && [ -f .git/hooks/pre-commit ]; then\
		pre-commit run blacken-docs $(PRE_COMMIT_OPTIONS);\
		pre-commit run build-docs $(PRE_COMMIT_OPTIONS);\
	else\
		pip install -e .[doc] --no-build-isolation &&\
		make -C doc html;\
	fi

.PHONY: htmltest
htmltest:
	make -C doc test

.PHONY: doc
doc: html
	make -C doc epub
	make -C doc pdf

.PHONY: install_test
install_test:
	if ! which pytest || ! which cxfreeze; then\
		pip install -e .[test] --no-build-isolation;\
	fi

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
	COVERAGE_FILE=$(COVERAGE_FILE) python -m pytest -nauto --cov=cx_Freeze
ifeq ($(PY_PLATFORM),win-amd64)
	# Extra coverage for Windows
	# to test lief < 0.14
	pip install "lief==0.13.2"
	COVERAGE_FILE=$(COVERAGE_FILE)-1 python -m pytest -nauto --cov=cx_Freeze\
		tests/test_command_build.py tests/test_command_build_exe.py\
		tests/test_winversioninfo.py
	# to test without lief (LIEF_DISABLED)
	CX_FREEZE_BIND=imagehlp \
	COVERAGE_FILE=$(COVERAGE_FILE)-2 python -m pytest -nauto --cov=cx_Freeze\
		--cov=cx_Freeze --cov-report=xml:./coverage/coverage2.xml\
		tests/test_command_build.py tests/test_command_build_exe.py\
		tests/test_winversioninfo.py
	# to coverage winversioninfo using pywin32
	pip install --upgrade pywin32
	COVERAGE_FILE=$(COVERAGE_FILE)-3 python -m pytest -nauto --cov=cx_Freeze\
		--cov=cx_Freeze --cov-report=xml:./coverage/coverage3.xml\
		tests/test_winversioninfo.py
	pip uninstall -y pywin32
	pip install "lief>0.13.2"
endif
	coverage combine --keep $(BUILDDIR)/.coverage-*
	rm -rf $(BUILDDIR)/coverage
	coverage html
	python -m webbrowser -t $(BUILDDIR)/coverage/index.html

.PHONY: install_test_pre
install_test_pre: install_test
	# Hack to bind to manylinux or macpython extensions
	@mkdir -p wheelhouse
	@rm -f wheelhouse/cx_Freeze-*-cp$(PY_VERSION_NODOT)*_$(ARCH).whl
	pip download cx_Freeze --pre --no-deps \
		--index-url https://marcelotduarte.github.io/packages/ -d wheelhouse
	unzip -q -o wheelhouse/cx_Freeze-*-cp$(PY_VERSION_NODOT)*_$(ARCH).whl "cx_Freeze/bases/*" -x "*.py"

.PHONY: test-pre
test-pre: install_test_pre
	python -m pytest -o pythonpath=cx_Freeze/bases/lib-dynload/

.PHONY: cov-pre
cov-pre: install_test_pre
	python -m pytest --cov=cx_Freeze --cov-report=html\
		-o pythonpath=cx_Freeze/bases/lib-dynload/
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
