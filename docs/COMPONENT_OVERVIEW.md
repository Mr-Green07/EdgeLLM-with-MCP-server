# Component Overview - Visual Guide

## 🏗️ System Architecture

### The Big Picture

```
┌─────────────────────────────────────────────────────┐
│         YOU (Speak into microphone)                 │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
        ╔════════════════════╗
        ║   WAKE WORD        ║  "Hey Assistant"
        ║   DETECTION        ║  Only starts on wake word
        ║  (Porcupine)       ║
        ╚────────┬───────────╝
                 │
                 ▼
        ╔════════════════════╗
        ║   AUDIO INPUT      ║  Records your voice
        ║  (PyAudio)         ║  Captures sound waves
        ╚────────┬───────────╝
                 │
                 ▼
        ╔════════════════════╗
        ║ SPEECH-TO-TEXT     ║  "What's the weather?"
        ║ ASR (Whisper)      ║  Converts voice to text
        ╚────────┬───────────╝
                 │
                 ▼
        ╔════════════════════╗
        ║ INTENT DETECTION   ║  Intent: "get_weather"
        ║ NLU                ║  Understands your request
        ╚────────┬───────────╝
                 │
                 ▼
        ╔════════════════════╗
        ║ TASK EXECUTION     ║  Fetches weather data
        ║ (Custom Code)      ║  Performs the action
        ╚────────┬───────────╝
                 │
                 ▼
        ╔════════════════════╗
        ║ RESPONSE GEN       ║  "It's sunny today"
        ║ (Templates/LLM)    ║  Creates natural response
        ╚────────┬───────────╝
                 │
                 ▼
        ╔════════════════════╗
        ║ TEXT-TO-SPEECH     ║  Converts to voice
        ║ TTS                ║  Generates audio
        ╚────────┬───────────╝
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│      YOU (Hear response through speakers)           │
└─────────────────────────────────────────────────────┘
```

---

## 📦 Component Details

### 1. Wake Word Detection
```
Status: Listening (Low Power)
        ↓
You say "Hey Assistant"
        ↓
Wake word detected!
        ↓
Status: Active (Full Processing)
```

**File**: `src/voice_assistant/wake_word/`
**Library**: Porcupine
**Speed**: <100ms

---

### 2. Audio Input
```
Microphone Sound Wave
        ↓
PyAudio Captures
        ↓
Librosa Processes
        ↓
Audio Data (WAV/MP3)
```

**File**: `src/voice_assistant/audio/`
**Libraries**: PyAudio, Librosa
**Formats**: WAV, MP3, FLAC

---

### 3. Speech-to-Text (ASR)

```
Input: Audio File
        ↓
Whisper AI Model
        ↓
Output: "Turn on the lights"
Confidence: 98.5%
Language: en
```

**File**: `src/voice_assistant/asr/`
**Model**: OpenAI Whisper
**Options**: 
- `base` - Fastest
- `small` - Fast
- `medium` - Balanced
- `large-v3-turbo` - Recommended
- `large-v3` - Most accurate

---

### 4. Intent Detection (NLU)

```
Input: "Turn on the living room lights"
        ↓
Tokenizer breaks into words
        ↓
Intent Classifier: "control_device"
Entity Extractor: 
  - device: "lights"
  - location: "living room"
  - action: "on"
```

**File**: `src/voice_assistant/nlu/`
**Methods**: Rules-based or ML-based

---

### 5. Task Execution

```
Intent: control_device
Params: {device: lights, action: on, location: living room}
        ↓
Task Router finds handler
        ↓
Handler executes action
        ↓
Result: Success
        ↓
Returns: Task Status
```

**File**: `src/voice_assistant/tasks/`
**Handlers**: Custom functions per task

---

### 6. Response Generation

```
Task Result: Success
Original Request: "Turn on the lights"
        ↓
Template/AI Generator
        ↓
Response: "I've turned on the living room lights"
```

**File**: `src/voice_assistant/response_generation/`
**Methods**: Templates or LLM

---

### 7. Text-to-Speech (TTS)

```
Input: "I've turned on the lights"
        ↓
TTS Engine (pyttsx3 or Cloud)
        ↓
Output: Audio (MP3/WAV)
Quality: Natural sounding
```

**File**: `src/voice_assistant/tts/`
**Options**: Local or Cloud TTS

---

## 🔄 Data Flow

### Example: "Turn on the lights"

```
STAGE 1: Input
┌─────────────────────────┐
│ Audio wave data         │
│ (Sound from mic)        │
└────────────┬────────────┘
             │
STAGE 2: Processing
┌─────────────────────────┐
│ Text: "Turn on lights"  │
└────────────┬────────────┘
             │
STAGE 3: Understanding
┌─────────────────────────┐
│ Intent: control_device  │
│ Device: lights          │
│ Action: on              │
└────────────┬────────────┘
             │
STAGE 4: Action
┌─────────────────────────┐
│ Execute: Turn on lights │
│ Result: Success         │
└────────────┬────────────┘
             │
STAGE 5: Response
┌─────────────────────────┐
│ Text: "Lights are on"   │
└────────────┬────────────┘
             │
STAGE 6: Output
┌─────────────────────────┐
│ Audio response          │
│ (Sound from speaker)    │
└─────────────────────────┘
```

