import whisper as ws # type: ignore


model = ws.load_model("base")
result = model.transcribe("sample-0.mp3")
print(result["text"])