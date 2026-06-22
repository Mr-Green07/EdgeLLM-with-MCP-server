from src.voice_assistant.storage.models import ConversationLog
from src.voice_assistant.storage.database import SessionLocal

session = SessionLocal()

logs = session.query(ConversationLog).all()

for log in logs:
    print(log.id)
    print(log.user_text)
    print(log.response)
    print("-" * 30)

session.close()