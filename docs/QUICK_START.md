# Voice Assistant - Quick Start Guide

## Get Started in 5 Minutes ⚡

### 1️⃣ **Install Python** (if not already installed)
- Download from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

### 2️⃣ **Download Project**
```bash
git clone https://github.com/Mr-Green07/ASR.git
cd ASR
```

### 3️⃣ **Set Up Environment** (Windows)
```bash
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1
```

### 4️⃣ **Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements/base.txt
```

### 5️⃣ **Run the Program**
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

