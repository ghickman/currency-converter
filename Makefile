SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo " make test          | Run the test suite."
	@echo " make release       | Release to the PyPI."

test:
	tox

release:
	python setup.py register sdist bdist_wheel upload
