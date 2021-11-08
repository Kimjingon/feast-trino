
.PHONY: build

ROOT_DIR 	:= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

format:
	# Sort
	cd ${ROOT_DIR}; python -m isort feast_trino/

	# Format
	cd ${ROOT_DIR}; python -m black --target-version py37 feast_trino

lint:
	cd ${ROOT_DIR}; python -m mypy feast_trino/
	cd ${ROOT_DIR}; python -m isort feast_trino/ --check-only
	cd ${ROOT_DIR}; python -m flake8 feast_trino/
	cd ${ROOT_DIR}; python -m black --target-version py37 --check feast_trino 

build:
	rm -rf dist/*
	python setup.py sdist bdist_wheel

install-ci-dependencies:
	pip install -e ".[ci]"

start-trino-locally:
	docker run --detach --rm -p 8080:8080 --name trino -v ${ROOT_DIR}/config/catalog/:/etc/catalog/:ro trinodb/trino:364

stop-trino-locally:
	docker stop trino