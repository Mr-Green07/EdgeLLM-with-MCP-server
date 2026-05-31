# PHASE 1 DETAILED INSTALLATION & SETUP GUIDE
## Complete Step-by-Step Instructions

**Document Date:** May 30, 2026  
**Version:** 1.0  
**Status:** Phase 1 - Speech-to-Text Foundation

---

## TABLE OF CONTENTS

1. [Pre-Installation Checklist](#pre-installation-checklist)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [Model Download](#model-download)
6. [Verification](#verification)
7. [First Run](#first-run)
8. [Post-Installation](#post-installation)

---

## PRE-INSTALLATION CHECKLIST

Before you start, verify:

- [ ] Administrator access (Windows) or sudo privileges (Linux/Mac)
- [ ] 10GB free disk space minimum
- [ ] 8GB RAM minimum
- [ ] Stable internet connection (for downloads)
- [ ] Git installed (optional, for cloning)
- [ ] Text editor or IDE available

---

## SYSTEM REQUIREMENTS

### Operating Systems

✅ **Windows 10/11 64-bit**  
✅ **macOS 10.15+**  
✅ **Ubuntu 18.04+ / Debian / CentOS**

### Hardware Requirements

| Component | Minimum | Recommended | Optimal |
|-----------|---------|-------------|---------|
| CPU | 2 cores | 4 cores | 8+ cores |
| RAM | 8 GB | 16 GB | 32 GB+ |
| GPU | None | NVIDIA GTX 1660+ | RTX 3060+ |
| Storage | 20 GB | 50 GB | 100 GB+ |

### Software Requirements

| Software | Version | Status |
|----------|---------|--------|
| Python | 3.8+ | **Required** |
| pip | 20.0+ | **Required** |
| FFmpeg | Latest | **Required** |
| Git | Latest | Optional |
| CUDA | 11.8+ | Optional (for GPU) |
| cuDNN | 8.x | Optional (for GPU) |

---

## INSTALLATION STEPS

### STEP 1: Install Python (5-10 minutes)

#### Windows:
1. Visit https://www.python.org/downloads/
2. Download Python 3.11 (or latest 3.x)
3. Run installer
4. ✅ **Check:** "Add Python to PATH"
5. Click "Install Now"

#### macOS:
```bash
# Using Homebrew
brew install python3.11

# Or download from python.org
```

#### Linux:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3-pip

# CentOS/RedHat
sudo yum install python3.11 python3-pip
```

#### Verify:
```bash
python --version      # Should show: Python 3.11.x
python -m pip --version  # Should show: pip 23.x
```

---

### STEP 2: Install FFmpeg (5-10 minutes)

#### Windows:
```bash
# Option 1: Chocolatey
choco install ffmpeg

# Option 2: Manual
# Download from https://ffmpeg.org/download.html
# Add to PATH
```

#### macOS:
```bash
brew install ffmpeg
```

#### Linux (Ubuntu):
```bash
sudo apt-get install ffmpeg
```

#### Verify:
```bash
ffmpeg -version
# Output: ffmpeg version 5.x or higher
```

---

### STEP 3: Clone/Navigate to Project (2 minutes)

```bash
# Clone if using Git
git clone https://github.com/Mr-Green07/ASR.git
cd ASR

# Or navigate to existing directory
cd "g:\Student\Project in Python\ASR"
```

---

### STEP 4: Create Virtual Environment (3 minutes)

A virtual environment isolates project dependencies.

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verify activation:** You should see `(venv)` in your terminal prompt.

---

### STEP 5: Upgrade pip & Install Dependencies (10-15 minutes)

```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirement.txt

# Wait for installation to complete...
# This installs:
# - openai-whisper
# - torch & torchaudio
# - fastapi & uvicorn
# - And all other dependencies
```

**Expected output:** "Successfully installed [packages]"

---

### STEP 6: Create Required Directories

```bash
# Create directories for data storage
mkdir offline_models
mkdir output

# Create subdirectories
mkdir data\logs      # Windows
mkdir data\temp
mkdir data\database

# For macOS/Linux:
mkdir -p data/{logs,temp,database,models,cache,backups}
```

---

### STEP 7: Set Up Environment Configuration (5 minutes)

```bash
# Create .env file from .env.example (if exists)
# Or create new .env with:

cat > .env << 'EOF'
# Model Configuration
MODEL_SIZE=base
DEVICE=cpu
LANGUAGE=en
NUM_THREADS=4

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_PREFIX=/api/v1
RELOAD=true
ENABLE_DOCS=true

# Output Configuration
OUTPUT_FORMAT=json
OUTPUT_DIR=./output
TEMP_UPLOAD_DIR=./data/temp
MAX_UPLOAD_SIZE=500
ALLOWED_FORMATS=mp3,wav,m4a,flac,ogg,webm

# Logging
LOG_LEVEL=INFO
LOG_FILE=./data/logs/phase1.log
LOG_MAX_SIZE=100
LOG_BACKUP_COUNT=5

# Performance
BEAM_SIZE=5
NUM_WORKERS=2
REQUEST_TIMEOUT=300

# Caching (Phase 1 - disabled)
CACHE_ENABLED=false
REDIS_HOST=localhost
REDIS_PORT=6379

# Database (Phase 1 - optional)
DATABASE_URL=sqlite:///./data/database/asr.db
DATABASE_LOG=false

# Features
FEATURE_TRANSCRIPTION=true
FEATURE_SENTIMENT_ANALYSIS=false
FEATURE_NER=false
FEATURE_QUESTION_ANSWERING=false
FEATURE_CACHING=false

# Security
ENABLE_CORS=true
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Debug
DEBUG=true
VERBOSE=false
DEBUG_STORAGE=false
EOF
```

---

## MODEL DOWNLOAD

### Download Whisper Model (15-30 minutes)

```bash
# Ensure virtual environment is activated
# (venv) should be visible in terminal

# Download base model (recommended for Phase 1)
python download_models.py --model base

# Expected output:
# Starting download of 'base' model...
# This may take a few minutes...
# ✓ Successfully downloaded 'base' model!
# ✓ Model saved to: ./offline_models
```

### Verify Model Download

```bash
# List downloaded models
python download_models.py --list

# Expected output:
# Downloaded models in ./offline_models:
#   - base.pt (140.5 MB)

# Verify model integrity
python download_models.py --verify

# Expected output:
# Verifying 'base' model...
# ✓ 'base' model verified successfully!
```

### Optional: Download Multiple Models

```bash
# Download multiple models at once
python download_models.py --models tiny base small --device cpu

# Download large model for better accuracy (requires 1550MB)
python download_models.py --model large --device cpu
```

---

## CONFIGURATION

### Edit .env File

Open `.env` in your text editor and review:

```env
# Most important settings:
MODEL_SIZE=base          # Keep for Phase 1
DEVICE=cpu               # Change to 'cuda' if you have NVIDIA GPU
API_PORT=8000            # Change if port is in use
```

### Create .env.example

```bash
# Copy .env to .env.example for repository
cp .env .env.example
```

---

## VERIFICATION

### Test 1: Python Environment

```bash
python --version
# Expected: Python 3.11.x

python -c "import whisper; print('Whisper available')"
# Expected: Whisper available
```

### Test 2: Dependencies

```bash
# List installed packages
pip list | grep -E "whisper|torch|fastapi"

# Or Python:
python -c "import torch, whisper, fastapi; print('All dependencies OK')"
# Expected: All dependencies OK
```

### Test 3: Model Loading

```bash
python -c "
import whisper
model = whisper.load_model('base')
print('Model loaded successfully!')
"
# Expected: Model loaded successfully!
```

### Test 4: Run Test Suite

```bash
python whiper_test.py

# Expected output:
# ============================================================
# PHASE 1 WHISPER MODEL TEST SUITE
# ============================================================
# ✓ PASS: Test 1: Environment Verification
# ✓ PASS: Test 2: Model Manager Initialization
# ✓ PASS: Test 3: Model Loading
# ✓ PASS: Test 4: Model Information
# ✓ PASS: Test 5: Device Information
# [✓ PASS: Test 6: Model Transcription (if audio available)]
# ✓ PASS: Test 7: Error Handling
# SUMMARY: 7 passed, 0 failed out of 7 tests
```

---

## FIRST RUN

### Start the API Server

```bash
# Activate virtual environment (if not already)
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Start server
python main.py

# Expected output:
# ============================================================
# PHASE 1: Offline Speech Recognition System - Starting
# ============================================================
# ✓ Whisper model loaded successfully
# ✓ Device: cpu
# ✓ Model Size: base
# ✓ API Server running on 0.0.0.0:8000/api/v1
# [INFO] Uvicorn running on http://0.0.0.0:8000
```

### Server Ready!

The server is now running. In your browser, visit:

```
Swagger UI (Interactive API docs):
http://localhost:8000/docs

ReDoc (Alternative documentation):
http://localhost:8000/redoc

Health check:
http://localhost:8000/health
```

---

## POST-INSTALLATION

### Test Transcription

**Option 1: Using cURL**

```bash
# Open new terminal (keep server running in first terminal)
curl -X POST http://localhost:8000/api/v1/transcribe \
  -F "file=@your_audio.mp3"
```

**Option 2: Using Python**

```python
import requests

with open('your_audio.mp3', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/transcribe',
        files={'file': f}
    )
    print(response.json()['transcript'])
```

**Option 3: Using Browser (Swagger UI)**

1. Visit http://localhost:8000/docs
2. Click "Try it out" on /api/v1/transcribe
3. Click "Choose File" and select audio
4. Click "Execute"
5. See result below

### Verify Offline Capability

To confirm the system works completely offline:

1. Disconnect internet
2. Restart server: `python main.py`
3. Transcribe audio via API
4. ✅ Should work perfectly without internet!

### Create Log Rotation Script

```bash
# Optional: Create log cleanup script
cat > cleanup_logs.py << 'EOF'
import os
from pathlib import Path

log_dir = Path('./data/logs')
for log_file in log_dir.glob('*.log.*'):
    os.remove(log_file)
    print(f"Deleted: {log_file}")
EOF

python cleanup_logs.py
```

### Set Up Startup Scripts

**Windows (`startup.bat`):**
```batch
@echo off
cd %~dp0
call venv\Scripts\activate
python main.py
```

**macOS/Linux (`startup.sh`):**
```bash
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python main.py
```

---

## TROUBLESHOOTING INSTALLATION

### Issue: "Python not found"

```bash
# Windows: Add to PATH
# Edit Environment Variables > PATH > Add python directory

# Linux/Mac: Use python3
python3 --version
alias python=python3
```

### Issue: "pip install fails"

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try installing with no binary cache
pip install --no-cache-dir -r requirement.txt
```

### Issue: "FFmpeg not found"

```bash
# Windows: Add to PATH after installation
# Linux: sudo apt-get install ffmpeg
# Mac: brew install ffmpeg
```

### Issue: "Port 8000 in use"

```bash
# Change port in .env
API_PORT=8001

# Restart server
python main.py
```

### Issue: "Model download fails"

```bash
# Check internet connection
ping github.com

# Try smaller model first
python download_models.py --model tiny

# Manually specify directory
python download_models.py --model base --model-dir /custom/path
```

---

## INSTALLATION CHECKLIST

Mark these as you complete:

- [ ] Python 3.8+ installed and verified
- [ ] FFmpeg installed and verified
- [ ] Project directory created/cloned
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] pip upgraded
- [ ] Dependencies installed from requirement.txt
- [ ] Directories created (offline_models, data, output)
- [ ] .env file created and configured
- [ ] Whisper model downloaded
- [ ] All tests pass (python whiper_test.py)
- [ ] Server starts without errors
- [ ] API accessible at http://localhost:8000/docs
- [ ] Transcription test successful
- [ ] Offline functionality verified

---

## NEXT STEPS

After successful installation:

1. ✅ Read [QUICK_START.md](QUICK_START.md) for 5-minute overview
2. ✅ Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for endpoints
3. ✅ Check [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md) for file organization
4. ✅ Explore API documentation at http://localhost:8000/docs
5. ✅ Test with different audio files
6. ✅ Configure settings in .env as needed
7. ✅ Set up monitoring and logging
8. ✅ Plan Phase 2 features

---

## GETTING HELP

If you encounter issues:

1. Check [PHASE1_SETUP.md](PHASE1_SETUP.md) for detailed information
2. Review logs: `./data/logs/phase1.log`
3. Run test suite: `python whiper_test.py --verbose`
4. Check GitHub issues
5. Review documentation in `/docs` folder

---

## DOCUMENT HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | May 30, 2026 | Initial installation guide |

---

**Installation Complete! Welcome to Phase 1 of the Offline Speech Recognition System. 🎉**
