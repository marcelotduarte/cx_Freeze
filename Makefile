# Makefile to automate some tools

BUILDDIR = ./build
EXT_SUFFIX := $(shell python -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))")
PY_VERSION_NODOT := $(shell python -c "import sysconfig; print(sysconfig.get_config_var('py_version_nodot'))")
ARCH := $(shell python -c "import platform; print(platform.machine().lower())")

.PHONY: all
all: install

.PHONY: pre-commit
pre-commit: install
	@SKIP=pylint pre-commit run -a --hook-stage manual || true
	@pre-commit gc

.PHONY: pre-commit-all
pre-commit-all: install
	@pre-commit run -a --hook-stage manual || true
	@pre-commit gc

.PHONY: pylint
pylint:
	pip install --upgrade pylint
	@pre-commit run pylint -a -v --hook-stage manual

.PHONY: clean
clean:
	@if which pre-commit && [ -f .git/hooks/pre-commit ]; then\
		pre-commit clean;\
		pre-commit uninstall;\
		rm -f .git/hooks/pre-commit;\
	fi
	@make -C doc clean

.PHONY: install
install:
	if ! which pre-commit || ! [ -f .git/hooks/pre-commit ]; then\
		python -m pip install --upgrade pip &&\
		pip install -e .[dev,doc] &&\
		pre-commit install --install-hooks --overwrite -t pre-commit;\
	fi

.PHONY: upgrade
upgrade: clean
	@rm -f .git/hooks/pre-commit || true
	pip uninstall -y cx_Freeze || true
	pip install --upgrade pre-commit
	pre-commit autoupdate
	make pre-commit
	git diff || true

.PHONY: html
html: install
	@if which pre-commit && [ -f .git/hooks/pre-commit ]; then\
		pre-commit run blacken-docs -a --hook-stage manual;\
		pre-commit run build-docs -a -v --hook-stage manual;\
	else\
		pip install -e .[doc] &&\
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
	pip install -e .[test]

.PHONY: test
test: install_test
	python -m pytest

.PHONY: cov
cov: install_test
	python -m pytest \
		--cov="cx_Freeze" \
		--cov-report=html:$(BUILDDIR)/coverage \
		--cov-report=xml:$(BUILDDIR)/coverage.xml
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
	python -m pytest -o pythonpath=cx_Freeze/bases/lib-dynload/ \
		--cov="cx_Freeze" \
		--cov-report=html:$(BUILDDIR)/coverage \
		--cov-report=xml:$(BUILDDIR)/coverage.xml
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
