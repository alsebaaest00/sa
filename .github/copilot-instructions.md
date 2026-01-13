# Copilot / Agent instructions for `sa` 🔧

## Purpose ✅
- Provide concise, project-specific guidance so an AI coding agent can be productive immediately.

## Current snapshot (updated) 🧾
- This repository contains a minimal Python scaffold:
  - `pyproject.toml` (Poetry) with dev deps: **pytest**, **black**, **pre-commit**
  - `src/sa/__init__.py` (package layout under `src/`)
  - `tests/test_placeholder.py` (pytest test)
  - `.github/workflows/python-ci.yml` (CI: pre-commit checks, tests + coverage)
  - `LICENSE` (MIT — update author/year if needed)
  - `.github/ISSUE_TEMPLATE` and `.github/PULL_REQUEST_TEMPLATE.md`
  - `README.md` with quickstart and badges

- Draft PRs were created to get this scaffold and tooling in place: **#2** (scaffold), **#3** (quality), **#4** (professionalize), **#5** (advanced). See issue **#1** to change language/license/CI.

## First actions (MANDATORY) ✋
1. Confirm preferences before changing language/CI/license further: respond to issue **#1** or comment on PR **#2** with choices (language, license, CI scope).
2. If maintainers approve a scaffold change, open a small, focused PR that references issue #1 and includes minimal diffs and explicit test instructions.

## Local dev & CI notes 🔧
- Python version: **3.11** (workflow uses `actions/setup-python@v4`).
- Recommended dev workflow:
  - Install Poetry: `python -m pip install --upgrade pip && pip install poetry`
  - Install deps: `poetry install --no-interaction`
  - Install pre-commit hooks: `poetry run pre-commit install`
  - Run pre-commit locally: `poetry run pre-commit run --all-files` (this runs `black` and `ruff` via hooks)
  - Run tests: `poetry run pytest -q --cov=src --cov-report=xml`
- CI workflow: `.github/workflows/python-ci.yml` runs pre-commit checks and tests with coverage. To enable Codecov uploads, add a repository secret named `CODECOV_TOKEN` via **Settings → Secrets and variables → Actions → New repository secret**. The workflow will skip uploads if `CODECOV_TOKEN` is not set.

## Project-specific conventions ⚙️
- Package code lives under `src/` and tests under `tests/`.
- Use **Poetry** metadata in `pyproject.toml` for packaging and dev tooling.
- Formatting/linting: use `pre-commit` (hooks include **black** and **ruff**) and respect these checks in PRs.
- Use the provided PR template (`.github/PULL_REQUEST_TEMPLATE.md`) checklist when proposing changes.

## Allowed low-risk changes (can be implemented without explicit approval) 🔍
- Fix typos or clarify text in `README.md` and small doc edits.
- Add/adjust non-invasive metadata (e.g., update `pyproject.toml` dev dependencies) with a small PR.
- Add small helper scripts or CI improvements that don't change release pipelines (open PR and reference issue #1 where appropriate).

## Changes that require explicit approval (do NOT merge without confirmation) 🚫
- Replacing the primary language/stack (e.g., switching from Python to Node). Open issue #1 and wait for approval.
- Adding or modifying release workflows, deployment pipelines, or secrets.
- Significant architecture or public API changes.

## Testing & verification ✅
- Running the commands in **Local dev & CI notes** should reproduce CI behavior locally.
- Keep PRs small and include test steps in the PR description.

## Commit/PR etiquette ✍️
- Use clear, imperative commit messages (e.g., `feat: add feature`, `chore(ci): add lint step`).
- Use the PR template and checklist; ensure CI checks pass before requesting review.

## Helpful examples from this repo 📎
- `README.md` — quickstart and badges demonstrate how to run the project locally.

---
If anything in this file is unclear or you'd like more examples (e.g., alternative scaffolding for Node or Go), tell me which sections to expand or any repo-specific policies you want enforced. 🙏

## Purpose ✅
- Provide concise, project-specific guidance so an AI coding agent can be productive immediately.

