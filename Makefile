# Makefile for Amlexa.
#
# Author:: Greg Albrecht W2GMD <gba@orionlabs.co>
# Copyright:: Copyright 2016 Orion Labs, Inc.
# License:: Apache License, Version 2.0
#


.DEFAULT_GOAL := all


all: install_requirements develop

develop:
	python setup.py develop

install:
	python setup.py install

install_requirements:
	pip install --upgrade -r requirements.txt

uninstall:
	pip uninstall -y amlexa

clean:
	rm -rf *.egg* build dist *.py[oc] */*.py[co] cover doctest_pypi.cfg \
		nosetests.xml pylint.log *.egg output.xml flake8.log tests.log \
		test-result.xml htmlcov fab.log *.deb *.eggs

nosetests:
	python setup.py nosetests

pep8:
	flake8

flake8: install_requirements
	flake8 --max-complexity 12 --exit-zero amlexa/*.py *.py

lint: install_requirements
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
	-r n amlexa/*.py *.py || exit 0

test: lint flake8 nosetests
