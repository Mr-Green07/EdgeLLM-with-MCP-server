# PHASE 1 QUICK START GUIDE
**Offline Speech Recognition System - Get Started in 10 Minutes**

---

## Prerequisites

- Python 3.8+ installed
- 10GB free disk space
- Internet connection (for initial setup only)

---

## 5-Minute Quick Start

### 1. Set Up Environment (2 minutes)

```bash
# Clone/navigate to project
cd "g:\Student\Project in Python\ASR"

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux
```

### 2. Install Dependencies (3 minutes)

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirement.txt
```

### 3. Download Model (30 seconds)

```bash
# Download Whisper base model (~140MB)
python download_models.py --model base
```

### 4. Start Server (30 seconds)

```bash
# Start FastAPI server
python main.py

# Output:
# ✓ Whisper model loaded successfully
# ✓ API Server running on 0.0.0.0:8000/api/v1
```

### 5. Test API (1 minute)

```bash
# Open new terminal in same project directory
# Activate venv in new terminal first

# Test with curl
curl -X POST http://localhost:8000/api/v1/transcribe \
  -F "file=@test_audio.mp3"

# Or open in browser
# http://localhost:8000/docs
```

---

## Common Commands

### Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Run Tests

```bash
python whiper_test.py
```

### Download Different Model Sizes

```bash
python download_models.py --model tiny     # Fast (39MB)
python download_models.py --model base     # Balanced (140MB) - Recommended
python download_models.py --model large    # Accurate (1550MB)
```

### View API Docs

```
Swagger UI:   http://localhost:8000/docs
ReDoc:        http://localhost:8000/redoc
```

### Check System Health

```bash
curl http://localhost:8000/health
```

---

## Transcribe Audio

### Using cURL

```bash
curl -X POST http://localhost:8000/api/v1/transcribe \
  -F "file=@your_audio.mp3"
```

### Using Python

```python
import requests

with open('your_audio.mp3', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/api/v1/transcribe',
        files=files
    )
    print(response.json()['transcript'])
```

### Using JavaScript/Fetch

```javascript
const formData = new FormData();
const audioFile = document.getElementById('audioInput').files[0];
formData.append('file', audioFile);

fetch('http://localhost:8000/api/v1/transcribe', {
    method: 'POST',
    body: formData
})
.then(r => r.json())
.then(data => console.log(data.transcript));
```

---

## Supported Audio Formats

- MP3, WAV, M4A, FLAC, OGG, WebM
- Maximum size: 500MB (configurable)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Change `API_PORT` in `.env` |
| Model not downloading | Check internet; try `--model tiny` |
| Slow transcription | Use `MODEL_SIZE=tiny` in `.env` or enable GPU |
| Memory issues | Reduce model size or close other applications |

---

## Next Steps

1. ✅ Test with sample audio file
2. ✅ Review API documentation at `/docs`
3. ✅ Check logs in `./data/logs/`
4. ✅ Read full guide: [PHASE1_SETUP.md](PHASE1_SETUP.md)

---

**Ready to transcribe! 🎉**
```bash
python main.py
```

**Wait for initialization (about 30 seconds on first run)**, then speak into your microphone!

---

## What You'll See

```
Initializing Model (this takes 10 seconds)...

🔴 Ready! Speak into your microphone...
Press Ctrl+C to stop.

[0.00s -> 2.34s] What is the weather today?
[2.34s -> 5.12s] Can you play my favorite music?
```

Each line shows what the system heard, with timing information.

---

## Next Steps

1. **Read the full documentation**: [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)
2. **Explore components**: Check `src/voice_assistant/` folder
3. **Run tests**: `pytest tests/unit`
4. **Try the API**: `python -m src.voice_assistant.api.server`

---

## Common Issues

### Issue: "ModuleNotFoundError"
```bash
pip install -r requirements/base.txt
```

### Issue: "No microphone detected"
```bash
pip install pyaudio
```

### Issue: "CUDA out of memory"
Edit `main.py` and change:
```python
model = WhisperModel(model_size, device="cpu")  # Use CPU instead
```

---

## Help & Support

- 📖 Read [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md) for detailed explanation
- 🔍 Check [troubleshooting.md](user_guide/troubleshooting.md)
- 💬 Create GitHub issue for help

**Enjoy your voice assistant! 🎉**