## Current snapshot (updated) 🧾
- This repository contains a minimal Python scaffold:
  - `pyproject.toml` (Poetry) with dev deps: **pytest**, **black**, **pre-commit**
  - `src/sa/__init__.py` (package layout under `src/`)
  - `tests/test_placeholder.py` (pytest test)
  - `.github/workflows/python-ci.yml` (CI: pre-commit checks, tests + coverage)
  - `LICENSE` (MIT — update author/year if needed)
  - `.github/ISSUE_TEMPLATE` and `.github/PULL_REQUEST_TEMPLATE.md`
  - `README.md` with quickstart and badges

- Draft PRs were created to get this scaffold and tooling in place: **#2** (scaffold), **#3** (quality), **#4** (professionalize), **#5** (advanced). See issue **#1** to change language/license/CI.

## First actions (MANDATORY) ✋
1. Confirm preferences before changing language/CI/license further: respond to issue **#1** or comment on PR **#2** with choices (language, license, CI scope).
2. If maintainers approve a scaffold change, open a small, focused PR that references issue #1 and includes minimal diffs and explicit test instructions.

## Local dev & CI notes 🔧
- Python version: **3.11** (workflow uses `actions/setup-python@v4`).
- Recommended dev workflow:
  - Install Poetry: `python -m pip install --upgrade pip && pip install poetry`
  - Install deps: `poetry install --no-interaction`
  - Install pre-commit hooks: `poetry run pre-commit install`
  - Run pre-commit locally: `poetry run pre-commit run --all-files` (this runs `black` and `ruff` via hooks)
  - Run tests: `poetry run pytest -q --cov=src --cov-report=xml`
- CI workflow: `.github/workflows/python-ci.yml` runs pre-commit checks and tests with coverage; some runs previously included a dependency-review step that failed in the runner and was removed.

## Project-specific conventions ⚙️
- Package code lives under `src/` and tests under `tests/`.
- Use **Poetry** metadata in `pyproject.toml` for packaging and dev tooling.
- Formatting/linting: use `pre-commit` (hooks include **black** and **ruff**) and respect these checks in PRs.
- Use the provided PR template (`.github/PULL_REQUEST_TEMPLATE.md`) checklist when proposing changes.

## Allowed low-risk changes (can be implemented without explicit approval) 🔍
- Fix typos or clarify text in `README.md` and small doc edits.
- Add/adjust non-invasive metadata (e.g., update `pyproject.toml` dev dependencies) with a small PR.
- Add small helper scripts or CI improvements that don't change release pipelines (open PR and reference issue #1 where appropriate).

## Changes that require explicit approval (do NOT merge without confirmation) 🚫
- Replacing the primary language/stack (e.g., switching from Python to Node). Open issue #1 and wait for approval.
- Adding or modifying release workflows, deployment pipelines, or secrets.
- Significant architecture or public API changes.

## Testing & verification ✅
- Running the commands in **Local dev & CI notes** should reproduce CI behavior locally.
- Keep PRs small and include test steps in the PR description.

## Commit/PR etiquette ✍️
- Use clear, imperative commit messages (e.g., `feat: add feature`, `chore(ci): add lint step`).
- Use the PR template and checklist; ensure CI checks pass before requesting review.

## Helpful examples from this repo 📎
- `README.md` — short single-line file; use it as the authoritative source for any initial wording changes.

---
If anything in this file is unclear or you'd like more examples (e.g., alternative scaffolding for Node or Go), tell me which sections to expand or any repo-specific policies you want enforced. 🙏

## Safety & assumptions ⚠️
- If repository intent is ambiguous, **stop and ask**—do not add implementation that could conflict with the owner's goals.
- Avoid adding third-party services or secrets. If a service is necessary, document required secrets and request them explicitly from maintainers.

