# Practical Examples & Code Snippets

## 🎯 Learn by Doing

This guide shows you actual code you can run to understand each component.

---

## Example 1: Recording Audio

### What It Does
Records audio from your microphone and saves it.

### Code

```python
# File: test_audio_recording.py
from src.voice_assistant.audio import AudioRecorder
import time

# Create recorder
recorder = AudioRecorder()

print("🎤 Recording for 5 seconds...")
print("Say something!")

# Record for 5 seconds
audio_file = recorder.record(duration=5)

print(f"✅ Saved to: {audio_file}")
print(f"📊 File size: {len(audio_file)} bytes")
```

### How to Run
```bash
python test_audio_recording.py
```

### What Happens
1. Microphone turns on
2. Records sound for 5 seconds
3. Saves to a file
4. Prints the file location

---

## Example 2: Convert Speech to Text

### What It Does
Takes an audio file and converts spoken words to text.

### Code

```python
# File: test_speech_to_text.py
from src.voice_assistant.asr import WhisperASR

# Initialize ASR (Speech-to-Text)
print("🤖 Loading Whisper model...")
asr = WhisperASR(
    model_size="large-v3-turbo",  # Best balance of speed/accuracy
    device="cuda"                   # Use GPU (change to "cpu" if no GPU)
)
print("✅ Model loaded!")

# Transcribe audio file
print("\n🔊 Transcribing audio...")
audio_path = "your_audio.mp3"  # Path to audio file
text = asr.transcribe(audio_path)

print(f"📝 You said: {text}")
```

### How to Run
```bash
python test_speech_to_text.py
```

### Example Output
```
🤖 Loading Whisper model...
✅ Model loaded!

🔊 Transcribing audio...
📝 You said: What is the weather today?
```

---

## Example 3: Detect User Intent

### What It Does
Understands what the user means (intent) and extracts important information (entities).

### Code

```python
# File: test_intent_detection.py
from src.voice_assistant.nlu import IntentDetector

# Initialize intent detector
detector = IntentDetector()

# Test different sentences
test_sentences = [
    "Turn on the living room lights",
    "What's the weather?",
    "Play my favorite music",
    "Set a reminder for 2 PM",
    "What time is it?"
]

print("🧠 Intent Detection Examples:\n")

for sentence in test_sentences:
    result = detector.detect(sentence)
    
    print(f"📝 Input: {sentence}")
    print(f"🎯 Intent: {result['intent']}")
    print(f"📊 Entities: {result['entities']}")
    print(f"📈 Confidence: {result['confidence']:.0%}\n")
```

### How to Run
```bash
python test_intent_detection.py
```

### Example Output
```
🧠 Intent Detection Examples:

📝 Input: Turn on the living room lights
🎯 Intent: control_device
📊 Entities: {'device': 'lights', 'location': 'living room', 'action': 'on'}
📈 Confidence: 98%

📝 Input: What's the weather?
🎯 Intent: get_weather
📊 Entities: {}
📈 Confidence: 99%
```

---

## Example 4: Execute Tasks

### What It Does
Performs the action requested by the user.

### Code

```python
# File: test_task_execution.py
from src.voice_assistant.tasks import TaskExecutor

# Initialize task executor
executor = TaskExecutor()

# Define tasks to execute
tasks = [
    {
        "intent": "get_weather",
        "parameters": {"location": "New York"}
    },
    {
        "intent": "control_device",
        "parameters": {"device": "lights", "action": "on", "location": "bedroom"}
    },
    {
        "intent": "get_time",
        "parameters": {}
    }
]

print("⚙️ Task Execution Examples:\n")

for task in tasks:
    print(f"🎯 Executing: {task['intent']}")
    
    try:
        result = executor.execute(
            intent=task['intent'],
            parameters=task['parameters']
        )
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
```

### How to Run
```bash
python test_task_execution.py
```

### Example Output
```
⚙️ Task Execution Examples:

🎯 Executing: get_weather
✅ Result: {'status': 'sunny', 'temperature': 25, 'location': 'New York'}

🎯 Executing: control_device
✅ Result: {'device': 'lights', 'action': 'on', 'status': 'success'}

🎯 Executing: get_time
✅ Result: {'time': '14:30:45', 'timezone': 'UTC'}
```

