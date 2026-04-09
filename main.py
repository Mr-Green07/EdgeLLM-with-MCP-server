from faster_whisper import WhisperModel
import audio 

# Use "large-v3-turbo" -> It is almost as accurate as Large, but much faster and lighter.
# If you want absolute max accuracy, change to "large-v3".
model_size = "large-v3-turbo"

# Run on GPU (cuda) with INT8 quantization to fit in 4GB VRAM
model = WhisperModel(model_size, device="cuda", compute_type="int8")

# segments, info = model.transcribe("your_audio.mp3", beam_size=5)
live_audio_path = audio.record_audio()  # make sure audio.py saves/returns a playable file path
segments, info = model.transcribe(live_audio_path, beam_size=5)
print(f"Detected language: {info.language}")
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
