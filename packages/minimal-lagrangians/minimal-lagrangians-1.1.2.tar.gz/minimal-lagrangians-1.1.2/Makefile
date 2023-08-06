.PHONY: build clean publish

build:
	python3 setup.py sdist bdist_wheel

clean:
	python3 setup.py clean --all
	rm -rf build/ dist/ *.egg-info/

publish: clean build
	python3 -m twine upload dist/*
