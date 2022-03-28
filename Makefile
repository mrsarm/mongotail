.PHONY: clean install install-dev uninstall check-mongotail-version build upload upload-test
.DEFAULT_GOAL := install

VENV ?= venv

SYSTEM_PYTHON  = $(or $(shell which python3), $(shell which python))
SYSTEM_PIP     = $(or $(shell which pip3), $(shell which pip))
PYTHON	= $(or $(wildcard $(VENV)/bin/python), $(SYSTEM_PYTHON))
PIP		= $(or $(wildcard $(VENV)/bin/pip), $(SYSTEM_PIP))

# PyPI test repo
TEST_REPO = testpypi
TEST_INDEX_URL = https://test.pypi.org/simple/

# PyPI main repo
MAIN_REPO = pypi
MAIN_INDEX_URL = https://pypi.org/simple/

REPO = ${MAIN_REPO}
INDEX_URL = ${MAIN_INDEX_URL}


PIP_ARGS = --index-url ${MAIN_INDEX_URL}

clean:
	rm -fR build/ dist/ .eggs/ mongotail.egg-info/

clean-all: clean
	rm -Rf ${VENV}

install:
	${PIP} install ${PIP_ARGS} .

# Install mongotail in editable mode, linking the module with the local project path
install-dev: ${VENV}
	${PIP} install ${PIP_ARGS} -e .

uninstall:
	yes | ${PIP} uninstall mongotail

update-dev-dependencies:
	${PIP} install ${PIP_ARGS} -U pip wheel setuptools
	${PIP} install ${PIP_ARGS} -U build twine

${VENV}:
	${PYTHON} -m venv ${VENV}
	$(eval PIP := $(shell echo ${VENV}/bin/pip))
	${MAKE} update-dev-dependencies

check-mongotail-version:
	${VENV}/bin/mongotail --version

# Build distributable
build:
	${PYTHON} -m build

# Upload the distributable packages on PyPI
upload: build
	${PYTHON} -m twine upload --repository ${REPO} dist/*

# Upload the distributable packages on test PyPI
upload-test: build
	${PYTHON} -m twine upload --repository ${TEST_REPO} dist/*

# Install the distributable package from PyPI
install-from-pypi:
	${PYTHON} -m pip install --index-url ${INDEX_URL} --extra-index-url ${MAIN_INDEX_URL} -U --pre mongotail

#build-docker-image:
	# Remember to update the version in the Dockerfile first !
#	docker build -t mrsarm/mongotail:3.0.0 .
#	docker push mrsarm/mongotail:3.0.0
#	docker tag mrsarm/mongotail:3.0.0 mrsarm/mongotail:latest
#   docker push mrsarm/mongotail:3.0.0
#   docker push mrsarm/mongotail:latest