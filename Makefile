.PHONY: build, install, test, rate

build:
	venv/scripts/python.exe build_tools/build.py

mock:
	venv/scripts/python.exe test_tools/build_mock_data.py

install:
	. venv/Scripts/activate
	pip install -e . --use-feature=in-tree-build;

test:
	pytest tests -v ${args}

rate:
	-flake8 src/spotifywrapper
	-pylint src/spotifywrapper
