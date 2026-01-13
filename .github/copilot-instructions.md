# Copilot / Agent instructions for `sa` 🔧

## Purpose ✅
- Provide concise, project-specific guidance so an AI coding agent can be productive immediately.

## Current snapshot 🧾
- This repository currently contains a single file: `README.md` with the repo title `sa`.
- **No source code, tests, CI workflows, or language-specific files were found.**

## First actions (MANDATORY) ✋
1. **Ask the repo owner/maintainer** clarifying questions before adding language-specific code or CI: which language/framework should the project use, preferred license, and preferred CI provider.
2. If contact info or issue templates are missing, **open an issue** describing the recommended minimal scaffolding and ask for approval before implementing.

## Allowed low-risk changes (can be implemented without explicit approval) 🔍
- Fix typos or clarify text in `README.md` and small doc edits.
- Add a minimal `.github/copilot-instructions.md` (this file) to help future agents.
- Add metadata files (e.g., `LICENSE`, `CONTRIBUTING.md`) **only** if the intended license and contribution policy are obvious or explicitly stated by the owner.

## Changes that require approval (do NOT merge without confirmation) 🚫
- Adding language scaffolding (e.g., `package.json`, `pyproject.toml`, `src/` layout).
- Creating CI workflows that run builds/tests or modify release pipelines.
- Adding large code features, changing architecture, or modifying public APIs.

## When you propose scaffolding or features — make a clear PR template 🧩
- Start with an **issue** that lists: motivation, suggested files, minimal example, and how you'll test it locally.
- PRs should be small and scoped (one logical change per PR) and include:
  - A short description, rationale, and migration notes (if any).
  - How to run or test the change locally (commands). If unknown, ask the owner before adding run scripts.

## Testing & CI 🔬
- No tests or CI were found. **Do not assume** a language's default test runner or CI configuration—ask first.
- If asked to add CI, prefer a minimal job that checks formatting and runs tests; include docs on required secrets and permissions.

## Commit/PR etiquette ✍️
- Use clear, imperative commit messages (e.g., `feat: add CI skeleton`, `chore: add MIT license`).
- Include a descriptive PR title and summary that explains behavior, not just the files changed.

## Safety & assumptions ⚠️
- If repository intent is ambiguous, **stop and ask**—do not add implementation that could conflict with the owner's goals.
- Avoid adding third-party services or secrets. If a service is necessary, document required secrets and request them explicitly from maintainers.

## Helpful examples from this repo 📎
- `README.md` — short single-line file; use it as the authoritative source for any initial wording changes.

---
If anything in this file is unclear or incomplete, please tell me which sections to expand or any repo-specific policies you want enforced. 🙏