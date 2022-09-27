# Makefile to automate some tools

.PHONY: all
all: install
	pre-commit run -a -v --hook-stage manual
	pre-commit gc

.PHONY: clean
clean:
	if [ -f .git/hooks/pre-commit ] ; then\
		pre-commit clean;\
		pre-commit uninstall;\
		rm -f .git/hooks/pre-commit;\
	fi
	make -C doc clean

.PHONY: install
install:
	if ! [ -f .git/hooks/pre-commit ] ; then\
		python -m pip install --upgrade pip &&\
		pip install -r requirements-dev.txt --upgrade --upgrade-strategy eager &&\
		pip install -e . --no-build-isolation --no-deps &&\
		pre-commit install --install-hooks --overwrite -t pre-commit;\
	fi

.PHONY: upgrade
upgrade:
	if [ -f .git/hooks/pre-commit ] ; then\
		make all || true;\
		make clean || true;\
		pip uninstall -y cx_Freeze || true;\
	fi
	make install
	pre-commit autoupdate
	make all
	git diff || true

.PHONY: html
html: install
	pre-commit run build-docs -a -v --hook-stage manual

.PHONY: htmltest
htmltest:
	make -C doc test

.PHONY: epub
epub:
	make -C doc epub

.PHONY: pdf
pdf:
	make -C doc pdf

.PHONY: tests
tests:
	python -m pytest

.PHONY: cov
cov:
	python -m pytest -m "not long" --cov="cx_Freeze" --cov-report=html
	python -m webbrowser -t ./htmlcov/index.html
