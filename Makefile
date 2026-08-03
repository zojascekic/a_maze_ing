PYTHON := python3
MAIN := a_maze_ing.py
CONFIG := config.txt

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf maze.txt
	rm -rf build dist *.egg-info

build:
	$(PYTHON) -m build

lint:
	flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	$(PYTHON) -m mypy . --strict

.PHONY: install run debug clean build lint lint-strict