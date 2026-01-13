# sa

[![CI](https://github.com/alsebaaest00-hue/sa/actions/workflows/python-ci.yml/badge.svg)](https://github.com/alsebaaest00-hue/sa/actions/workflows/python-ci.yml) [![Dependabot Status](https://img.shields.io/badge/dependabot-enabled-brightgreen)](https://github.com/alsebaaest00-hue/sa/network/updates) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://pre-commit.com/) [![License](https://img.shields.io/github/license/alsebaaest00-hue/sa)](LICENSE)

Minimal scaffold created as an example Python project. If you would like a different language, license, or CI, please respond to issue #1 with your preferences.

## Quickstart

- Install Poetry and dependencies:

```bash
python -m pip install --upgrade pip && pip install poetry
poetry install --no-interaction
```

- Run linters and tests:

```bash
poetry run ruff check .
poetry run black --check .
poetry run pytest -q
```

- Install pre-commit hooks locally:

```bash
poetry run pre-commit install
poetry run pre-commit run --all-files
```
