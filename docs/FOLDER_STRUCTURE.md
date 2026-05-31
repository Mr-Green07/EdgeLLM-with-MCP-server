# PHASE 1 DETAILED FOLDER STRUCTURE
## Complete Directory Layout & File Descriptions

**Document Date:** May 30, 2026  
**Version:** 1.0

---

## Root Directory Structure

```
g:\Student\Project in Python\ASR/
│
├─ 📄 CORE APPLICATION FILES
│  ├── main.py                    ⭐ FastAPI application (API server)
│  ├── models.py                  ⭐ Whisper model manager
│  ├── download_models.py         ⭐ Model downloader script
│  └── whiper_test.py             ⭐ Test suite for model
│
├─ 📄 CONFIGURATION & SETUP
│  ├── requirement.txt             📦 Python dependencies
│  ├── .env                        ⚙️  Environment variables
│  ├── .env.example                📋 Example env file
│  ├── pyproject.toml
│  ├── setup.py
│  ├── setup.cfg
│  ├── Makefile
│  ├── VERSION
│  └── MANIFEST.in
│
├─ 📁 config/                      ⚙️  YAML CONFIGURATION
│  ├── base.yaml
│  ├── development.yaml
│  ├── production.yaml
│  ├── staging.yaml
│  ├── testing.yaml
│  └── logging/
│      └── logging.yaml
│
├─ 📁 data/                        💾 DATA & STORAGE
│  ├── backups/                    (Backup files)
│  ├── cache/                      (Cache data)
│  ├── database/                   (SQLite database)
│  ├── logs/                       (Application logs)
│  ├── models/                     (Model metadata)
│  └── temp/                       (Temporary uploads)
│
├─ 📁 offline_models/              🤖 WHISPER MODELS (AUTO-DOWNLOADED)
│  └── (Models downloaded here after first run)
│
├─ 📁 output/                      📤 TRANSCRIPTION OUTPUT
│  └── (Transcription results stored here)
│
├─ 📁 src/                         💻 SOURCE CODE
│  └── voice_assistant/
│      ├── __init__.py
│      ├── api/                    (API modules)
│      ├── asr/                    (ASR modules - Phase 2+)
│      ├── audio/                  (Audio processing)
│      ├── core/                   (Core functionality)
│      ├── nlu/                    (NLU modules - Phase 2+)
│      ├── response_generation/    (Response generation - Phase 2+)
│      ├── storage/                (Storage modules)
│      ├── tasks/                  (Task modules)
│      ├── tts/                    (Text-to-speech - Phase 2+)
│      ├── utils/                  (Utility functions)
│      └── wake_word/              (Wake word detection - Phase 2+)
│
├─ 📁 tests/                       🧪 TEST FILES
│  ├── __init__.py
│  ├── conftest.py                 (pytest configuration)
│  ├── coverage/                   (Coverage reports)
│  ├── e2e/                        (End-to-end tests)
│  ├── fixtures/                   (Test fixtures)
│  ├── integration/                (Integration tests)
│  ├── performance/                (Performance tests)
│  └── unit/                       (Unit tests)
│
├─ 📁 docs/                        📚 DOCUMENTATION
│  ├── PHASE1_SETUP.md             ⭐ Complete Phase 1 setup guide
│  ├── QUICK_START.md              ⭐ Quick start guide
│  ├── API_DOCUMENTATION.md        ⭐ API endpoints reference
│  ├── FOLDER_STRUCTURE.md         ⭐ This file
│  ├── COMPONENT_OVERVIEW.md
│  ├── COMPLETE_GUIDE.md
│  ├── PRACTICAL_EXAMPLES.md
│  ├── getting_started.md
│  ├── index.md
│  ├── conf.py                     (Sphinx config)
│  ├── requirements.txt
│  ├── _templates/                 (Doc templates)
│  ├── api/
│  │  ├── openapi.yaml
│  │  └── rest_api.md
│  ├── architecture/
│  │  ├── components.md
│  │  ├── data_flow.md
│  │  ├── overview.md
│  │  └── state_machine.md
│  ├── deployment/
│  │  ├── configuration.md
│  │  ├── docker.md
│  │  ├── installation.md
│  │  └── kubernetes.md
│  ├── development/
│  │  ├── coding_standards.md
│  │  ├── contributing.md
│  │  ├── setup.md
│  │  └── testing.md
│  ├── performance/
│  │  ├── benchmarks.md
│  │  ├── optimization.md
│  │  └── resource_usage.md
│  └── user_guide/
│      ├── commands.md
│      ├── customization.md
│      └── troubleshooting.md
│
├─ 📁 docker/                      🐳 DOCKER CONFIGURATION
│  ├── Dockerfile                  (Production image)
│  ├── Dockerfile.dev              (Development image)
│  ├── Dockerfile.test             (Testing image)
│  ├── docker-compose.yml          (Dev compose)
│  ├── docker-compose.prod.yml     (Prod compose)
│  └── entrypoint.sh               (Container entry point)
│
├─ 📁 kubernetes/                  ☸️  KUBERNETES MANIFESTS
│  ├── namespace.yaml
│  ├── deployment.yaml
│  ├── service.yaml
│  ├── ingress.yaml
│  ├── configmap.yaml
│  ├── secret.yaml
│  ├── hpa.yaml                    (Horizontal Pod Autoscaler)
│  ├── networkpolicy.yaml
│  ├── pdb.yaml                    (Pod Disruption Budget)
│  ├── helm/
│  │  ├── Chart.yaml
│  │  ├── values.yaml
│  │  ├── values-dev.yaml
│  │  ├── values-prod.yaml
│  │  └── templates/
│  └── monitoring/
│      └── (Monitoring configurations)
│
├─ 📁 ci-cd/                       🔄 CI/CD PIPELINES
│  ├── github-actions/
│  │  ├── ci-cd.yml                (Main CI/CD pipeline)
│  │  ├── code-quality.yml
│  │  ├── test-coverage.yml
│  │  ├── security-scan.yml
│  │  └── release.yml
│  ├── gitlab-ci/
│  │  └── .gitlab-ci.yml
│  └── jenkins/
│      ├── Jenkinsfile
│      └── pipeline-config.groovy
│
├─ 📁 monitoring/                  📊 MONITORING SETUP
│  ├── grafana/                    (Grafana configuration)
│  │  └── (Dashboard configs)
│  ├── logging/                    (Logging setup)
│  ├── prometheus/                 (Prometheus config)
│  └── tracing/                    (Tracing setup)
│
├─ 📁 notebooks/                   📓 JUPYTER NOTEBOOKS
│  ├── data_exploration.ipynb
│  ├── model_evaluation.ipynb
│  └── performance_analysis.ipynb
│
├─ 📁 requirements/                📦 REQUIREMENT FILES
│  ├── base.txt
│  ├── dev.txt
│  ├── docs.txt
│  ├── prod.txt
│  └── test.txt
│
├─ 📁 scripts/                     🔧 UTILITY SCRIPTS
│  ├── __init__.py
│  ├── deployment/
│  ├── maintenance/
│  ├── setup/
│  ├── testing/
│  └── utils/
│
├─ 📄 PROJECT DOCUMENTATION
│  ├── README.md                   (Project readme)
│  ├── CHANGELOG.md                (Version history)
│  ├── LICENSE                     (License file)
│  ├── CODE_OF_CONDUCT.md
│  ├── CONTRIBUTING.md
│  ├── Page AI.md
│  ├── project_analysis.md
│  └── install.cmd                 (Windows installer)
```

