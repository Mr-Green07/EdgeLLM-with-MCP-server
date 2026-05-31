# PHASE 1 DEVELOPMENT: Offline Speech Recognition System
## Complete Setup & Implementation Guide

**Document Date:** May 30, 2026  
**Version:** 1.0  
**Status:** Phase 1 - Speech-to-Text Foundation  
**Technology Stack:** Python, OpenAI Whisper, FastAPI

---

## TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Folder Structure](#folder-structure)
4. [Requirements & Installation](#requirements--installation)
5. [Configuration Guide](#configuration-guide)
6. [Core Modules](#core-modules)
7. [API Endpoints](#api-endpoints)
8. [Running the Application](#running-the-application)
9. [Testing Procedures](#testing-procedures)
10. [Deployment Checklist](#deployment-checklist)
11. [Troubleshooting](#troubleshooting)
12. [Phase 2 Roadmap](#phase-2-roadmap)

---

## PROJECT OVERVIEW

**Objective:** Build a complete offline speech recognition system that operates independently without requiring internet connectivity.

**Phase 1 Focus:** 
- Implement fully functional, offline speech-to-text system
- Convert audio files to text with high accuracy
- Set up FastAPI endpoints
- Implement caching infrastructure
- Prepare foundation for Phase 2 expansion

**Success Criteria:**
- ✅ Whisper runs locally without internet
- ✅ Audio files transcribe accurately
- ✅ FastAPI endpoints respond correctly
- ✅ System works completely offline after initial setup

---

## SYSTEM ARCHITECTURE

### High-Level Architecture

```
┌─────────────┐
│  Audio File │ (mp3, wav, m4a, flac, ogg, webm)
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  FastAPI Upload Endpoint    │ (/api/v1/transcribe)
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Whisper Model (Local)       │ (base = 140MB)
│ - Device: CPU/CUDA          │
│ - Language: Auto-detect     │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Response Handler           │
│ - Format: JSON/TXT/VTT/SRT  │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Client Output / Storage    │
│ - Redis Cache (Optional)    │
│ - Database (Optional)       │
└─────────────────────────────┘
```

### Component Interactions

```
main.py (FastAPI Server)
    ├─ models.py (WhisperModelManager)
    │   └─ Whisper Model Loading & Management
    ├─ download_models.py (Model Download)
    │   └─ Automated Model Fetching
    └─ API Endpoints
        ├─ POST /api/v1/transcribe
        ├─ GET /api/v1/status
        ├─ GET /api/v1/model-info
        └─ GET /health
```

---

## FOLDER STRUCTURE

### Project Root Directory

```
g:\Student\Project in Python\ASR/
│
├── 📄 main.py                    ⭐ FastAPI application server
├── 📄 models.py                  ⭐ Whisper model manager
├── 📄 download_models.py         ⭐ Model download script
├── 📄 whiper_test.py             ⭐ Test suite
│
├── 📄 requirement.txt             📦 Python dependencies
├── 📄 .env                        ⚙️  Configuration file
├── 📄 pyproject.toml
├── 📄 setup.py
│
├── 📁 config/                     ⚙️  Configuration files
│   ├── base.yaml
│   ├── development.yaml
│   ├── production.yaml
│   ├── staging.yaml
│   ├── testing.yaml
│   └── logging/
│       └── logging.yaml
│
├── 📁 data/                       💾 Data storage
│   ├── backups/
│   ├── cache/
│   ├── database/
│   ├── logs/
│   ├── models/
│   └── temp/                      (temp uploaded files)
│
├── 📁 offline_models/             🤖 Whisper models (downloaded)
│   └── (models downloaded here after setup)
│
├── 📁 output/                     📤 Transcription outputs
│   └── (transcribed results)
│
├── 📁 src/                        💻 Source code
│   └── voice_assistant/
│       ├── api/
│       ├── asr/
│       ├── audio/
│       ├── core/
│       ├── nlu/
│       ├── response_generation/
│       ├── storage/
│       ├── tasks/
│       ├── tts/
│       ├── utils/
│       ├── wake_word/
│       └── __init__.py
│
├── 📁 tests/                      🧪 Test files
│   ├── __init__.py
│   ├── conftest.py
│   ├── coverage/
│   ├── e2e/
│   ├── fixtures/
│   ├── integration/
│   ├── performance/
│   └── unit/
│
├── 📁 docs/                       📚 Documentation
│   ├── QUICK_START.md
│   ├── API_DOCUMENTATION.md
│   ├── COMPONENT_OVERVIEW.md
│   ├── COMPLETE_GUIDE.md
│   ├── PRACTICAL_EXAMPLES.md
│   ├── architecture/
│   ├── deployment/
│   ├── development/
│   └── api/
│
├── 📁 docker/                     🐳 Docker configuration
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── Dockerfile.test
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   └── entrypoint.sh
│
├── 📁 kubernetes/                 ☸️  Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── helm/
│   └── monitoring/
│
├── 📁 ci-cd/                      🔄 CI/CD pipelines
│   ├── github-actions/
│   ├── gitlab-ci/
│   └── jenkins/
│
└── 📁 notebooks/                  📓 Jupyter notebooks
    ├── data_exploration.ipynb
    ├── model_evaluation.ipynb
    └── performance_analysis.ipynb
```

### Key Files Description

| File | Purpose | Status |
|------|---------|--------|
| `main.py` | FastAPI application server with API endpoints | ✅ Phase 1 |
| `models.py` | Whisper model management and loading | ✅ Phase 1 |
| `download_models.py` | Automated model download script | ✅ Phase 1 |
| `whiper_test.py` | Comprehensive test suite | ✅ Phase 1 |
| `requirement.txt` | Python dependencies | ✅ Phase 1 |
| `.env` | Environment configuration | ✅ Phase 1 |

---

## REQUIREMENTS & INSTALLATION

### 4. HARDWARE REQUIREMENTS

| Component | Minimum | Recommended | Optimal |
|-----------|---------|-------------|---------|
| **CPU** | Intel i5 / Ryzen 5 | Intel i7 / Ryzen 7 | Intel i9 / Ryzen 9 |
| **RAM** | 8 GB | 16 GB | 32 GB+ |
| **GPU** | None (CPU OK) | NVIDIA GTX 1660+ | NVIDIA RTX 3060+ |
| **Storage** | 10 GB Free | 20 GB Free | 50 GB+ Free |
| **Network** | Not needed | Not needed | Not needed |

### 5. SOFTWARE REQUIREMENTS

| Software | Version | Purpose | Installation |
|----------|---------|---------|--------------|
| **Python** | 3.8+ | Core Language | python.org |
| **pip** | 20.0+ | Package Manager | Included with Python |
| **FFmpeg** | Latest | Audio Processing | ffmpeg.org |
| **Git** | Latest | Version Control | git-scm.com |

### Step-by-Step Installation

#### Step 1: Install Python

```bash
# Visit https://www.python.org/downloads/
# Download Python 3.9+ for your operating system
# Run the installer and check "Add Python to PATH"

# Verify installation
python --version      # Should show: Python 3.9.x or higher
pip --version         # Should show: pip 20.0.x or higher
```

#### Step 2: Install FFmpeg

**Windows:**
```bash
# Option 1: Download from https://ffmpeg.org/download.html
# Option 2: Using Chocolatey (if installed)
choco install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Verify:**
```bash
ffmpeg -version
```

#### Step 3: Clone Repository

```bash
git clone <repository-url>
cd ASR
```

#### Step 4: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### Step 5: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirement.txt

# This will install:
# - openai-whisper (speech recognition)
# - torch (deep learning framework)
# - fastapi (web framework)
# - uvicorn (ASGI server)
# - And all other dependencies listed in requirement.txt
```

**Installation Time:** 10-15 minutes (depending on internet speed)

#### Step 6: Download Whisper Models

```bash
# Download base model (~140MB) - Recommended
python download_models.py --model base --device cpu

# Or download other sizes:
python download_models.py --model tiny    # ~39MB - fastest
python download_models.py --model small   # ~244MB
python download_models.py --model medium  # ~769MB
python download_models.py --model large   # ~1550MB - most accurate

# Download multiple models at once:
python download_models.py --models tiny base small --device cpu

# List downloaded models:
python download_models.py --list

# Verify models:
python download_models.py --verify
```

#### Step 7: Verify Installation

```bash
# Check Whisper version
whisper --version

# Check Python packages
pip list | grep -E "whisper|torch|fastapi"

# Run test suite
python whiper_test.py

# Run with specific options
python whiper_test.py --model base --device cpu --verbose
```

---

## CONFIGURATION GUIDE

### `.env` File Configuration

The `.env` file controls all application settings. Located in project root.

#### Model Configuration

```env
# Model size: tiny, base, small, medium, large
# Recommendation: 'base' for Phase 1
MODEL_SIZE=base

# Device: cpu or cuda (cuda requires NVIDIA GPU)
DEVICE=cpu

# Language: 'en' for English, 'es' for Spanish, etc.
# Leave empty for auto-detection
LANGUAGE=en

# CPU thread count (for CPU inference)
NUM_THREADS=4
```

#### API Configuration

```env
# FastAPI server host and port
API_HOST=0.0.0.0
API_PORT=8000

# API URL prefix for versioning
API_PREFIX=/api/v1

# Auto-reload server on code changes
RELOAD=true

# Enable API documentation at /docs
ENABLE_DOCS=true
```

#### Output Configuration

```env
# Output format: json, txt, vtt, srt
OUTPUT_FORMAT=json

# Directory for output files
OUTPUT_DIR=./output

# Directory for temporary uploads
TEMP_UPLOAD_DIR=./data/temp

# Maximum upload size in MB (0 = unlimited)
MAX_UPLOAD_SIZE=500

# Allowed audio formats
ALLOWED_FORMATS=mp3,wav,m4a,flac,ogg,webm
```

#### Performance Configuration

```env
# Beam size for Whisper (1-5, higher = slower but more accurate)
BEAM_SIZE=5

# Number of concurrent workers
NUM_WORKERS=2

# Request timeout in seconds
REQUEST_TIMEOUT=300
```

#### Caching Configuration (Phase 2+)

```env
# Enable Redis caching
CACHE_ENABLED=false

# Redis configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Cache expiration time in seconds
CACHE_EXPIRATION=3600
```

#### Logging Configuration

```env
# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Log file path
LOG_FILE=./data/logs/phase1.log

# Log file size (MB)
LOG_MAX_SIZE=100

# Number of backup log files
LOG_BACKUP_COUNT=5
```

#### Security Configuration

```env
# Enable CORS (Cross-Origin Resource Sharing)
ENABLE_CORS=true

# Allowed CORS origins
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

#### Feature Flags (Phase 1)

```env
# Phase 1 Features (Available)
FEATURE_TRANSCRIPTION=true

# Phase 2+ Features (Disabled)
FEATURE_SENTIMENT_ANALYSIS=false
FEATURE_NER=false
FEATURE_QUESTION_ANSWERING=false
FEATURE_CACHING=false
```

---

## CORE MODULES

### 1. `models.py` - WhisperModelManager

Handles loading, managing, and using the Whisper model.

```python
from models import WhisperModelManager, initialize_model_manager, get_model_manager

# Initialize model manager
manager = initialize_model_manager(
    model_size='base',
    device='cpu',
    language='en'
)

# Load model
model = manager.load_model()

# Get model information
info = manager.get_model_info()
print(info)
# Output: {
#   'model_size': 'base',
#   'parameters': 140000000,
#   'device': 'cpu',
#   'model_loaded': True
# }

# Get device information
device_info = manager.get_device_info()

# Perform transcription
result = model.transcribe('audio.mp3')
print(result['text'])

# Unload model to free memory
manager.unload_model()
```

**Key Features:**
- Automatic model downloading
- Device detection (CPU/CUDA)
- Model caching
- Memory management
- Error handling

### 2. `download_models.py` - ModelDownloader

Automated script for downloading and verifying Whisper models.

```bash
# Download single model
python download_models.py --model base

# Download multiple models
python download_models.py --models tiny base small

# Verify downloaded models
python download_models.py --verify

# List downloaded models
python download_models.py --list

# Use custom model directory
python download_models.py --model base --model-dir /custom/path
```

### 3. `main.py` - FastAPI Application

The main application server with REST API endpoints.

```bash
# Start server
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Visit API documentation
# http://localhost:8000/docs  (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

### 4. `whiper_test.py` - Test Suite

Comprehensive testing for the Whisper model.

```bash
# Run all tests
python whiper_test.py

# Run with specific model
python whiper_test.py --model base

# Use GPU for testing
python whiper_test.py --device cuda

# Verbose output
python whiper_test.py --verbose

# Tests include:
# ✓ Environment verification
# ✓ Model manager initialization
# ✓ Model loading
# ✓ Model information retrieval
# ✓ Device information
# ✓ Transcription accuracy
# ✓ Error handling
```

---

## API ENDPOINTS

### Base URL: `http://localhost:8000`

### 1. Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model_loaded": true,
  "model_info": {
    "model_size": "base",
    "parameters": 140000000,
    "device": "cpu",
    "model_loaded": true
  },
  "device_info": {
    "device": "cpu",
    "torch_version": "2.0.1"
  }
}
```

### 2. System Status

```http
GET /api/v1/status
```

**Response:**
```json
{
  "status": "running",
  "version": "1.0.0",
  "timestamp": "2026-05-30T12:00:00",
  "api_prefix": "/api/v1",
  "model_config": {...},
  "features": {
    "transcription": true,
    "caching": false,
    "sentiment_analysis": false,
    "ner": false,
    "question_answering": false
  }
}
```

### 3. Transcribe Audio

```http
POST /api/v1/transcribe
Content-Type: multipart/form-data

file: <audio_file>
language: en (optional)
```

**Example using cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/transcribe \
  -F "file=@sample.mp3" \
  -F "language=en"
```

**Example using Python:**
```python
import requests

with open('sample.mp3', 'rb') as f:
    files = {'file': f}
    data = {'language': 'en'}
    response = requests.post(
        'http://localhost:8000/api/v1/transcribe',
        files=files,
        data=data
    )
    print(response.json())
```

**Response:**
```json
{
  "success": true,
  "message": "Transcription completed successfully",
  "transcript": "This is a sample transcription",
  "segments": [
    {
      "start": 0.0,
      "end": 3.5,
      "text": "This is a sample"
    },
    {
      "start": 3.5,
      "end": 5.0,
      "text": "transcription"
    }
  ],
  "language": "en",
  "duration": 5.0,
  "processing_time": 2.34,
  "timestamp": "2026-05-30T12:00:00"
}
```

### 4. Model Information

```http
GET /api/v1/model-info
```

**Response:**
```json
{
  "model_size": "base",
  "approximate_size": "140M",
  "parameters": 140000000,
  "device": "cpu",
  "language": "en",
  "model_dir": "./offline_models",
  "model_loaded": true
}
```

### 5. Supported Formats

```http
GET /api/v1/supported-formats
```

**Response:**
```json
{
  "supported_formats": ["mp3", "wav", "m4a", "flac", "ogg", "webm"],
  "max_file_size_mb": 500,
  "max_file_size_description": "500MB"
}
```

### 6. Supported Languages

```http
GET /api/v1/languages
```

**Response:**
```json
{
  "auto_detect": true,
  "default_language": "en",
  "note": "Whisper supports 99+ languages"
}
```

---

## RUNNING THE APPLICATION

### 1. Quick Start

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Start the server
python main.py

# Output:
# ============================================================
# PHASE 1: Offline Speech Recognition System - Starting
# ============================================================
# ✓ Whisper model loaded successfully
# ✓ Device: cpu
# ✓ Model Size: base
# ✓ API Server running on 0.0.0.0:8000/api/v1
```

### 2. Access API Documentation

```
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```

### 3. Test Transcription

```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/transcribe \
  -F "file=@test_audio.mp3"

# Using Python
python -c "
import requests
with open('test_audio.mp3', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/transcribe',
        files={'file': f}
    )
    print(response.json())
"
```

### 4. Check System Health

```bash
curl http://localhost:8000/health
```

---

## TESTING PROCEDURES

### Test 1: Verify Whisper Installation

```bash
whisper --version
# Expected Output: Whisper version x.x.x
```

### Test 2: Download Models

```bash
python download_models.py --model base
# Expected: Model downloads (~140MB)
# Status: ✓ PASS if successful
```

### Test 3: Run Python Script

```bash
python -c "
import whisper
model = whisper.load_model('base')
print('Model loaded successfully')
"
# Expected: Model loaded successfully
```

### Test 4: Start FastAPI Server

```bash
python main.py
# Expected: Server starts on http://localhost:8000
# Visit: http://localhost:8000/docs
# Status: ✓ PASS if Swagger UI loads
```

### Test 5: API Endpoint Testing

```bash
# In a new terminal:
curl -X POST http://localhost:8000/api/v1/transcribe \
  -F "file=@sample.mp3"

# Expected Response: JSON with transcription
# Status: ✓ PASS if transcription returned
```

### Test 6: Run Test Suite

```bash
python whiper_test.py --verbose

# Expected:
# ✓ PASS: Test 1: Environment Verification
# ✓ PASS: Test 2: Model Manager Initialization
# ✓ PASS: Test 3: Model Loading
# ✓ PASS: Test 4: Model Information
# ✓ PASS: Test 5: Device Information
# ✓ PASS: Test 6: Model Transcription
# ✓ PASS: Test 7: Error Handling
# SUMMARY: 7 passed, 0 failed
```

---

## DEPLOYMENT CHECKLIST

### ✅ Installation & Setup

- [ ] Python 3.8+ installed and verified
- [ ] FFmpeg installed and verified
- [ ] Virtual environment created and activated
- [ ] `requirement.txt` created with all dependencies
- [ ] All dependencies installed successfully (`pip install -r requirement.txt`)
- [ ] Whisper model downloaded locally (`python download_models.py --model base`)

### ✅ Configuration

- [ ] `.env` file created and configured properly
- [ ] `MODEL_SIZE=base` configured
- [ ] `DEVICE=cpu` or `cuda` configured correctly
- [ ] `API_HOST` and `API_PORT` configured
- [ ] `OUTPUT_DIR` and `TEMP_UPLOAD_DIR` created
- [ ] Log directory created: `./data/logs/`

### ✅ Code & Modules

- [ ] `models.py` - Model manager implemented
- [ ] `download_models.py` - Download script implemented
- [ ] `main.py` - FastAPI application implemented
- [ ] `whiper_test.py` - Test suite implemented
- [ ] All Python files have proper error handling
- [ ] All Python files have comprehensive logging

### ✅ Testing

- [ ] Whisper installation verified
- [ ] Model download successful
- [ ] Python import test passed
- [ ] FastAPI server starts without errors
- [ ] API documentation accessible at `/docs`
- [ ] Transcription test completed successfully
- [ ] Different audio formats tested (mp3, wav, m4a)
- [ ] Error handling verified
- [ ] Performance benchmarking done

### ✅ Verification

- [ ] Offline functionality confirmed
- [ ] Model loads without internet
- [ ] Transcription works accurately
- [ ] API responses are correct
- [ ] No memory leaks in model usage

### ✅ Documentation & Version Control

- [ ] Documentation updated
- [ ] Code committed to version control
- [ ] `.env` example file created (`.env.example`)
- [ ] README.md updated
- [ ] Contributing guidelines updated
- [ ] Changelog updated

### ✅ Deployment

- [ ] Docker image built (if using Docker)
- [ ] Kubernetes manifests tested (if using K8s)
- [ ] Environment variables set correctly
- [ ] Database initialized (if applicable)
- [ ] Cache configured (optional for Phase 1)

### ✅ Phase 1 Completion

- [ ] All checklist items completed
- [ ] Phase 1 approved and signed off
- [ ] Ready for Phase 2 development

---

## TROUBLESHOOTING

### Issue: "ModuleNotFoundError: No module named 'whisper'"

**Solution:**
```bash
pip install openai-whisper

# Or reinstall from requirements
pip install -r requirement.txt
```

### Issue: "CUDA out of memory" (if using GPU)

**Solution:**
```bash
# Use CPU instead
export DEVICE=cpu
# Or in .env:
DEVICE=cpu
```

### Issue: "Model download fails"

**Solution:**
```bash
# Check internet connection
ping github.com

# Try downloading with verbose output
python download_models.py --model base --verbose

# Or download manually and place in offline_models/
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Use a different port
python main.py  # Change API_PORT in .env
# Or kill the process using port 8000
```

### Issue: "FFmpeg not found"

**Solution:**
```bash
# Windows: Download from https://ffmpeg.org/download.html
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
```

### Issue: "Transcription is slow"

**Solution:**
```bash
# Use smaller model
MODEL_SIZE=tiny   # in .env

# Or enable GPU
DEVICE=cuda       # in .env (requires NVIDIA GPU)

# Reduce audio quality if possible
```

---

## PHASE 2 ROADMAP

### Phase 2: NLP Enhancement (Planned)

**New Features:**
- Sentiment Analysis
- Named Entity Recognition (NER)
- Question Answering capabilities
- Redis caching layer
- Database integration

**Expected Timeline:** After Phase 1 completion + 2-3 weeks

**Dependencies to Add:**
```
transformers>=4.30.0
torch-nlp>=0.5.0
redis-py>=5.0.0
```

### Phase 3: Advanced Features (Planned)

- Voice Activity Detection
- Speaker Identification
- Multi-language real-time processing
- WebSocket streaming
- Advanced caching strategies
- Performance optimization

---

## SUCCESS METRICS

### Phase 1 Success Criteria (All Must Pass)

✅ **Transcription Accuracy:** >95% for clear audio  
✅ **Processing Speed:** <5 seconds for 1-minute audio (base model on CPU)  
✅ **System Uptime:** 99%+ during testing  
✅ **Memory Usage:** <2GB for base model on CPU  
✅ **API Response Time:** <50ms for non-transcription endpoints  
✅ **Error Handling:** All errors properly logged and reported  
✅ **Offline Capability:** Fully functional without internet after setup  

---

## DOCUMENT HISTORY

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | May 30, 2026 | Initial Phase 1 Documentation | ASR Dev Team |

---

## CONTACT & SUPPORT

For issues or questions:
- Create GitHub issue
- Check documentation: `/docs` folder
- Review logs: `./data/logs/phase1.log`

---

**End of Phase 1 Setup Guide**