---

## Example 5: Generate Responses

### What It Does
Creates a natural-sounding response to show to the user.

### Code

```python
# File: test_response_generation.py
from src.voice_assistant.response_generation import ResponseGenerator

# Initialize generator
generator = ResponseGenerator()

# Define responses to generate
responses_to_generate = [
    {
        "task_result": "sunny, 25°C",
        "intent": "get_weather"
    },
    {
        "task_result": "lights turned on",
        "intent": "control_device"
    },
    {
        "task_result": "14:30",
        "intent": "get_time"
    }
]

print("💬 Response Generation Examples:\n")

for item in responses_to_generate:
    response = generator.generate(
        task_result=item['task_result'],
        intent=item['intent']
    )
    
    print(f"🎯 Intent: {item['intent']}")
    print(f"📊 Task Result: {item['task_result']}")
    print(f"💭 Generated Response: {response}\n")
```

### How to Run
```bash
python test_response_generation.py
```

### Example Output
```
💬 Response Generation Examples:

🎯 Intent: get_weather
📊 Task Result: sunny, 25°C
💭 Generated Response: It's a beautiful day! We have sunny skies and the temperature is 25 degrees Celsius.

🎯 Intent: control_device
📊 Task Result: lights turned on
💭 Generated Response: I've successfully turned on the lights for you.

🎯 Intent: get_time
📊 Task Result: 14:30
💭 Generated Response: The current time is 2 o'clock and 30 minutes.
```

---

## Example 6: Text to Speech

### What It Does
Converts text to spoken voice.

### Code

```python
# File: test_text_to_speech.py
from src.voice_assistant.tts import TextToSpeech

# Initialize TTS
tts = TextToSpeech(
    engine="pyttsx3"  # Local engine (no internet needed)
)

# Test phrases
phrases = [
    "Hello! I'm a voice assistant",
    "The weather is sunny and 25 degrees",
    "I've turned on the lights for you",
    "The current time is 2 o'clock"
]

print("🔊 Text-to-Speech Examples:\n")

for phrase in phrases:
    print(f"📝 Speaking: {phrase}")
    
    try:
        tts.speak(phrase)
        print("✅ Spoken!\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
```

### How to Run
```bash
python test_text_to_speech.py
```

### What Happens
- Each phrase will be spoken aloud
- Listen to your speakers!

---

## Example 7: Complete Flow

### What It Does
Combines all components in a complete voice conversation.

### Code

```python
# File: complete_voice_flow.py
from src.voice_assistant.audio import AudioRecorder
from src.voice_assistant.asr import WhisperASR
from src.voice_assistant.nlu import IntentDetector
from src.voice_assistant.tasks import TaskExecutor
from src.voice_assistant.response_generation import ResponseGenerator
from src.voice_assistant.tts import TextToSpeech

def complete_voice_interaction():
    """Complete voice assistant flow"""
    
    print("🎤 Voice Assistant Starting...\n")
    
    # Initialize components
    print("⚙️ Loading models...")
    recorder = AudioRecorder()
    asr = WhisperASR(model_size="large-v3-turbo", device="cuda")
    nlu = IntentDetector()
    executor = TaskExecutor()
    generator = ResponseGenerator()
    tts = TextToSpeech()
    print("✅ Models loaded!\n")
    
    # Loop for continuous interaction
    while True:
        try:
            # Step 1: Record audio
            print("🎤 Listening... (Say something or Ctrl+C to stop)")
            audio_path = recorder.record(duration=5)
            print(f"✅ Audio recorded: {audio_path}\n")
            
            # Step 2: Convert audio to text
            print("📝 Converting speech to text...")
            user_text = asr.transcribe(audio_path)
            print(f"You said: {user_text}\n")
            
            # Step 3: Detect intent
            print("🧠 Understanding intent...")
            intent_result = nlu.detect(user_text)
            intent = intent_result['intent']
            entities = intent_result['entities']
            print(f"Intent: {intent}")
            print(f"Entities: {entities}\n")
            
            # Step 4: Execute task
            print("⚙️ Executing task...")
            task_result = executor.execute(
                intent=intent,
                parameters=entities
            )
            print(f"Task result: {task_result}\n")
            
            # Step 5: Generate response
            print("💬 Generating response...")
            response = generator.generate(
                task_result=task_result,
                intent=intent
            )
            print(f"Assistant: {response}\n")
            
            # Step 6: Speak response
            print("🔊 Speaking response...")
            tts.speak(response)
            print("✅ Response spoken!\n")
            
            print("-" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")
            continue

if __name__ == "__main__":
    complete_voice_interaction()
```

