# Voice Assistant Platform (ASR)

Production-oriented voice assistant platform with modular components for:

- Wake word detection
- ASR (speech-to-text)
- NLU (intent and entity extraction)
- Task execution
- Response generation
- TTS (text-to-speech)
- API access, storage, monitoring, and deployment support

## Features

- Modular architecture under `src/voice_assistant`
- Local and cloud-ready deployment (`docker`, `kubernetes`)
- Automated workflows with GitHub Actions (`.github/workflows`)
- Multi-level testing strategy (`tests/unit`, `tests/integration`, `tests/e2e`, `tests/performance`)
- Environment-specific configuration in `config/`

## Repository Structure

Main folders:

- `src/voice_assistant/` - Application source code
- `tests/` - Unit, integration, e2e, and performance tests
- `docs/` - Architecture, API, deployment, and development docs
- `scripts/` - Setup, deployment, maintenance, and testing scripts
- `config/` - Base and environment-specific configuration
- `docker/` - Containerization files
- `kubernetes/` - K8s manifests and Helm chart scaffolding
- `monitoring/` - Metrics, logging, and tracing setup
- `requirements/` - Split dependency files by environment

## Quick Start

### 1. Clone

```bash
git clone https://github.com/Mr-Green07/ASR.git
cd ASR
```

### 2. Create and activate virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows (Git Bash):

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
```

## Development

Use this layout as the baseline implementation guide:

- Core orchestration: `src/voice_assistant/core/orchestrator.py`
- API service: `src/voice_assistant/api/server.py`
- Audio input/output pipeline: `src/voice_assistant/audio/`

You can add module-level implementations incrementally while preserving package boundaries.

## Running Tests

```bash
pytest
```

Run specific suites:

```bash
pytest tests/unit
pytest tests/integration
pytest tests/e2e
pytest tests/performance
```

## Quality Checks

Typical checks used in this project:

- Linting
- Formatting
- Type checks
- Security scanning

These are automated in CI under `.github/workflows/`.

## Deployment

- Local containers: `docker/docker-compose.yml`
- Production-style manifests: `kubernetes/`
- Monitoring setup: `monitoring/`

## Contribution

Please review:

- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`

## License

See `LICENSE`.
