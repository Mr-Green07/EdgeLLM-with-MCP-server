# import whisper as ws  # type: ignore

# model = ws.load_model("small")
# result = model.transcribe("sample-0.mp3")
# print(result["text"])


import wave
from piper import PiperVoice

voice = PiperVoice.load("./offline_models/en_US-lessac-medium.onnx")

with wave.open("output.wav", "wb") as wav_file:
    voice.synthesize_wav("Hello world, this is the new era of staring of this world", wav_file)

print("Audio saved to output.wav")
