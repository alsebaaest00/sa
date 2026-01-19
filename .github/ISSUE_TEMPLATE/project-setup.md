---
name: Project setup / scaffolding request
about: Use this to specify language, license, and CI preferences when requesting initial project scaffolding
---

# Project Setup

**Preferred language/framework**: Python 3.11+ (Poetry for dependency management)

**Preferred license**: MIT License

**Preferred CI and scope**: GitHub Actions - linting (black, ruff, mypy, pylint) + pytest with coverage

**Repo structure preferences**:

- `src/sa/` - Main application code
  - `api/` - FastAPI REST endpoints
  - `generators/` - Image, Video, Audio generators
  - `ui/` - Streamlit web interface
  - `utils/` - Configuration and utilities
- `tests/` - Unit and integration tests
- `outputs/` - Generated media files
- `monitoring/` - Prometheus & Grafana configs

**Any files to explicitly exclude**:

- `.env` (API keys - use `.env.example` as template)
- `outputs/`, `mlruns/`, `logs/` (runtime data)
- Virtual environments (`.venv/`, `venv/`)

**Additional notes / requirements**:

- Multi-modal AI platform: Text → Image (Replicate) → Video (MoviePy) → Audio (ElevenLabs/gTTS)
- Three interfaces: Streamlit UI, FastAPI REST API, CLI scripts
- Pre-commit hooks configured for code quality
- Full Arabic language support in UI
- API key management with validation
