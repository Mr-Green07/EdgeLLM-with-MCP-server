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

If you are not using a virtual environment, you can install dependencies directly in your system Python:

```bash
python -m pip install --upgrade pip
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
```

Note: Installing without a venv can cause version conflicts with other Python projects on the same machine.

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

## Phase-wise Implementation Plan

Use this project in delivery phases so each step produces a verifiable output before moving forward.

### Phase 1: Foundation and Environment Setup

Goal: Create a stable local development environment and baseline project structure.

- Set up Python environment and install dependencies from `requirements/base.txt` and `requirements/dev.txt`.
- Validate configuration loading from `config/base.yaml` and environment files (`development.yaml`, `testing.yaml`, etc.).
- Confirm basic project bootstrapping using entry points such as `main.py` and `first.py`.

Expected output:

- Development environment is reproducible.
- Team can run the project locally without configuration errors.

### Phase 2: Core Pipeline Skeleton

Goal: Implement the end-to-end control flow skeleton without full model optimization.

- Build orchestrator flow in `src/voice_assistant/core/orchestrator.py`.
- Define module interfaces for audio input, ASR, NLU, task execution, response generation, and TTS.
- Add structured logging and error handling hooks.

Expected output:

- A full request lifecycle can execute through stub or early-stage modules.
- Pipeline boundaries are clearly separated for future improvements.

### Phase 3: Audio and ASR Layer

Goal: Capture audio reliably and convert speech to text.

- Implement audio capture/preprocessing in `src/voice_assistant/audio/`.
- Integrate ASR model configuration from `config/models/asr_config.yaml`.
- Add fallback behavior for noisy/empty input and timeout scenarios.

Expected output:

- Speech input is converted into text with measurable baseline quality.
- Audio edge cases are handled gracefully.

### Phase 4: NLU and Intent Workflow

Goal: Convert ASR text into intents, entities, and actionable context.

- Implement intent and entity extraction using `config/models/nlu_config.yaml`.
- Define intent routing and validation rules in the core layer.
- Add confidence thresholds and fallback intent strategy.

Expected output:

- User utterances map to intents/entities consistently.
- Unknown or low-confidence intents follow a safe fallback path.

### Phase 5: Task Execution and Response Generation

Goal: Execute business actions and generate response text.

- Implement task handlers/services under the application service layer.
- Integrate response generation settings via `config/models/llm_config.yaml`.
- Add response templates and policy checks for robust outputs.

Expected output:

- Intent-to-action flow is functional.
- System returns relevant and safe response text for supported commands.

### Phase 6: TTS and User Output

Goal: Convert final response text into natural audio output.

- Integrate TTS using `config/models/tts_config.yaml`.
- Tune voice parameters (speed, tone, language/locale settings).
- Ensure output playback and failure recovery logic are in place.

Expected output:

- Voice response is generated and delivered consistently.
- Text-only fallback exists when TTS fails.

### Phase 7: API, Data, and Integration Hardening

Goal: Expose stable APIs and ensure service reliability.

- Finalize API surface in `src/voice_assistant/api/server.py` and align with `docs/api/openapi.yaml`.
- Validate persistence/logging paths under `data/` and `monitoring/`.
- Implement integration tests in `tests/integration/` and E2E scenarios in `tests/e2e/`.

Expected output:

- API is testable and documented.
- Cross-module interactions are validated in realistic workflows.

### Phase 8: Performance, Deployment, and Operations

Goal: Prepare production deployment with observability and scaling.

- Run performance benchmarks from `tests/performance/` and tune bottlenecks.
- Package and deploy with `docker/` and `kubernetes/` assets.
- Enable metrics, logs, and tracing from `monitoring/` for production operations.

Expected output:

- System is deployable and observable in production-like environments.
- Performance and reliability targets are measured and tracked.

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
