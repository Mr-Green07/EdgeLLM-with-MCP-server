import pvporcupine
import pyaudio

# Wake word detector using Porcupine (example)

class WakeWordDetector:
    def __init__(self, access_key, keywords=None):
        self.porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=keywords or ["jarvis"]
        )
        self.audio_stream = None
    
    def detect(self):
        """Stream audio and detect wake word"""
        pa = pyaudio.PyAudio()
        self.audio_stream = pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )
        
        try:
            while True:
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                result = self.porcupine.process(pcm)
                if result >= 0:
                    return f"Wake word detected: {result}"
        finally:
            self.audio_stream.close()