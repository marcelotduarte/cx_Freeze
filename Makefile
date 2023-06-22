# Makefile to automate some tools

.PHONY: all
all: install

.PHONY: pre-commit
pre-commit: install
	@pre-commit run check-case-conflict -a --hook-stage manual
	@pre-commit run check-toml -a --hook-stage manual
	@pre-commit run check-yaml -a --hook-stage manual
	@pre-commit run end-of-file-fixer -a --hook-stage manual || true
	@pre-commit run fix-byte-order-marker -a --hook-stage manual || true
	@pre-commit run mixed-line-ending -a --hook-stage manual || true
	@pre-commit run trailing-whitespace -a --hook-stage manual || true
	@pre-commit run validate-pyproject -a --hook-stage manual || true
	@pre-commit run ruff -a --hook-stage manual || true
	@pre-commit run black -a --hook-stage manual || true
	@pre-commit run license -a --hook-stage manual || true
	@pre-commit run requirements -a --hook-stage manual || true
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

.PHONY: epub
epub:
	make -C doc epub

.PHONY: pdf
pdf:
	make -C doc pdf

.PHONY: install_test
install_test:
	python -m pip install --upgrade pip
	pip install -e .[test]

.PHONY: test
test: install_test
	python -m pytest

.PHONY: cov
cov: install_test
	@rm -rf ./htmlcov/
	python -m pytest --cov="cx_Freeze" --cov-report=html --cov-report=xml
	python -m webbrowser -t ./htmlcov/index.html

.PHONY: release
release:
	@echo \
	"# Run:\nbump2version --verbose --sign-tags release\n"\
	"git push origin main --tags"

.PHONY: release-patch
release-patch:
	@echo \
	"# Run:\nbump2version --verbose --sign-tags patch --new-version=X.XX.X\n"\
	"git push origin `git branch --show-current` --tags"

.PHONY: release-dev
release-dev:
	if (grep "current_version" .bumpversion.cfg | grep -q "\-dev"); then\
		bump2version --allow-dirty --verbose --no-tag build;\
	else\
		bump2version --allow-dirty --verbose --no-tag minor;\
	fi
