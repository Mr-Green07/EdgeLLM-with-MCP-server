---
sessionId: session-260709-235146-1d34
---

# Findings

### Piper TTS Usage in the Project

Piper (specifically the `piper` Python package / `PiperVoice` class) is used in the following places:

#### 1. Active Code — `whiper_test.py` (root)
A **smoke test** script that imports `from piper import PiperVoice`, loads the `en_US-lessac-medium.onnx` voice model, and synthesizes a sentence to `output.wav`.

#### 2. Commented-Out Code — `one.py` (lines 69–74)
A **commented-out** block that does the same thing with a different voice (`en_US-hfc_female-medium.onnx`).

#### 3. Model Download Script — `scripts/download_models.sh` (lines 10–13)
Downloads Piper voice files from `rhasspy/piper-voices` on Hugging Face (the `en_US-lessac-medium` voice + JSON config).

#### 4. Offline Models Directory — `offline_models/`
Contains Piper `.onnx` voice files and their `.onnx.json` configs:
- `en_US-lessac-medium.onnx` (+json)
- `en_US-hfc_female-medium.onnx` (+json)
- `hi_IN-priyamvada-medium.onnx` (+json)

Also: `scripts/models/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json`

#### 5. Configuration — `.env`
Defines `PIPER_MODEL=en_US-lessac-medium.onnx` (referenced in docs but not consumed by any active source code).

#### 6. Documentation References
- `README.md` — mentions Piper TTS in acknowledgments, file structure, and test instructions
- `docs/CODE_DOCUMENTATION.md` — documents Piper usage in playback (22050 Hz sample rate) and scripts
- `filestructure.md` — lists Piper-related files and directories

#### 7. Indirect Reference — `src/audio/output_handler.py`
The `Playback` class docstring mentions "Piper: 22050 Hz" as the expected TTS sample rate, but **does not import or call Piper directly**. It just consumes PCM audio from whatever TTS engine produces it.

---

### Key Observation

The **production TTS module** (`src/tts/synthesizer.py`) does **NOT** use Piper — it uses **pyttsx3** instead. Piper is only used in standalone test/demo scripts (`whiper_test.py`, commented code in `one.py`) and referenced in config/docs. The `PIPER_MODEL` env var is defined but not consumed by any active production code.

# Delivery Steps

###   Step 1: Audit complete — no code changes needed
This was an investigation-only task. All Piper usage locations have been identified and documented in the Findings tab.

###   Step 2: Optional: Decide on Piper vs pyttsx3 for production TTS
If desired, a follow-up task could:
- Integrate Piper into `src/tts/synthesizer.py` to replace pyttsx3, using the voice models already in `offline_models/`
- Or remove unused Piper references if pyttsx3 is the chosen TTS engine