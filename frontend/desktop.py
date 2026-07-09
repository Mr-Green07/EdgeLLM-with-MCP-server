"""Run the ASR Voice Console as a DESKTOP APPLICATION.

    python frontend/desktop.py

What it does:
  1. Starts the FastAPI backend (server.py) in a background thread.
  2. Opens the glass-design UI in a native desktop window via pywebview.
     If pywebview is not installed, it falls back to opening the app in
     your default browser (functionally identical).

Install the native-window dependency with:
    pip install pywebview
"""
from __future__ import annotations

import os
import sys
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path

# Make project root importable regardless of where this is launched from
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from server import main as run_server  # noqa: E402

PORT = int(os.getenv("API_PORT", "8000"))
URL = f"http://localhost:{PORT}/"

WINDOW_TITLE = "ASR Voice Console"
WINDOW_SIZE = (1024, 720)


def _wait_for_backend(timeout: float = 30.0) -> bool:
    """Poll /health until the backend answers (model import can be slow)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{URL}health", timeout=1) as r:
                if r.status == 200:
                    return True
        except Exception:
            time.sleep(0.3)
    return False


def main() -> None:
    threading.Thread(target=run_server, name="backend", daemon=True).start()
    print("Starting backend...", flush=True)
    if not _wait_for_backend():
        print("Backend did not come up in time; window will retry on load.")

    try:
        import webview  # pywebview: native desktop window

        window = webview.create_window(
            WINDOW_TITLE,
            URL,
            width=WINDOW_SIZE[0],
            height=WINDOW_SIZE[1],
            min_size=(760, 560),
        )
        webview.start()          # blocks until the window is closed
    except ImportError:
        print("pywebview not installed -- opening in your default browser.")
        print("For a native window: pip install pywebview")
        webbrowser.open(URL)
        try:
            while True:          # keep the backend alive
                time.sleep(3600)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
