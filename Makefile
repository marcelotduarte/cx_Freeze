# Makefile to automate some tools

.PHONY: black
black:
	pip install --upgrade black isort pyupgrade
	find . -name '*.py' \
		! -path './tests/samples/invalid_syntax.py' \
		! -path './cx_Freeze/samples/*/build/**.py' \
		-exec pyupgrade --py36-plus {} + || true
	isort . || true
	black . || true

.PHONY: clean
clean:
	make -C doc clean

.PHONY: html
html:
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
