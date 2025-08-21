.PHONY : all clean build upload test test-verbose test-coverage

all: install clean

clean:
	@rm -rf `find ./ -type d -name "*__pycache__"`
	@rm -rf ./build/ ./dist/ ./bhopengraph.egg-info/

generate-docs:
	@python3 -m pip install pdoc --break-system-packages
	@echo "[$(shell date)] Generating docs ..."
	@PDOC_ALLOW_EXEC=1 python3 -m pdoc -d markdown -o ./documentation/ ./bhopengraph/
	@echo "[$(shell date)] Done!"

uninstall:
	pip uninstall bhopengraph --yes --break-system-packages

install: build
	pip install . --break-system-packages

build:
	python3 -m pip uninstall bhopengraph --yes --break-system-packages
	python3 -m pip install .[build] --break-system-packages
	python3 -m build --wheel

upload: build
	python3 -m pip install .[twine] --break-system-packages
	python3 -m twine upload dist/*

test:
	@echo "[$(shell date)] Running tests ..."
	@cd bhopengraph/tests && python3 run_tests.py
	@echo "[$(shell date)] Tests completed!"

test-verbose:
	@echo "[$(shell date)] Running tests with verbose output ..."
	@cd bhopengraph/tests && python3 -m unittest discover -v
	@echo "[$(shell date)] Tests completed!"

test-coverage:
	@echo "[$(shell date)] Installing coverage and running tests with coverage ..."
	@python3 -m pip install coverage --break-system-packages
	@coverage run --source=bhopengraph bhopengraph/tests/run_tests.py
	@coverage report
	@coverage html
	@echo "[$(shell date)] Coverage report generated in htmlcov/"
