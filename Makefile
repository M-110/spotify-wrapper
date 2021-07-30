.PHONY: build, install, test, rate

build:
	venv/scripts/python.exe build_tools/build.py

install:
	. venv/Scripts/activate
	pip install -e . --use-feature=in-tree-build;

test:
	pytest tests -v ${args}

rate:
	-flake8 src/spotifywrapper
	-pylint src/spotifywrapper
