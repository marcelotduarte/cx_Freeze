# Makefile to automate some tools

.PHONY: black
black:
	pip install --upgrade pre-commit
	pre-commit run -a

.PHONY: clean
clean:
	make -C doc clean

.PHONY: html
html:
	pip install -e .[doc]
	make -C doc html

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
