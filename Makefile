.PHONY: venv install dev lint

VENV_DIR = .venv

# Detect OS for venv paths
ifeq ($(OS),Windows_NT)
	PYTHON  = $(VENV_DIR)/Scripts/python
	PIP     = $(VENV_DIR)/Scripts/pip
else
	PYTHON  = $(VENV_DIR)/bin/python
	PIP     = $(VENV_DIR)/bin/pip
endif

venv:
	python -m venv $(VENV_DIR)

install: venv
	$(PIP) install -r requirements.txt

dev:
	$(PYTHON) -m uvicorn main:app --reload --port 8000

lint:
	$(PYTHON) -m ruff check .
