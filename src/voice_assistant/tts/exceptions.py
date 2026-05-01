class TTSException(Exception):
    """Base exception for TTS module"""
    pass


class AudioPlaybackError(TTSException):
    """Raised when audio playback fails"""
    pass


class SynthesisError(TTSException):
    """Raised when text-to-speech synthesis fails"""
    pass


class VoiceNotFoundError(TTSException):
    """Raised when requested voice is not available"""
    pass


