/* ============ ASR Voice Console — frontend logic ============
 * Talks to the FastAPI backend (server.py). When packaged as a
 * desktop app (desktop.py / pywebview) it is served from the same
 * origin, so API_BASE stays "".
 */
const API_BASE = "";

const $ = (id) => document.getElementById(id);
const transcript = $("transcript");
const statusPill = $("status-pill");
const statusText = $("status-text");
const langChip = $("lang-chip");
const meta = $("meta");
const micFab = $("mic-fab");

/* ---------------- status helper ---------------- */
function setStatus(kind, text) {
  statusPill.classList.remove("rec", "busy", "err");
  if (kind !== "idle") statusPill.classList.add(kind);
  statusText.textContent = text;
}

/* ---------------- transcript rendering ---------------- */
function showTranscript(data) {
  transcript.innerHTML = "";
  const p = document.createElement("p");
  p.className = "typed";
  p.textContent = data.transcript || "(no speech detected)";
  transcript.appendChild(p);
  langChip.textContent = data.language || "auto";
  const dur = typeof data.duration === "number" ? data.duration.toFixed(1) : "?";
  meta.textContent = `${dur}s audio · ${data.processing_time ?? "?"}s processing`;
}

function showError(html) {
  transcript.innerHTML = `<p class="placeholder">${html}</p>`;
}

/* ---------------- send audio to the backend ---------------- */
async function sendAudio(blob, filename) {
  setStatus("busy", "Transcribing…");
  const form = new FormData();
  form.append("file", blob, filename);
  try {
    const res = await fetch(`${API_BASE}/api/v1/transcribe`, { method: "POST", body: form });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    showTranscript(await res.json());
    setStatus("idle", "Ready");
  } catch (err) {
    showError(`Transcription failed: ${err.message}.<br>
      Is the backend running? Start it with <code>python server.py</code>.`);
    setStatus("err", "Error");
  }
}

/* ---------------- file upload ---------------- */
$("file-input").addEventListener("change", (e) => {
  const f = e.target.files[0];
  if (f) sendAudio(f, f.name);
  e.target.value = "";
});

/* drag & drop onto the transcript panel */
transcript.addEventListener("dragover", (e) => e.preventDefault());
transcript.addEventListener("drop", (e) => {
  e.preventDefault();
  const f = e.dataTransfer.files[0];
  if (f) sendAudio(f, f.name);
});

/* ---------------- microphone recording ---------------- */
let mediaRecorder = null;
let chunks = [];
let recording = false;

async function toggleRecord() {
  if (recording) { stopRecord(); return; }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    chunks = [];
    mediaRecorder.ondataavailable = (e) => e.data.size && chunks.push(e.data);
    mediaRecorder.onstop = () => {
      stream.getTracks().forEach((t) => t.stop());
      const blob = new Blob(chunks, { type: "audio/webm" });
      sendAudio(blob, "recording.webm");
    };
    mediaRecorder.start();
    recording = true;
    micFab.classList.add("rec");
    setStatus("rec", "Recording… tap to stop");
  } catch (err) {
    setStatus("err", "Mic blocked");
    showError(`Microphone unavailable (${err.message}). You can still use <b>Upload audio</b>.`);
  }
}

function stopRecord() {
  if (mediaRecorder && recording) mediaRecorder.stop();
  recording = false;
  micFab.classList.remove("rec");
}

micFab.addEventListener("click", toggleRecord);

/* ---------------- boot: ping backend + fill model card ---------------- */
(async () => {
  try {
    const r = await fetch(`${API_BASE}/api/v1/model-info`);
    if (!r.ok) throw new Error();
    const s = await r.json();
    $("mi-model").textContent = s.model_size ?? "?";
    $("mi-device").textContent = s.device ?? "?";
    $("mi-lang").textContent = s.language ?? "auto";
    $("mi-loaded").textContent = s.model_loaded ? "yes" : "on first use";
    setStatus("idle", "Ready");
  } catch {
    setStatus("err", "Backend offline");
    showError(`Cannot reach the API. Start the backend with <code>python server.py</code>
      (or <code>python frontend/desktop.py</code> which starts both).`);
  }
})();
