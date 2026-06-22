# pyrefly: ignore [missing-import]
from sqlalchemy.orm import declarative_base
# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Float
# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine


Base = declarative_base()
engine = create_engine("sqlite:///./data/database/asr.db")

class ConversationLog(Base):
    __tablename__ = 'conversation_logs'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(String, nullable=False)
    user_text = Column(String, nullable=False)       # Output from ASR
    intent = Column(String, nullable=False)          # Output from NLU
    response = Column(String, nullable=False)        # Read by TTS
    
    # 💾 Crucial Column: Points directly to the file on disk
    audio_path = Column(String, nullable=False)       # e.g., "data/audio/recording_20260621.wav"
    
    processing_time_ms = Column(Float, nullable=False)

print(Base)
# print(ConversationLog)
# NOTE: create_all is called from create_db.py, not here
