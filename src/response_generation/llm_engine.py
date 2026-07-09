import requests
import json
from src.response_generation.exceptions import (
    ResponseGenerationError,
    LLMTimeoutError
)

class LLMResponseGenerator:
    def __init__(self, config: dict):
        """
        Initializes the response generator using your base.yaml config rules.
        """
        self.llm_config = config.get("llm", {})
        self.provider = self.llm_config.get("provider", "ollama")
        self.model_name = self.llm_config.get("model_name", "gemma2:2b-it-qat")
        self.base_url = self.llm_config.get("base_url", "http://localhost:11434")

    def generate_response(self, user_prompt: str, context: str = "") -> str:
        """
        Routes the system transcript directly to your local quantized Gemma model.
        """
        if self.provider != "ollama":
            raise ResponseGenerationError(f"Unsupported LLM provider: {self.provider}")

        # Construct a clean, speech-friendly instruction system prompt
        payload = {
            "model": self.model_name,
            "prompt": f"System Context: {context}\nUser: {user_prompt}\nAssistant:",
            "stream": False,
            "options": {
                "temperature": 0.3  # Keep responses predictable and fast
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=10  # Enforces clean execution bounds to prevent endless loop hangs
            )
            
            if response.status_code == 404:
                raise ResponseGenerationError(
                    f"Model '{self.model_name}' not found. Did you run 'ollama run {self.model_name}'?"
                )
            elif response.status_code != 200:
                raise ResponseGenerationError(f"Ollama returned error status: {response.status_code}")

            result_json = response.json()
            return result_json.get("response", "").strip()

        except requests.exceptions.Timeout:
            raise LLMTimeoutError("The local Ollama model timed out during generation.")
        except requests.exceptions.ConnectionError:
            raise ResponseGenerationError("Could not connect to Ollama server. Verify it is running.")