---

## File Descriptions

### 🟡 CORE APPLICATION FILES (Phase 1)

#### `main.py` (4KB)
- **Purpose:** FastAPI web server application
- **Key Functions:**
  - Initializes FastAPI app
  - Manages model lifecycle (startup/shutdown)
  - Defines API endpoints
  - Handles file uploads and transcription
- **Dependencies:** FastAPI, Uvicorn, Models.py
- **Run:** `python main.py`

#### `models.py` (8KB)
- **Purpose:** Manages Whisper model loading and transcription
- **Key Classes:**
  - `WhisperModelManager`: Main model management class
- **Key Methods:**
  - `load_model()`: Load Whisper model
  - `get_model_info()`: Get model information
  - `get_device_info()`: Get device information
- **Dependencies:** Whisper, Torch
- **Used By:** main.py

#### `download_models.py` (6KB)
- **Purpose:** Download Whisper models for offline use
- **Key Classes:**
  - `ModelDownloader`: Handles model downloads
- **Key Methods:**
  - `download_model()`: Download single model
  - `download_multiple_models()`: Download multiple models
  - `verify_model()`: Verify model integrity
- **Run:** `python download_models.py --model base`

#### `whiper_test.py` (10KB)
- **Purpose:** Comprehensive test suite
- **Key Classes:**
  - `WhisperTester`: Test runner
  - `TestResults`: Result aggregator