## Current snapshot (updated) 🧾
- This repository now contains a minimal Python scaffold:
  - `pyproject.toml` (Poetry) with dev deps: **pytest**, **black**, **pre-commit**
  - `src/sa/__init__.py` (package layout under `src/`)
  - `tests/test_placeholder.py` (pytest test)
  - `.github/workflows/python-ci.yml` (CI: pre-commit checks, tests + coverage)
  - `LICENSE` (MIT — update author/year if needed)
  - `.github/ISSUE_TEMPLATE/project-setup.md` and `.github/PULL_REQUEST_TEMPLATE.md`
  - `README.md` was updated to reflect the scaffold

- Draft PRs created: **#2** (scaffold), **#3** (quality), **#4** (professionalize), **#5** (advanced) on branches `scaffold/*`. If you prefer a different stack, respond to issue **#1**.

## First actions (MANDATORY) ✋
1. **Confirm preferences** before changing language/CI/license further: reply to issue **#1** or comment on PR **#2** with choices (language, license, CI scope).
2. If maintainers approve a scaffold change, open a small, focused PR (referencing issue #1) with clear test instructions and minimal diffs.

## Local dev & CI notes 🔧
- Python version: **3.11** (workflow uses `actions/setup-python@v4` with `3.11`).
- Recommended dev workflow:
  - Install Poetry: `python -m pip install --upgrade pip && pip install poetry`
  - Install deps: `poetry install --no-interaction`
  - Install pre-commit hooks: `poetry run pre-commit install`
  - Run pre-commit locally: `poetry run pre-commit run --all-files` (this runs `black` and `ruff` via hooks)
  - Run tests: `poetry run pytest -q --cov=src --cov-report=xml`
- CI workflow: `.github/workflows/python-ci.yml` runs pre-commit checks and tests with coverage; a dependency-review step was previously added but removed because it couldn't be resolved in the runner. To enable Codecov uploads, add a repository secret named `CODECOV_TOKEN` via **Settings → Secrets and variables → Actions → New repository secret**. The workflow will skip uploads if `CODECOV_TOKEN` is not set.

## Project-specific conventions ⚙️
- Package code lives under `src/` and tests under `tests/`.
- Use **Poetry** metadata in `pyproject.toml` for packaging and dev tooling.
- Formatting/linting: use `pre-commit` (hooks include **black** and **ruff**) and respect these checks in PRs.
- Use the provided PR template (`.github/PULL_REQUEST_TEMPLATE.md`) checklist when proposing changes.

## Allowed low-risk changes (can be implemented without explicit approval) 🔍
- Fix typos or clarify text in `README.md` and small doc edits.
- Add/adjust non-invasive metadata (e.g., update `pyproject.toml` dev dependencies) with a small PR.
- Add small helper scripts or CI improvements that don't change release pipelines (open PR and reference issue #1 where appropriate).

## Changes that require explicit approval (do NOT merge without confirmation) 🚫
- Replacing the primary language/stack (e.g., switching from Python to Node). Open issue #1 and wait for approval.
- Adding or modifying release pipelines, deployment workflows, or secrets.
- Significant architecture or public API changes.

## Testing & verification ✅
- Running the commands in **Local dev & CI notes** should reproduce the CI behavior locally.
- Keep PRs small and include test steps in the PR description.

## Commit/PR etiquette ✍️
- Use clear, imperative commit messages (e.g., `feat: add feature`, `chore(ci): add lint step`).
- Use the PR template and checklist; mark CI-related checks as passing before requesting review.
---
If anything in this file is unclear or you'd like more examples (e.g., alternative scaffolding for Node or Go), tell me which sections to expand or any repo-specific policies you want enforced. 🙏

## Safety & assumptions ⚠️
- If repository intent is ambiguous, **stop and ask**—do not add implementation that could conflict with the owner's goals.
- Avoid adding third-party services or secrets. If a service is necessary, document required secrets and request them explicitly from maintainers.

## Helpful examples from this repo 📎
- `README.md` — short single-line file; use it as the authoritative source for any initial wording changes.

---
If anything in this file is unclear or incomplete, please tell me which sections to expand or any repo-specific policies you want enforced. 🙏