### How to Run
```bash
python complete_voice_flow.py
```

### What Happens
```
🎤 Voice Assistant Starting...

⚙️ Loading models...
✅ Models loaded!

🎤 Listening... (Say something or Ctrl+C to stop)
✅ Audio recorded: /tmp/audio_12345.wav

📝 Converting speech to text...
You said: Turn on the bedroom lights

🧠 Understanding intent...
Intent: control_device
Entities: {'device': 'lights', 'location': 'bedroom', 'action': 'on'}

⚙️ Executing task...
Task result: {'status': 'success', 'message': 'Lights turned on'}

💬 Generating response...
Assistant: I've successfully turned on the bedroom lights for you.

🔊 Speaking response...
✅ Response spoken!

--------------------------------------------------
```

---

## Example 8: Using the API

### What It Does
Shows how to access the voice assistant through REST API.

### Code - Start Server

```python
# File: run_api_server.py
from src.voice_assistant.api import create_app
import uvicorn

if __name__ == "__main__":
    app = create_app()
    
    print("🌐 Starting API server...")
    print("📍 Access at: http://localhost:8000")
    print("📚 Docs at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Code - Make API Calls

```python
# File: test_api_client.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_process_endpoint():
    """Test processing text through API"""
    
    data = {
        "text": "Turn on the living room lights",
        "user_id": "test_user"
    }
    
    response = requests.post(
        f"{BASE_URL}/process",
        json=data
    )
    
    result = response.json()
    print(json.dumps(result, indent=2))

def test_health_endpoint():
    """Check if API is running"""
    
    response = requests.get(f"{BASE_URL}/health")
    status = response.json()
    
    print(f"Status: {status['status']}")
    print(f"Uptime: {status['uptime_seconds']} seconds")

if __name__ == "__main__":
    print("Testing API endpoints...\n")
    
    print("1. Health Check:")
    test_health_endpoint()
    print()
    
    print("2. Process Request:")
    test_process_endpoint()
```

### How to Run

**Terminal 1 - Start Server:**
```bash
python run_api_server.py
```

**Terminal 2 - Make Requests:**
```bash
python test_api_client.py
```

### API Response Example
```json
{
  "intent": "control_device",
  "entities": {
    "device": "lights",
    "location": "living room",
    "action": "on"
  },
  "response": "I've turned on the living room lights",
  "success": true,
  "processing_time_ms": 245
}
```

---

## Example 9: Working with Configuration

### What It Does
Shows how to load and use configuration files.

### Code

```python
# File: test_configuration.py
from src.voice_assistant.utils import load_config
import os

# Load config
env = os.getenv("ENV", "development")  # Default to development
config = load_config(env)

print(f"🔧 Configuration (Environment: {env})\n")

# ASR Settings
print("🎤 ASR Settings:")
print(f"  Model Size: {config['asr']['model_size']}")
print(f"  Device: {config['asr']['device']}")
print(f"  Compute Type: {config['asr']['compute_type']}\n")

# NLU Settings
print("🧠 NLU Settings:")
print(f"  Language: {config['nlu']['language']}")
print(f"  Confidence Threshold: {config['nlu']['confidence_threshold']}\n")

# TTS Settings
print("🔊 TTS Settings:")
print(f"  Engine: {config['tts']['engine']}")
print(f"  Speed: {config['tts']['speed']}\n")

