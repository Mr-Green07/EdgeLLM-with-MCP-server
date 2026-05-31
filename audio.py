from RealtimeSTT import AudioToTextRecorder

if __name__ == '__main__':
    print("Initializing Model (this takes 10 seconds)...")

    # We configure it for your 4GB GPU (cuda + int8)
    # "large-v3-turbo" is the best balance of speed/quality for live
    recorder = AudioToTextRecorder(
        model="medium",
        language="en",
        device="cuda", 
        compute_type="int8",
        spinner=False  # Turn off the loading spinner for cleaner text
    )

    print("🔴 Ready! Speak into your microphone...")
    print("Press Ctrl+C to stop.")

    while True:
        # This will block until you finish a sentence, then print the text
        print(recorder.text())
