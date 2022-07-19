# Makefile to automate some tools

.PHONY: all
all:
	pre-commit run -a -v --hook-stage manual
	pre-commit gc

.PHONY: clean
clean:
	pre-commit clean
	make -C doc clean

.PHONY: upgrade
upgrade:
	make all || true
	make clean || true
	python -m pip install -U pip
	pip install -r requirements-dev.txt --upgrade --upgrade-strategy eager
	pip install -e .
	pre-commit autoupdate
	make all
	git diff || true

.PHONY: html
html:
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