- **Tests:**
  - Environment verification
  - Model loading
  - Transcription accuracy
  - Error handling
- **Run:** `python whiper_test.py`

---

### ⚙️ CONFIGURATION FILES

#### `.env` (2KB)
- **Purpose:** Environment variables configuration
- **Key Variables:**
  - `MODEL_SIZE`: Whisper model size
  - `DEVICE`: cpu or cuda
  - `API_PORT`: FastAPI port
  - `OUTPUT_DIR`: Output directory
  - Feature flags for Phase 2+

#### `requirement.txt` (2KB)
- **Purpose:** Python package dependencies
- **Key Packages:**
  - openai-whisper
  - torch, torchaudio
  - fastapi, uvicorn
  - pydantic, python-dotenv
- **Install:** `pip install -r requirement.txt`

#### `pyproject.toml`
- **Purpose:** Project metadata and build configuration
- **Defines:** Package name, version, dependencies

#### `setup.py`
- **Purpose:** Installation script
- **Use:** `pip install -e .` for development install

---

### 📁 DATA DIRECTORY (`data/`)

#### `data/logs/`
- **Purpose:** Application logs
- **Files:**
  - `phase1.log`: Phase 1 application logs
  - Rotated logs (phase1.log.1, phase1.log.2, etc.)

#### `data/temp/`
- **Purpose:** Temporary uploaded files
- **Auto-cleaned:** Files deleted after processing

#### `data/models/`
- **Purpose:** Model metadata storage
- **Contents:** Model information and caching

#### `data/database/`
- **Purpose:** SQLite database storage
- **Files:** `asr.db` (when database is enabled)

---

### 🤖 OFFLINE MODELS DIRECTORY (`offline_models/`)

- **Purpose:** Store downloaded Whisper models
- **Created On:** First run of `download_models.py`
- **Files:** Binary model files (.pt extension)
- **Size:** Varies by model (39MB-1550MB)

**Models available:**
- `tiny.pt` (39MB) - Fastest, lowest accuracy
- `base.pt` (140MB) - Recommended for Phase 1
- `small.pt` (244MB) - Better accuracy
- `medium.pt` (769MB) - High accuracy
- `large.pt` (1550MB) - Highest accuracy, slowest

---

### 📤 OUTPUT DIRECTORY (`output/`)

- **Purpose:** Store transcription results
- **File Format:** JSON (by default)
- **Naming:** `transcript_<timestamp>.json`
- **Structure:**
  ```json
  {
    "original_filename": "sample.mp3",
    "transcript": "Transcribed text...",
    "language": "en",
    "segments": [...],
    "timestamp": "2026-05-30T12:00:00"
  }
  ```

---

### 💻 SOURCE CODE DIRECTORY (`src/`)

#### `src/voice_assistant/`
- **Purpose:** Main application source code
- **Subdirectories:**
  - `api/`: API endpoint implementations
  - `asr/`: Audio processing (Phase 2+)
  - `audio/`: Audio utilities
  - `core/`: Core business logic
  - `utils/`: Helper functions
  - `storage/`: Data persistence

---

### 🧪 TESTS DIRECTORY (`tests/`)

#### Structure:
```
tests/
├── unit/              (Unit tests)
├── integration/       (Integration tests)
├── e2e/               (End-to-end tests)
├── performance/       (Performance tests)
├── fixtures/          (Test data)
├── coverage/          (Coverage reports)
└── conftest.py        (pytest configuration)
```

#### Running Tests:
```bash
pytest                           # Run all tests
pytest tests/unit/              # Run unit tests only
pytest --cov                    # With coverage report
pytest -v                       # Verbose output
```

