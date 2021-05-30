# Makefile to automate some tools

.PHONY: black
black:
	pip install --upgrade black pyupgrade
	find . -name '*.py' \
    	! -path './test/samples/invalid_syntax.py' \
    	! -path './cx_Freeze/samples/*/build/**.py' \
    	-exec pyupgrade --py36-plus {} + || true
	find . -name '*.py' \
    	! -path './test/samples/invalid_syntax.py' \
    	! -path './cx_Freeze/samples/*/build/**.py' \
    	-exec black -l 79 -t py36 {} + || true

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
test:
	make -C doc test

.PHONY: clean
clean:
	make -C doc clean
