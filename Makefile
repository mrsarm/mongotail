.PHONY: clean install install-dev uninstall check-mongotail-version
.DEFAULT_GOAL := install

VENV=venv

SYSTEM_PYTHON  = $(or $(shell which python3), $(shell which python))
SYSTEM_PIP     = $(or $(shell which pip3), $(shell which pip))
PYTHON	= $(or $(wildcard $(VENV)/bin/python), $(SYSTEM_PYTHON))
PIP		= $(or $(wildcard $(VENV)/bin/pip), $(SYSTEM_PYTHON))

clean:
	rm -fR build/
	rm -fR dist/
	rm -fR .eggs/

clean-all: clean
	rm -Rf ${VENV}

install:
	${PIP} install .

# Install mongotail in editable mode, linking the module with the local project path
install-dev: ${VENV}
	${PIP} install -e .

uninstall:
	yes | ${PIP} uninstall mongotail

${VENV}:
	${PYTHON} -m venv ${VENV}
	${PIP} install -U pip wheel setuptools

check-mongotail-version:
	${VENV}/bin/mongotail --version
