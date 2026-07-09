"""Exceptions for the response-generation (LLM) module."""


class ResponseGenerationError(Exception):
    """Raised when the LLM backend cannot produce a response
    (unsupported provider, HTTP error, model missing, connection refused)."""
    pass


class LLMTimeoutError(ResponseGenerationError):
    """Raised when the local LLM (Ollama) exceeds the generation timeout."""
    pass


class InvalidPromptError(ResponseGenerationError):
    """Raised when the prompt is empty or malformed."""
    pass
