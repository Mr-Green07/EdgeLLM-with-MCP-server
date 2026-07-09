"""Gradio-based frontend for the Offline ASR system.

Replaces the JavaScript/HTML/CSS frontend with a pure-Python UI.
Calls the Whisper model manager directly (in-process, no HTTP needed).

Run standalone:
    python frontend/gradio_app.py

Or via the desktop launcher:
    python frontend/desktop.py
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Make project root importable regardless of where this is launched from
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

import gradio as gr  # noqa: E402

# ---------------------------------------------------------------- model glue
try:
    from models import get_model_manager  # noqa: E402

    _MODELS_AVAILABLE = True
except Exception as _exc:
    _MODELS_AVAILABLE = False
    _MODELS_ERROR = str(_exc)


def _model_info() -> dict:
    """Return a dict describing the current Whisper model."""
    if not _MODELS_AVAILABLE:
        return {
            "model_size": os.getenv("MODEL_SIZE", "small"),
            "device": os.getenv("DEVICE", "cpu"),
            "language": os.getenv("LANGUAGE", "en"),
            "model_loaded": False,
            "error": f"whisper not installed: {_MODELS_ERROR}",
        }
    return get_model_manager().get_model_info()


def _model_info_md() -> str:
    """Format model info as a Markdown table for display."""
    info = _model_info()
    rows = [
        ("Model", info.get("model_size", "?")),
        ("Device", info.get("device", "?")),
        ("Language", info.get("language", "auto")),
        ("Loaded", "✅ Yes" if info.get("model_loaded") else "⏳ On first use"),
    ]
    if info.get("error"):
        rows.append(("Status", f"⚠️ {info['error']}"))
    md = "| Property | Value |\n|----------|-------|\n"
    md += "\n".join(f"| {k} | {v} |" for k, v in rows)
    return md


# ------------------------------------------------------------ transcription
SUPPORTED_FORMATS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".webm"}


def transcribe(audio_path: str | None) -> tuple[str, str, str]:
    """Core transcription function.

    Args:
        audio_path: Path to the audio file (from mic or upload).

    Returns:
        (transcript_text, language_chip, meta_line)
    """
    if audio_path is None:
        return (
            "No audio provided. Record via microphone or upload a file.",
            "—",
            "",
        )

    suffix = Path(audio_path).suffix.lower()
    if suffix not in SUPPORTED_FORMATS:
        return (
            f"Unsupported format '{suffix}'.\n"
            f"Allowed: {', '.join(sorted(SUPPORTED_FORMATS))}",
            "—",
            "",
        )

    started = time.perf_counter()

    if _MODELS_AVAILABLE:
        manager = get_model_manager()
        model = manager.load_model()
        result = model.transcribe(
            audio_path, language=manager.language or None
        )
        text = (result.get("text") or "").strip() or "(no speech detected)"
        detected = result.get("language", manager.language or "auto")
        segments = result.get("segments") or []
        duration = float(segments[-1]["end"]) if segments else 0.0
    else:
        size_kb = Path(audio_path).stat().st_size / 1024
        text = (
            f"[stub] Received {size_kb:.1f} KB of audio.\n"
            "Install openai-whisper (pip install -r requirement.txt) "
            "for real transcription."
        )
        detected, duration = "en", 0.0

    elapsed = time.perf_counter() - started
    meta = f"{duration:.1f}s audio · {elapsed:.2f}s processing"
    return text, detected, meta


# --------------------------------------------------------------- Gradio UI

CUSTOM_CSS = """
/* ---- Dark glassmorphism theme overrides ---- */
:root {
    --body-background-fill: #0d0b1e !important;
    --background-fill-primary: rgba(255,255,255,0.06) !important;
    --background-fill-secondary: rgba(255,255,255,0.04) !important;
    --block-background-fill: rgba(255,255,255,0.08) !important;
    --block-border-color: rgba(255,255,255,0.15) !important;
    --block-label-text-color: #f5f7ff !important;
    --body-text-color: #f5f7ff !important;
    --body-text-color-subdued: rgba(245,247,255,0.62) !important;
    --input-background-fill: rgba(0,0,0,0.22) !important;
    --input-border-color: rgba(255,255,255,0.12) !important;
    --border-color-primary: rgba(255,255,255,0.15) !important;
    --color-accent: #8a5cff !important;
    --color-accent-soft: rgba(138,92,255,0.18) !important;
    --button-primary-background-fill: linear-gradient(135deg, rgba(255,77,157,0.9), rgba(138,92,255,0.9)) !important;
    --button-primary-text-color: #fff !important;
    --button-primary-border-color: rgba(255,255,255,0.25) !important;
    --shadow-drop: 0 10px 40px rgba(0,0,0,0.35) !important;
}

.gradio-container {
    max-width: 900px !important;
    margin: auto !important;
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif !important;
}

/* Glass card effect on Gradio blocks */
.gr-group, .gr-box, .gr-panel, .gr-block {
    backdrop-filter: blur(22px) saturate(150%) !important;
    -webkit-backdrop-filter: blur(22px) saturate(150%) !important;
    border-radius: 20px !important;
}

