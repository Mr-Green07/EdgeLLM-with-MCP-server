from src.voice_assistant.storage.models import ConversationLog
from src.voice_assistant.storage.database import SessionLocal

session = SessionLocal()

log = ConversationLog(
    timestamp="2026-06-21",
    user_text="Hello",
    intent="greeting",
    response="Hi there",
    audio_path="audio/test.wav",
    processing_time_ms=150
)

session.add(log)
session.commit()

print("Data Inserted")

session.close()