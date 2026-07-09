"""Brain: STT → LLM → TTS → Playback.

This module is the plug that replaces main.py's placeholder beep once the
pipeline is running. It is injected as `on_utterance` into Pipeline:

    brain = Brain(cfg)
    pipeline = Pipeline(cfg, on_utterance=brain.on_utterance)

Thread safety: on_utterance is called from the main loop (single-threaded),
so no locking is needed here. Heavy init (model loads) happens in __init__
before the pipeline starts.
"""
from __future__ import annotations

import logging

import numpy as np

log = logging.getLogger(__name__)


class Brain:
    """Wires speech recognition → language model → speech synthesis."""

    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg
        log.info("Loading STT model…")
        self._stt = self._init_stt()
        log.info("STT ready")

        log.info("Connecting to LLM…")
        self._llm = self._init_llm()
        log.info("LLM ready")

        log.info("Loading TTS engine…")
        self._tts = self._init_tts()
        log.info("TTS ready")

    # ------------------------------------------------------------------
    def _init_stt(self):
        from src.asr.transcriber import Transcriber
        asr = self.cfg.get("asr", {})
        return Transcriber(
            model_name=asr.get("model", "base"),
            device=asr.get("device", "cpu"),
            language=asr.get("language", "en"),
        )

    def _init_llm(self):
        from src.response_generation.llm_engine import LLMResponseGenerator
        return LLMResponseGenerator(self.cfg)

    def _init_tts(self):
        from src.tts.synthesizer import TTSSynthesizer
        return TTSSynthesizer(self.cfg)

    # ------------------------------------------------------------------
    def on_utterance(self, audio: np.ndarray, pipeline) -> None:
        """Called by the main loop with int16 mono audio captured at 16 kHz.

        Steps:
          1. Normalise int16 → float32 [-1, 1] for Whisper
          2. Transcribe with Whisper
          3. Send transcript to the local LLM (Ollama)
          4. Synthesise the LLM reply with pyttsx3
          5. Enqueue audio to Playback and signal end-of-utterance
        """
        # 1. Normalise
        audio_f32 = audio.astype(np.float32) / 32768.0

        # 2. STT
        try:
            result = self._stt.transcribe(audio_f32)
            text = result.text.strip()
        except Exception as exc:
            log.error("STT failed: %s", exc)
            pipeline.playback.end_of_utterance()
            return

        log.info("STT  → %r", text)
        if not text:
            log.info("Empty transcript, skipping LLM")
            pipeline.playback.end_of_utterance()
            return

        # 3. LLM
        try:
            response = self._llm.generate_response(text)
        except Exception as exc:
            log.error("LLM failed: %s", exc)
            pipeline.playback.end_of_utterance()
            return

        log.info("LLM  → %r", response[:120])
        if not response:
            pipeline.playback.end_of_utterance()
            return

        # 4 + 5. TTS → Playback
        try:
            audio_out = self._tts.synthesize(response)
            if len(audio_out) > 0:
                pipeline.playback.enqueue(audio_out)
        except Exception as exc:
            log.error("TTS failed: %s", exc)

        pipeline.playback.end_of_utterance()