/* Animated background blobs (pure CSS) */
.gradio-container::before,
.gradio-container::after {
    content: "";
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.3;
    mix-blend-mode: screen;
    z-index: -1;
    animation: drift 22s ease-in-out infinite;
}
.gradio-container::before {
    width: 40vmax; height: 40vmax;
    background: #8a5cff;
    top: -10%; right: -10%;
}
.gradio-container::after {
    width: 35vmax; height: 35vmax;
    background: #ff4d9d;
    bottom: -10%; left: -5%;
    animation-delay: -8s;
}

@keyframes drift {
    0%,100% { transform: translate(0,0) scale(1); }
    33%     { transform: translate(6%, 8%) scale(1.12); }
    66%     { transform: translate(-7%, -5%) scale(0.94); }
}

/* Brand header */
#brand-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
}
#brand-header .brand-dot {
    display: inline-block;
    width: 14px; height: 14px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ff4d9d, #8a5cff);
    box-shadow: 0 0 14px #ff4d9d;
}
#brand-header h1 {
    font-size: 20px;
    font-weight: 600;
    letter-spacing: 0.4px;
    margin: 0;
    color: #f5f7ff;
}

/* Language chip */
.lang-chip {
    display: inline-block;
    font-size: 13px;
    padding: 4px 12px;
    border-radius: 999px;
    background: rgba(37,230,208,0.15);
    color: #8ff5ea;
    border: 1px solid rgba(37,230,208,0.35);
    font-weight: 600;
}

/* Meta line styling */
.meta-text {
    font-size: 13px;
    color: rgba(245,247,255,0.62);
}

/* Transcript output area */
#transcript-output textarea {
    font-size: 16px !important;
    line-height: 1.6 !important;
    min-height: 180px !important;
}

/* Engine info card */
#engine-info {
    font-size: 14px;
}
"""


def build_ui() -> gr.Blocks:
    """Build and return the Gradio Blocks UI."""
    with gr.Blocks(
        title="ASR Voice Console",
    ) as app:
        # ---- Header ----
        gr.HTML(
            '<div id="brand-header">'
            '  <span class="brand-dot"></span>'
            "  <h1>ASR&nbsp;Voice&nbsp;Console</h1>"
            "</div>"
        )

        with gr.Row(equal_height=False):
            # ---- Left column: transcript panel ----
            with gr.Column(scale=3):
                gr.Markdown("### 🎙️ Transcript")

                audio_input = gr.Audio(
                    sources=["microphone", "upload"],
                    type="filepath",
                    label="Record or upload audio",
                    show_label=True,
                )

                transcribe_btn = gr.Button(
                    "✦  Transcribe",
                    variant="primary",
                    size="lg",
                )

                transcript_out = gr.Textbox(
                    label="Transcription",
                    lines=8,
                    max_lines=20,
                    interactive=False,
                    buttons=["copy"],
                    elem_id="transcript-output",
                    placeholder="Tap Record and speak — or upload an audio file.\n"
                    "The offline Whisper engine transcribes it locally\n"
                    "and the text appears here.",
                )

                with gr.Row():
                    lang_out = gr.HTML(
                        '<span class="lang-chip">auto</span>',
                    )
                    meta_out = gr.HTML(
                        '<span class="meta-text"></span>',
                    )

            # ---- Right column: engine info ----
            with gr.Column(scale=1, min_width=240):
                gr.Markdown("### ⚙️ Engine")
                engine_info = gr.Markdown(
                    value=_model_info_md(),
                    elem_id="engine-info",
                )
                refresh_btn = gr.Button("↻ Refresh", size="sm")

        # ---- Event wiring ----
        def on_transcribe(audio_path):
            text, lang, meta = transcribe(audio_path)
            lang_html = f'<span class="lang-chip">{lang}</span>'
            meta_html = f'<span class="meta-text">{meta}</span>'
            return text, lang_html, meta_html

        transcribe_btn.click(
            fn=on_transcribe,
            inputs=[audio_input],
            outputs=[transcript_out, lang_out, meta_out],
        )

        # Also transcribe when audio recording stops (auto-submit)
        audio_input.stop_recording(
            fn=on_transcribe,
            inputs=[audio_input],
            outputs=[transcript_out, lang_out, meta_out],
        )

        refresh_btn.click(fn=_model_info_md, inputs=[], outputs=[engine_info])

    return app


# ---------------------------------------------------------------- entry point
PORT = int(os.getenv("GRADIO_PORT", os.getenv("API_PORT", "8000")))


def launch(**kwargs) -> None:
    """Build the Gradio app and launch it."""
    defaults = dict(
        server_name="0.0.0.0",
        server_port=PORT,
        share=False,
        inbrowser=True,
        css=CUSTOM_CSS,
        theme=gr.themes.Base(
            primary_hue=gr.themes.colors.purple,
            secondary_hue=gr.themes.colors.pink,
            neutral_hue=gr.themes.colors.gray,
            font=gr.themes.GoogleFont("Inter"),
        ),
    )
    defaults.update(kwargs)
    app = build_ui()
    app.launch(**defaults)


if __name__ == "__main__":
    launch()