---

## 🗂️ Folder Structure Simplified

```
ASR (Main Folder)
├── main.py ...................... Run this! ⭐
├── audio.py ...................... Audio recording
├── requirement.txt ............... Python packages
│
├── src/voice_assistant/ .......... Core logic
│   ├── audio/ ................... Audio input/output
│   ├── asr/ ..................... Speech-to-text
│   ├── nlu/ ..................... Intent detection
│   ├── tasks/ ................... Execute actions
│   ├── response_generation/ ..... Create responses
│   ├── tts/ ..................... Text-to-speech
│   ├── wake_word/ ............... Wake word detection
│   ├── api/ ..................... REST API
│   ├── storage/ ................. Database
│   ├── core/ .................... Main orchestrator
│   └── utils/ ................... Helper functions
│
├── config/ ....................... Settings
│   ├── base.yaml ................ Default config
│   ├── development.yaml ......... Dev settings
│   ├── production.yaml .......... Production settings
│   └── models/ .................. Model configs
│
├── tests/ ........................ Quality checks
│   ├── unit/ .................... Component tests
│   ├── integration/ ............. Combined tests
│   └── e2e/ ..................... Full flow tests
│
├── docs/ ......................... Documentation
│   ├── COMPLETE_GUIDE.md ........ Full guide ⭐
│   ├── QUICK_START.md ........... Quick start ⭐
│   └── architecture/ ............ How it's designed
│
├── docker/ ....................... Container setup
│   ├── Dockerfile ............... Production image
│   └── docker-compose.yml ....... Run all services
│
└── kubernetes/ ................... Cloud deployment
    ├── deployment.yaml .......... Deploy config
    └── helm/ .................... Templates
```

---

## 🚀 Execution Flow

### When You Start the Program

```python
# main.py starts

↓

# Initialize Whisper model
model = WhisperModel("large-v3-turbo", device="cuda")
# This takes ~30 seconds

↓

# Load audio recording
live_audio_path = audio.record_audio()
# This waits for your speech

↓

# Convert audio to text
segments, info = model.transcribe(live_audio_path)
# This processes your voice

↓

# Display results
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

↓

# Repeat - listen for next input
```

---

## 🔌 API Integration

### REST Endpoints

```
GET  /status ..................... Server is running?
GET  /health ..................... System health check
POST /process .................... Process text command
POST /transcribe ................. Convert audio to text
POST /speak ...................... Convert text to audio
GET  /history .................... Get past conversations
```

### Example API Call

```bash
# Start server
python -m src.voice_assistant.api.server

# In another terminal
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "text": "What is the weather?",
    "user_id": "user123"
  }'

# Response
{
  "intent": "get_weather",
  "entities": {},
  "response": "It's sunny and 25 degrees",
  "success": true
}
```

---

## ⚙️ Configuration

### Key Configuration Points

```yaml
# config/base.yaml

asr:
  model_size: "large-v3-turbo"    # Change model size
  device: "cuda"                    # Change to "cpu"
  compute_type: "int8"              # Change precision

nlu:
  language: "en"                    # Change language
  confidence_threshold: 0.8          # When to trust results

tts:
  engine: "pyttsx3"                 # Use different TTS
  speed: 1.0                        # Speech speed

wake_word:
  word: "hey assistant"             # Change wake word
  sensitivity: 0.5                  # Detection sensitivity
```

---

## 📊 Performance Metrics

### Speed

| Component | Time |
|-----------|------|
| Wake Word Detection | <100ms |
| ASR (Whisper) | 1-3x real-time |
| NLU | <50ms |
| TTS | 1-2x real-time |
| **Total | 5-10 seconds |

### Accuracy

| Component | Accuracy |
|-----------|----------|
| Wake Word | 99%+ |
| ASR | 99%+ |
| NLU | 95%+ |
| TTS | 99%+ |

### Resource Usage

| Resource | Usage |
|----------|-------|
| RAM | 4-8GB |
| GPU | 4-6GB VRAM |
| CPU | 10-30% |
| Disk | 20GB (models) |

---

## 🛠️ Common Customizations

### Change Model Size
```python
# In main.py
model_size = "base"  # Faster but less accurate
```

### Use CPU Instead of GPU
```python
# In main.py
device = "cpu"  # No GPU needed
```

### Change Wake Word
```yaml
# In config/base.yaml
wake_word:
  word: "hi there"
```

### Add Custom Task
```python
# In src/voice_assistant/tasks/handlers/
def handle_custom_task(params):
    # Your code here
    return result
```

---

## 📚 Learn More

- **Complete Guide**: [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)
- **Architecture**: [docs/architecture/](architecture/)
- **API Docs**: [docs/api/](api/)
- **Deployment**: [docs/deployment/](deployment/)

---

## 🎯 Next Steps

1. ✅ **Install** - Follow Quick Start
2. ✅ **Explore** - Run `python main.py`
3. ✅ **Understand** - Read Component sections above
4. ✅ **Customize** - Modify configs and code
5. ✅ **Deploy** - Use Docker or Kubernetes

**Happy building! 🎉**

