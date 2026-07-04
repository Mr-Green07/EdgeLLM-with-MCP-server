---
sessionId: session-260702-182457-lpyc
---

# Requirements

### Overview & Goals
Get the ASR project running successfully by fixing all blocking issues found during investigation.

### Issues Found

1. **PyTorch DLL load failure (BLOCKER)** — `torch 2.11.0+cu128` fails to load `c10.dll`. The installed torch build requires CUDA 12.8 runtime libraries, but the system driver reports CUDA UMD 13.3. This version mismatch causes an `OSError: [WinError 1114]` preventing `import torch` and therefore `import whisper`.

2. **Missing `download_models.py`** — README references `python download_models.py --model base` but the file does not exist in the project.

3. **Empty `offline_models/` directory** — No Whisper model weights are downloaded. The app will fail at startup when `whisper.load_model()` tries to load a model.

4. **`openai-whisper` and `torch` commented out in `requirement.txt`** — Lines 4-5 have `openai-whisper` and `torch`/`torchaudio` commented out, so a fresh `pip install -r requirement.txt` won't install the core dependencies.

5. **Duplicate/conflicting Redis packages** — `requirement.txt` lists both `redis==5.0.0` and `redis-py==5.0.0` (line 27). `redis-py` is not a valid PyPI package name; the package is just `redis`.

6. **`.env` sets `DEVICE=cuda`** — If CUDA is not working, the app should default to `cpu`.

7. **Missing `data/` subdirectories** — `data/logs/`, `data/temp/`, `data/database/` directories are empty/missing (though `main.py` creates `data/temp` and `output` automatically).

### Scope
- **In Scope**: Fix all issues above so `python main.py` starts successfully.
- **Out of Scope**: Phase 2+ features, `src/voice_assistant` module, `audio.py` real-time recording.

# Technical Design

### Key Decisions
- **Reinstall PyTorch with correct CUDA version**: Uninstall current torch and reinstall `torch` + `torchaudio` matching the system's CUDA capability. Since the driver supports CUDA 13.3, a `cu128` build should work — the DLL issue is likely a corrupted install or missing Visual C++ redistributable. Alternatively, install CPU-only torch as a safe fallback.
- **Create `download_models.py`**: A simple script that uses `whisper.load_model()` to download and cache a model to `./offline_models/`.

### Proposed Changes

 File | Change |
------|--------|
 `requirement.txt` | Uncomment `openai-whisper`, add `torch` + `torchaudio` with proper index URL, remove duplicate `redis-py` line |
 `download_models.py` | **New file** — CLI script to download Whisper models to `offline_models/` |
 `.env` | Change `DEVICE=cuda` → `DEVICE=cpu` as safe default (user can switch back) |
 `models.py` | Add fallback: if CUDA requested but unavailable, fall back to CPU with a warning |

### Risks
- PyTorch CUDA builds are large (~2.5GB) and download may be slow.
- If the DLL issue persists after reinstall, CPU-only torch is the fallback.

# Delivery Steps

###   Step 1: Fix dependencies and PyTorch installation
The project installs and imports torch/whisper successfully.

- Uncomment `openai-whisper` in `requirement.txt` and add proper `torch`/`torchaudio` entries
- Remove the duplicate `redis-py==5.0.0` line (keep only `redis==5.0.0`)
- Reinstall PyTorch with the correct CUDA build (or CPU-only as fallback) via `pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128`
- Verify `import torch` and `import whisper` succeed

###   Step 2: Create download_models.py and add CUDA fallback
The missing model downloader script exists and models.py gracefully handles CUDA unavailability.

- Create `download_models.py` with argparse CLI accepting `--model` (tiny/base/small/medium/large) and `--output-dir` (default `./offline_models`)
- Use `whisper.load_model(name, download_root=output_dir)` to download and cache the model
- In `models.py`, add a try/except around CUDA device selection: if `torch.cuda.is_available()` is False and device is `cuda`, log a warning and fall back to `cpu`
- Update `.env` to set `DEVICE=cpu` as the safe default

###   Step 3: Download model and verify server startup
The server starts successfully with `python main.py`.

- Run `python download_models.py --model base` to download the base model
- Run `python main.py` and verify the FastAPI server starts on port 8000
- Confirm the `/api/v1/health` endpoint responds correctly
- Create missing directories (`data/logs/`, `data/database/`) if not auto-created