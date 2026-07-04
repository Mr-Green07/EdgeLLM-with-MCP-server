from dotenv import load_dotenv
from piper import PiperVoice
import wave
import os

# Load .env from the project root (two levels up from this script)
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# Build model path from .env values
MODEL_DIR = os.getenv("MODEL_DIR", "./offline_models")
PIPER_MODEL = os.getenv("PIPER_MODEL", "en_US-lessac-medium.onnx")
MODEL_PATH = os.path.normpath(os.path.join(PROJECT_ROOT, MODEL_DIR, PIPER_MODEL))

voice = PiperVoice.load(MODEL_PATH)


with wave.open("output.wav", "wb") as wav_file:
    voice.synthesize_wav("Hello world, this is twhy this is working he new era of staring of this world", wav_file)

print("Audio saved to output.wav")