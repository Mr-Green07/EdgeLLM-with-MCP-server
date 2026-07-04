---
sessionId: session-260703-092805-cm3p
---

# Requirements

### Overview & Goals
Fix the `WhisperModelManager` so that Whisper models are actually downloaded to and loaded from the `./offline_models` directory instead of the default cache (`~/.cache/whisper`).

### Problem
The current code sets `os.environ['WHISPER_CACHE']` before calling `whisper.load_model()`, but **Whisper does not use a `WHISPER_CACHE` environment variable**. The `whisper.load_model()` function accepts a `download_root` parameter to control where models are stored. Because this parameter is not passed, models always download to the default system cache directory (`~/.cache/whisper` on Linux, `C:\Users\<user>\.cache\whisper` on Windows), which is why `./offline_models` stays empty.

### Scope
- **In Scope**: Fix `load_model()` to pass `download_root=self.model_dir` so models are saved to `./offline_models`.
- **Out of Scope**: No changes to transcription logic, UI, or other files.

# Technical Design

### Current Implementation
In `models.py` line 82-88, the `load_model` method sets a non-existent `WHISPER_CACHE` env var and calls `whisper.load_model()` without `download_root`:
```python
os.environ['WHISPER_CACHE'] = str(self.model_dir)
self.model = whisper.load_model(self.model_size, device=self.device)
```

### Proposed Changes
File: `models.py`

1. **Remove** the fake `WHISPER_CACHE` env var line (line 82).
2. **Pass `download_root`** to `whisper.load_model()`:
```python
self.model = whisper.load_model(
    self.model_size,
    device=self.device,
    download_root=str(self.model_dir)
)
```

This is the only change needed. The `whisper.load_model()` API accepts `download_root` which controls both where models are downloaded to and loaded from.

# Delivery Steps

###   Step 1: Fix download_root parameter in load_model
Models are downloaded to `./offline_models` instead of the default cache directory.

- Remove the ineffective `os.environ['WHISPER_CACHE']` line from `load_model()` in `models.py`
- Add `download_root=str(self.model_dir)` parameter to the `whisper.load_model()` call

###   Step 2: Verify the fix
Confirm the fix works correctly.

- Run `models.py` directly (`python models.py`) to trigger model download
- Check that the model `.pt` file appears in `./offline_models/`
- Verify `list_downloaded_models()` returns the downloaded model