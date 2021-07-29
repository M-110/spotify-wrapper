.PHONY: install, test, rate, clean

install:
	. venv/Scripts/activate
	pip install -e . --use-feature=in-tree-build;

test:
	pytest tests -v ${args}

rate:
	-flake8 src/tasks
	-pylint src/tasks

clean:
	@echo hello $(name)
	which pip