# Makefile to automate some tools

.PHONY: black
black:
	pip install --upgrade black pyupgrade
	find . -name '*.py' \
		! -path './tests/samples/invalid_syntax.py' \
		! -path './cx_Freeze/samples/*/build/**.py' \
		-exec pyupgrade --py36-plus {} + || true
	black . -v || true

.PHONY: html
html:
	make -C doc html

.PHONY: epub
epub:
	make -C doc epub

.PHONY: pdf
pdf:
	make -C doc pdf

.PHONY: test
htmltest:
	make -C doc test

.PHONY: clean
clean:
	make -C doc clean
