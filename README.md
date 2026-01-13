# sa

[![CI](https://github.com/alsebaaest00-hue/sa/actions/workflows/python-ci.yml/badge.svg)](https://github.com/alsebaaest00-hue/sa/actions/workflows/python-ci.yml) [![Codecov](https://codecov.io/gh/alsebaaest00-hue/sa/branch/main/graph/badge.svg)](https://codecov.io/gh/alsebaaest00-hue/sa) [![Dependabot Status](https://img.shields.io/badge/dependabot-enabled-brightgreen)](https://github.com/alsebaaest00-hue/sa/network/updates) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://pre-commit.com/) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/alsebaaest00-hue/sa/main.svg)](https://results.pre-commit.ci/latest/github/alsebaaest00-hue/sa/main) [![License](https://img.shields.io/github/license/alsebaaest00-hue/sa)](LICENSE)

Minimal scaffold created as an example Python project. If you would like a different language, license, or CI, please respond to issue #1 with your preferences.

## Quickstart

- Install Poetry and dependencies:

```bash
python -m pip install --upgrade pip && pip install poetry
poetry install --no-interaction
```

- Run linters and tests:

```bash
poetry run pre-commit run --all-files
poetry run pytest -q --cov=src --cov-report=xml
```

- Install pre-commit hooks locally:

```bash
poetry run pre-commit install
poetry run pre-commit run --all-files
```

## Codecov (optional)

If you'd like coverage uploads to Codecov (useful for protected branches), add a repository secret named `CODECOV_TOKEN`:

- Go to GitHub → Settings → **Secrets and variables** → **Actions** → **New repository secret**.
- Set **Name** = `CODECOV_TOKEN` and **Value** = the token provided by Codecov for this repository.

The CI workflow will skip uploads if `CODECOV_TOKEN` is not set.