---

### 📚 DOCUMENTATION DIRECTORY (`docs/`)

#### Phase 1 Documentation (Key Files):
- **PHASE1_SETUP.md**: Complete Phase 1 setup guide
- **QUICK_START.md**: 5-10 minute quick start
- **API_DOCUMENTATION.md**: API reference
- **FOLDER_STRUCTURE.md**: This file

#### Subdirectories:
- `api/`: API specifications
- `architecture/`: System architecture docs
- `deployment/`: Deployment guides
- `development/`: Developer guides
- `performance/`: Performance optimization
- `user_guide/`: User documentation

---

### 🐳 DOCKER DIRECTORY (`docker/`)

#### `Dockerfile` (Production)
- Multi-stage build
- Optimized for deployment
- ~500MB image size

#### `Dockerfile.dev` (Development)
- Includes dev tools
- Hot-reload enabled
- Larger image size

#### `Dockerfile.test` (Testing)
- Test framework included
- Coverage tools
- Test runner configured

#### `docker-compose.yml`
- Development environment
- Services: app, redis (optional), db (optional)

#### `docker-compose.prod.yml`
- Production environment
- Security configured
- Monitoring included

---

### ☸️ KUBERNETES DIRECTORY (`kubernetes/`)

#### Manifests:
- `deployment.yaml`: Application deployment
- `service.yaml`: Kubernetes service
- `configmap.yaml`: Configuration
- `secret.yaml`: Secrets (API keys, etc.)
- `ingress.yaml`: Ingress controller
- `hpa.yaml`: Horizontal pod autoscaling

#### Helm:
- `Chart.yaml`: Helm chart metadata
- `values.yaml`: Default values
- `values-dev.yaml`: Development values
- `values-prod.yaml`: Production values
- `templates/`: Helm templates

---

### 🔄 CI/CD DIRECTORY (`ci-cd/`)

#### GitHub Actions (`github-actions/`):
- `ci-cd.yml`: Main pipeline
- `code-quality.yml`: Code quality checks
- `test-coverage.yml`: Test coverage
- `security-scan.yml`: Security scanning
- `release.yml`: Release pipeline

#### GitLab CI (`.gitlab-ci.yml`)
#### Jenkins (`Jenkinsfile`)

---

### 📊 MONITORING DIRECTORY (`monitoring/`)

- **Grafana**: Dashboard configurations
- **Prometheus**: Metrics collection
- **Logging**: Log aggregation setup
- **Tracing**: Distributed tracing configuration

---

## Directory Creation Instructions

### Create Required Directories

```bash
# Windows
mkdir offline_models
mkdir data\logs
mkdir data\temp
mkdir data\models
mkdir data\database
mkdir output

# macOS/Linux
mkdir -p offline_models
mkdir -p data/logs
mkdir -p data/temp
mkdir -p data/models
mkdir -p data/database
mkdir -p output
```

### Verify Structure

```bash
# List all directories
tree /F  # Windows
tree -L 2  # macOS/Linux
```

---

## File Statistics (Phase 1)

| Directory | Files | Purpose |
|-----------|-------|---------|
| Root | 4 | Core Python files |
| config/ | 6 | Configuration |
| data/ | - | Data storage |
| docs/ | 8+ | Documentation |
| tests/ | - | Test suite |
| src/ | - | Source code |
| docker/ | 5 | Containerization |

---

## Phase 1 to Phase 2 Migration

When moving to Phase 2, the following directories will expand:

```
src/voice_assistant/
├── nlu/              👈 Phase 2 NLP components
├── asr/              👈 Phase 2 ASR enhancement
├── response_generation/  👈 Phase 2 Response generation
├── tts/              👈 Phase 2 Text-to-speech
└── wake_word/        👈 Phase 2 Wake word detection
```

---

## Best Practices

1. **Keep logs rotating:** Old logs automatically deleted
2. **Clean temp files:** Run cleanup script periodically
3. **Backup database:** Regular database backups
4. **Monitor storage:** Check `offline_models/` size
5. **Version outputs:** Include timestamp in results

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | May 30, 2026 | Initial Phase 1 folder structure |

---

**End of Folder Structure Documentation**
