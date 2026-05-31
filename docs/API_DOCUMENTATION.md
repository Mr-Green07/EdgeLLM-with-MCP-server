# PHASE 1 API DOCUMENTATION
## REST API Reference for Offline Speech Recognition

**Base URL:** `http://localhost:8000`  
**API Prefix:** `/api/v1`  
**Version:** 1.0  
**Status:** Phase 1 - Speech-to-Text

---

## Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Response Formats](#response-formats)
4. [Error Handling](#error-handling)
5. [Examples](#examples)
6. [Rate Limiting](#rate-limiting)

---

## Authentication

**Phase 1:** No authentication required (localhost only)

**Future (Phase 2+):** API key authentication will be implemented

---

## Endpoints

### 1. Health Check

Check if the API server is running and healthy.

```http
GET /health
```

**Description:** Returns system health status and model information.

**Response Status:** `200 OK`

**Response Body:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model_loaded": true,
  "model_info": {
    "model_size": "base",
    "approximate_size": "140M",
    "parameters": 140000000,
    "device": "cpu",
    "language": "en",
    "model_dir": "./offline_models",
    "model_loaded": true
  },
  "device_info": {
    "device": "cpu",
    "torch_version": "2.0.1",
    "cuda_available": false
  }
}
```

---

### 2. System Status

Get detailed system status and configuration.

```http
GET /api/v1/status
```

**Description:** Returns system configuration, running features, and status.

**Response Status:** `200 OK`

**Response Body:**
```json
{
  "status": "running",
  "version": "1.0.0",
  "timestamp": "2026-05-30T12:00:00.000000",
  "api_prefix": "/api/v1",
  "model_config": {
    "model_size": "base",
    "approximate_size": "140M",
    "parameters": 140000000,
    "device": "cpu",
    "language": "en",
    "model_dir": "./offline_models",
    "model_loaded": true
  },
  "features": {
    "transcription": true,
    "caching": false,
    "sentiment_analysis": false,
    "ner": false,
    "question_answering": false
  }
}
```

---

### 3. Transcribe Audio

Transcribe an audio file to text using Whisper model.

```http
POST /api/v1/transcribe
Content-Type: multipart/form-data
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | Yes | Audio file (mp3, wav, m4a, flac, ogg, webm) |
| `language` | String | No | Language code (e.g., 'en', 'es'); auto-detect if not provided |

**Constraints:**
- Maximum file size: 500MB (configurable via `MAX_UPLOAD_SIZE` in `.env`)
- Supported formats: MP3, WAV, M4A, FLAC, OGG, WebM
- Processing timeout: 300 seconds (5 minutes)

**Response Status:** 
- `200 OK` - Transcription successful
- `400 Bad Request` - Invalid file format or missing file
- `413 Payload Too Large` - File exceeds size limit
- `500 Internal Server Error` - Server error

**Response Body (Success):**
```json
{
  "success": true,
  "message": "Transcription completed successfully",
  "transcript": "This is the transcribed text from the audio file",
  "segments": [
    {
      "id": 0,
      "seek": 0,
      "start": 0.0,
      "end": 3.5,
      "text": "This is the transcribed",
      "tokens": [50364, 307, 264, 26154, 1022],
      "temperature": 0.0,
      "avg_logprob": -0.35,
      "compression_ratio": 1.5,
      "no_speech_prob": 0.001
    },
    {
      "id": 1,
      "seek": 0,
      "start": 3.5,
      "end": 5.0,
      "text": "text from the audio file",
      "tokens": [2487, 365, 264, 4627, 1387],
      "temperature": 0.0,
      "avg_logprob": -0.38,
      "compression_ratio": 1.45,
      "no_speech_prob": 0.002
    }
  ],
  "language": "en",
  "duration": 5.0,
  "processing_time": 2.34,
  "timestamp": "2026-05-30T12:00:00.000000"
}
```

**Response Body (Error):**
```json
{
  "error": true,
  "status_code": 400,
  "detail": "Invalid file format: xyz. Allowed formats: mp3, wav, m4a, flac, ogg, webm",
  "timestamp": "2026-05-30T12:00:00.000000"
}
```

**Example:**

```bash
# Using cURL
curl -X POST http://localhost:8000/api/v1/transcribe \
  -F "file=@sample.mp3" \
  -F "language=en"

# Using Python
import requests

with open('sample.mp3', 'rb') as f:
    files = {'file': f}
    data = {'language': 'en'}
    response = requests.post(
        'http://localhost:8000/api/v1/transcribe',
        files=files,
        data=data
    )
    result = response.json()
    print(result['transcript'])
```

---

### 4. Get Model Information

Get detailed information about the loaded Whisper model.

```http
GET /api/v1/model-info
```

**Response Status:** `200 OK`

**Response Body:**
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

**Example:**
```bash
curl http://localhost:8000/api/v1/model-info | jq
```

---

### 5. Get Supported Formats

Get list of supported audio formats and constraints.

```http
GET /api/v1/supported-formats
```

**Response Status:** `200 OK`

**Response Body:**
```json
{
  "supported_formats": [
    "mp3",
    "wav",
    "m4a",
    "flac",
    "ogg",
    "webm"
  ],
  "max_file_size_mb": 500,
  "max_file_size_description": "500MB"
}
```

---

### 6. Get Supported Languages

Get information about supported languages for transcription.

```http
GET /api/v1/languages
```

**Response Status:** `200 OK`

**Response Body:**
```json
{
  "auto_detect": true,
  "default_language": "en",
  "note": "Whisper supports 99+ languages. Specify language code for better accuracy or leave empty for auto-detection."
}
```

**Common Language Codes:**
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean
- `ru` - Russian
- `ar` - Arabic
- `pt` - Portuguese

---

### 7. Root Endpoint

Get basic API information and available endpoints.

```http
GET /
```

**Response Status:** `200 OK`

**Response Body:**
```json
{
  "name": "Offline Speech Recognition System",
  "phase": "Phase 1 - Speech-to-Text Transcription",
  "version": "1.0.0",
  "description": "OpenAI Whisper based offline speech recognition",
  "api_prefix": "/api/v1",
  "endpoints": {
    "health": "/health",
    "status": "/api/v1/status",
    "transcribe": "/api/v1/transcribe (POST)",
    "model_info": "/api/v1/model-info",
    "supported_formats": "/api/v1/supported-formats",
    "supported_languages": "/api/v1/languages",
    "docs": "/docs"
  }
}
```

---

## Response Formats

### Successful Transcription Response

```json
{
  "success": true,
  "message": "Transcription completed successfully",
  "transcript": "Full transcribed text...",
  "segments": [
    {
      "start": 0.0,
      "end": 3.5,
      "text": "Text segment..."
    }
  ],
  "language": "en",
  "duration": 5.0,
  "processing_time": 2.34,
  "timestamp": "2026-05-30T12:00:00"
}
```

### Error Response

```json
{
  "error": true,
  "status_code": 400,
  "detail": "Error message describing what went wrong",
  "timestamp": "2026-05-30T12:00:00"
}
```

---

## Error Handling

### Common HTTP Status Codes

| Status | Meaning | Description |
|--------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid file format or parameters |
| 413 | Payload Too Large | File size exceeds limit |
| 500 | Server Error | Internal server error |
| 503 | Service Unavailable | Model not loaded |

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid file format: xyz" | Unsupported audio format | Use mp3, wav, m4a, flac, ogg, or webm |
| "File too large: 600MB" | Exceeds size limit | Reduce file size or split into smaller files |
| "Model not loaded" | Server initialization failed | Check logs and restart server |
| "File not found" | Upload failed | Try uploading again |

---

## Examples

### Example 1: Basic Transcription

```python
import requests

def transcribe_audio(file_path):
    """Transcribe an audio file."""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            'http://localhost:8000/api/v1/transcribe',
            files=files
        )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Transcript: {result['transcript']}")
        print(f"Language: {result['language']}")
        print(f"Processing Time: {result['processing_time']}s")
    else:
        print(f"Error: {response.json()['detail']}")

transcribe_audio('sample.mp3')
```

### Example 2: Transcription with Language Specification

```python
import requests

def transcribe_with_language(file_path, language='en'):
    """Transcribe audio with specific language."""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'language': language}
        response = requests.post(
            'http://localhost:8000/api/v1/transcribe',
            files=files,
            data=data
        )
    
    return response.json()

# Transcribe Spanish audio
result = transcribe_with_language('spanish_audio.mp3', language='es')
print(result['transcript'])
```

### Example 3: Check System Status

```python
import requests

def check_system_status():
    """Check if system is healthy and model is loaded."""
    response = requests.get('http://localhost:8000/health')
    
    if response.status_code == 200:
        health = response.json()
        print(f"Status: {health['status']}")
        print(f"Model Loaded: {health['model_info']['model_loaded']}")
        print(f"Device: {health['device_info']['device']}")
        return True
    return False

check_system_status()
```

### Example 4: Using JavaScript/Fetch

```javascript
async function transcribeAudio(audioFile) {
    const formData = new FormData();
    formData.append('file', audioFile);
    
    try {
        const response = await fetch('http://localhost:8000/api/v1/transcribe', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Transcript:', result.transcript);
            console.log('Language:', result.language);
            console.log('Processing Time:', result.processing_time + 's');
        } else {
            const error = await response.json();
            console.error('Error:', error.detail);
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
}

// Usage
const fileInput = document.getElementById('audioFile');
fileInput.addEventListener('change', (e) => {
    transcribeAudio(e.target.files[0]);
});
```

---

## Rate Limiting

**Phase 1:** No rate limiting implemented.

**Phase 2+:** Rate limiting will be added based on deployment environment.

---

## API Documentation Tools

### Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

### Testing Tools

- **cURL:** Command-line HTTP client
- **Postman:** GUI REST client
- **HTTPie:** User-friendly HTTP client
- **Python Requests:** Python HTTP library

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | May 30, 2026 | Initial Phase 1 API release |

---

**End of API Documentation**
