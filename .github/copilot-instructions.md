# Copilot / Agent instructions for `sa` 🔧

## Purpose ✅
- Provide concise, project-specific guidance so an AI coding agent can be productive immediately.

## Current snapshot (updated) 🧾
- This repository now contains a minimal Python scaffold:
  - `pyproject.toml` (Poetry) with dev deps: **pytest**, **black**, **ruff**
  - `src/sa/__init__.py` (package layout under `src/`)
  - `tests/test_placeholder.py` (pytest test)
  - `.github/workflows/python-ci.yml` (CI: lint/format checks + pytest)
  - `LICENSE` (MIT — update author/year if needed)
  - `.github/ISSUE_TEMPLATE/project-setup.md` and `.github/PULL_REQUEST_TEMPLATE.md`
  - `README.md` was updated to reflect the scaffold

- Draft PR created: **#2** on branch `scaffold/python-mit-gha` (contains the scaffold + CI). If you prefer a different stack, respond to issue **#1**.

## First actions (MANDATORY) ✋
1. **Confirm preferences** before changing language/CI/license further: reply to issue **#1** or comment on PR **#2** with choices (language, license, CI scope).
2. If maintainers approve a scaffold change, open a small, focused PR (referencing issue #1) with clear test instructions and minimal diffs.

## Local dev & CI notes 🔧
- Python version: **3.11** (workflow uses `actions/setup-python@v4` with `3.11`).
- Recommended dev workflow:
  - Install Poetry: `python -m pip install --upgrade pip && pip install poetry`
  - Install deps: `poetry install --no-interaction`
  - Run linters: `poetry run ruff check .`
  - Check formatting: `poetry run black --check .`
  - Run tests: `poetry run pytest -q`
- CI workflow: `.github/workflows/python-ci.yml` performs the same steps during PRs and pushes to `main`. It also runs dependency review and uploads test coverage to Codecov (requires adding a Codecov token secret if desired for private repos).

## Project-specific conventions ⚙️
- Package code lives under `src/` and tests under `tests/`.
- Use **Poetry** metadata in `pyproject.toml` for packaging and dev tooling.
- Formatting/linting: **black** + **ruff** are used in CI and should be respected in PRs.
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

## Safety & assumptions ⚠️
- If repository intent is ambiguous, **stop and ask**—do not add implementation that could conflict with the owner's goals.
- Avoid adding third-party services or secrets. If a service is necessary, document required secrets and request them explicitly from maintainers.

---
If anything in this file is unclear or you'd like more examples (e.g., alternative scaffolding for Node or Go), tell me which sections to expand or any repo-specific policies you want enforced. 🙏