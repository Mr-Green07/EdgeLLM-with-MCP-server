"""Wires capture -> wakeword/vad -> (brain) -> playback into one organism.

Thread model:
  [PortAudio in]   capture callback -> bounded queue           (never blocks)
  [audio worker]   iterates capture.chunks(): feeds the wake engine ALWAYS,
                   feeds the VAD endpointer only while LISTENING, publishes
                   events. Handles barge-in inline (playback.stop() must not
                   wait for the main loop).
  [main loop]      consumes events, owns ALL state transitions, runs the
                   utterance handler (STT -> router -> agent -> TTS later).
  [PortAudio out]  playback callback drains its own buffer.

The brain is a plug: on_utterance(audio_16k_int16, pipeline). Until
Milestones 1-2 land, a placeholder beeps back -- which makes the whole
audio shell runnable on real hardware today:  python main.py

Known caveat (accepted): the wake chime plays while LISTENING begins, so the
mic hears it. It is 120 ms of pure tones; Silero scores tones low, and the
endpointer needs ~100 ms of sustained speech-prob to start. Revisit only if
logs show chime-triggered speech_starts.
"""
from __future__ import annotations
import os
import sys
import logging
import threading

import numpy as np

from src.audio.capture import MicCapture, Rebuffer
from src.core.events import Event, EventBus
from src.core.state import State, StateMachine

log = logging.getLogger(__name__)

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))
class Pipeline:
    def __init__(self, cfg: dict, *, capture=None, wake=None, vad=None,
                 playback=None, on_utterance=None) -> None:
        self.cfg = cfg
        self.bus = EventBus()
        self.fsm = StateMachine()
        # components are injectable (tests); heavy ones import lazily
        if capture is None:
            capture = MicCapture(cfg)
        if wake is None:
            from src.audio.wakeword import WakeWordEngine
            wake = WakeWordEngine(cfg)
        if vad is None:
            from src.audio.vad import VadEndpointer
            vad = VadEndpointer(cfg)
        if playback is None:
            from src.audio.playback import Playback
            playback = Playback(cfg)
        self.capture, self.wake, self.vad, self.playback = \
            capture, wake, vad, playback
        self.on_utterance = on_utterance or self._placeholder_reply
        self._wake_rb = Rebuffer(self.wake.FRAME_LEN)
        self._vad_rb = Rebuffer(self.vad.FRAME_LEN)
        self._wake_tail = int(
            16000 * cfg.get("audio", {}).get("wake_tail_ms", 300) / 1000)
        self._stop = threading.Event()

    # ---- audio worker thread --------------------------------------------
    def _audio_worker(self) -> None:
        for chunk in self.capture.chunks():
            for frame in self._wake_rb.push(chunk):
                if self.wake.process(frame):
                    st = self.fsm.state
                    if st == State.SPEAKING:
                        self.playback.stop()          # barge-in: kill NOW,
                        self.bus.publish(Event("barge_in"))  # not next tick
                    elif st == State.IDLE:
                        self.bus.publish(Event("wake"))
                    # wake during LISTENING/THINKING: already engaged, ignore
            if self.fsm.state == State.LISTENING:
                for frame in self._vad_rb.push(chunk):
                    ev = self.vad.process(frame)
                    if ev is not None:
                        self.bus.publish(Event(ev.kind, ev))

    # ---- main loop --------------------------------------------------------
    def run_forever(self) -> None:
        threading.Thread(target=self._audio_worker,
                         name="audio", daemon=True).start()
        log.info("ready -- say the wake word")
        try:
            while not self._stop.is_set():
                ev = self.bus.next(timeout=0.2)
                if ev is not None:
                    self._handle(ev)
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()

    def shutdown(self) -> None:
        self._stop.set()
        self.capture.stop()
        self.playback.close()

    # ---- event handling (single thread: the main loop) -------------------
    def _handle(self, ev: Event) -> None:
        if ev.kind in ("wake", "barge_in"):
            if self.fsm.state not in (State.IDLE, State.SPEAKING):
                return
            self.fsm.transition(State.LISTENING)
            self.vad.reset()
            self._vad_rb = Rebuffer(self.vad.FRAME_LEN)  # drop stale partials
            self.wake.set_speaking(False)
            if ev.kind == "wake":
                self.playback.chime()
            self._warm_start_vad()
        elif ev.kind == "speech_start":
            log.info("speech started")
        elif ev.kind == "timeout":
            log.info("no speech after wake -- back to sleep")
            if self.fsm.state == State.LISTENING:
                self.fsm.transition(State.IDLE)
        elif ev.kind == "endpoint":
            if self.fsm.state == State.LISTENING:
                self._respond(ev.payload.audio)

    def _warm_start_vad(self) -> None:
        """Feed the pre-roll tail (audio spoken WHILE the wake word was being
        confirmed) into the endpointer -- 'alexa set a timer' said in one
        breath loses nothing."""
        if self._wake_tail <= 0:
            return          # NB: arr[-0:] is the WHOLE array, hence the guard
        tail = self.capture.preroll.snapshot()[-self._wake_tail:]
        for frame in self._vad_rb.push(tail):
            ev = self.vad.process(frame)
            if ev is not None:
                self.bus.publish(Event(ev.kind, ev))

    def _respond(self, utt_audio: np.ndarray) -> None:
        self.fsm.transition(State.THINKING)
        try:
            self.wake.set_speaking(True)      # our voice is about to play
            self.fsm.transition(State.SPEAKING)
            self.on_utterance(utt_audio, self)     # the brain plug
            self.playback.wait_done()              # unblocks early on barge-in
        except Exception:
            log.exception("utterance handler failed")
            self.playback.stop()
        finally:
            self.wake.set_speaking(False)
            if self.fsm.state in (State.THINKING, State.SPEAKING):
                self.fsm.transition(State.IDLE)

    # ---- placeholder brain (replaced by STT -> router -> agent -> TTS) ---
    def _placeholder_reply(self, audio: np.ndarray, pipeline: "Pipeline") -> None:
        log.info("utterance captured: %.2f s (brain not wired yet)",
                 len(audio) / 16000)
        sr = self.playback.src_rate
        t = np.arange(int(0.09 * sr)) / sr
        env = np.minimum(1.0, np.minimum(t / 0.01, (t[-1] - t) / 0.02))
        for f in (660.0, 440.0):                   # descending: "heard you"
            self.playback.enqueue(0.2 * np.sin(2 * np.pi * f * t) * env)
        self.playback.end_of_utterance()