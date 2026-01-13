.PHONY: install install-dev lint format test pre-commit-install

install:
	python -m pip install --upgrade pip
	pip install poetry
	poetry install --no-interaction

install-dev:
	poetry install

lint:
	poetry run ruff check .

format:
	poetry run black .

test:
	poetry run pytest -q

pre-commit-install:
	poetry run pre-commit install
	poetry run pre-commit run --all-files
