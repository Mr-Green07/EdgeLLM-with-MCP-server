# Dummy snapshot logic inside src/voice_assistant/nlu/intent.py
class IntentDetector:
    def detect(self, transcript_text: str) -> dict:
        text = transcript_text.lower()
        
        # Phase 1 Simple Rule/Keyword Parser
        if any(word in text for word in ["turn", "switch", "open", "close", "run"]):
            return {
                "intent": "COMMAND",
                "entities": {"raw_query": transcript_text}
            }
        else:
            return {
                "intent": "CHAT",
                "entities": {}
            }