# Wake Word Settings
print("⏰ Wake Word Settings:")
print(f"  Word: {config['wake_word']['word']}")
print(f"  Sensitivity: {config['wake_word']['sensitivity']}\n")
```

### How to Run

```bash
# Use default (development) config
python test_configuration.py

# Use production config
set ENV=production
python test_configuration.py
```

### Example Output
```
🔧 Configuration (Environment: development)

🎤 ASR Settings:
  Model Size: large-v3-turbo
  Device: cuda
  Compute Type: int8

🧠 NLU Settings:
  Language: en
  Confidence Threshold: 0.8

🔊 TTS Settings:
  Engine: pyttsx3
  Speed: 1.0

⏰ Wake Word Settings:
  Word: hey assistant
  Sensitivity: 0.5
```

---

## Example 10: Testing Components

### What It Does
Shows how to write tests for the voice assistant.

### Code

```python
# File: tests/unit/test_components.py
import pytest
from src.voice_assistant.asr import WhisperASR
from src.voice_assistant.nlu import IntentDetector

class TestASR:
    """Test Speech-to-Text functionality"""
    
    @pytest.fixture
    def asr(self):
        """Create ASR instance"""
        return WhisperASR(model_size="base", device="cpu")
    
    def test_transcribe_basic(self, asr):
        """Test basic transcription"""
        # This would use a test audio file
        result = asr.transcribe("test_audio.wav")
        assert result is not None
        assert isinstance(result, str)
    
    def test_transcribe_empty(self, asr):
        """Test transcription with empty audio"""
        with pytest.raises(ValueError):
            asr.transcribe("empty_audio.wav")

class TestNLU:
    """Test Intent Detection functionality"""
    
    @pytest.fixture
    def nlu(self):
        """Create NLU instance"""
        return IntentDetector()
    
    def test_detect_weather_intent(self, nlu):
        """Test weather intent detection"""
        result = nlu.detect("What's the weather?")
        assert result['intent'] == "get_weather"
    
    def test_detect_device_control(self, nlu):
        """Test device control intent"""
        result = nlu.detect("Turn on the lights")
        assert result['intent'] == "control_device"
        assert result['entities']['device'] == "lights"
```

### How to Run

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/unit/test_components.py::TestASR::test_transcribe_basic

# Run with coverage
pytest --cov=src tests/
```

---

## 📊 Comparison Table

| Example | Purpose | Complexity | Time |
|---------|---------|-----------|------|
| 1. Recording | Capture audio | ⭐ | 5s |
| 2. Speech-to-Text | Convert audio to text | ⭐⭐ | 10s |
| 3. Intent Detection | Understand user meaning | ⭐⭐ | 5s |
| 4. Task Execution | Perform actions | ⭐⭐⭐ | 10s |
| 5. Response Generation | Create responses | ⭐⭐ | 5s |
| 6. Text-to-Speech | Convert text to voice | ⭐⭐ | 10s |
| 7. Complete Flow | All components together | ⭐⭐⭐⭐ | 30s |
| 8. API Access | Remote usage | ⭐⭐⭐ | 15s |
| 9. Configuration | Load settings | ⭐ | 5s |
| 10. Testing | Quality assurance | ⭐⭐⭐ | Varies |

---

## 🚀 Next Steps

1. **Try Examples** - Run each example above
2. **Modify Code** - Change parameters and see results
3. **Combine Examples** - Create your own workflows
4. **Add Features** - Build new functionality
5. **Deploy** - Use with Docker or Kubernetes

---

## 💡 Tips

- **Start Simple**: Try Example 1-2 first
- **Understand Flow**: Example 7 shows the complete process
- **Debug Issues**: Add `print()` statements to see what's happening
- **Use Comments**: Explain your code with `#` comments
- **Check Errors**: Look at error messages carefully

---

## 🆘 If Something Goes Wrong

```bash
# Check Python installation
python --version

# Check required packages
pip list | grep torch

# Check configuration
python test_configuration.py

# Run tests
pytest tests/unit

# Check logs
tail -f logs/app.log
```

---

**Happy coding! 🎉**

