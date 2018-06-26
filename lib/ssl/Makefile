all: build

build: ssl
	python setup.py build

install:
	python setup.py install

sdist:
	python setup.py sdist

clean:
	python setup.py clean
	rm -rf build

.PHONY: test

test:
	python test/test_ssl.py
