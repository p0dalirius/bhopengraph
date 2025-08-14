.PHONY : all clean build upload

all: install clean

clean:
	@rm -rf `find ./ -type d -name "*__pycache__"`
	@rm -rf ./build/ ./dist/ ./bhopengraph.egg-info/

docs:
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
