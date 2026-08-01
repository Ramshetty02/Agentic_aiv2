.PHONY: setup test lint typecheck security run docker-build smoke

PYTHON ?= python3

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest tests/ -v --cov=agents --cov=tools --cov=utils --cov-report=term-missing

lint:
	$(PYTHON) -m ruff check .
	@test -z "$$(git ls-files '*__pycache__*' '*.pyc')" || (echo "tracked generated Python cache files found" && exit 1)

typecheck:
	$(PYTHON) -m mypy agents tools utils app.py

security:
	$(PYTHON) -m pip_audit -r requirements.txt

run:
	$(PYTHON) -m streamlit run app.py

docker-build:
	docker build -t erevna:local .

smoke:
	$(PYTHON) -m compileall agents tools utils app.py

