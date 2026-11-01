# CLAUDE.md

## Project

Offline system-operations agent: a FastMCP server (`SystemOperatorServer`) exposes
five Windows/system tools, and a local GGUF LLM orchestrator discovers and calls
them over MCP. Package name `multi-orchestration-with-mcp-server`.

## Commands

Install (Python 3.12+):

```powershell
pip install -e .
# or
uv sync --all-extras --dev && uv pip install -e .
```

Run:

```powershell
python -m mcp_server.server                          # MCP server
python orchestrator/agent.py                         # CLI orchestrator
uv run uvicorn api.server:app --port 9000           # FastAPI wrapper
```

Test / lint / type-check (CI runs only these):

```powershell
uv run ruff check mcp_server --select E9,F63,F7,F82
uv run mypy mcp_server/ --ignore-missing-imports
uv run pytest -v tests/test_mcp_server.py
```

`pytest` config (`pyproject.toml`) ignores `tests/test_agent.py` and
`tests/test_metrics.py` and disables cacheprovider. Run full suite with
`uv run pytest` to include the rest.

## Layout

- Root-level modules imported as top-level: `config.py`, `security.py`,
  `tools.py`, `agent_controller.py`. They must stay importable from project root;
  tests insert the repo root into `sys.path` (see `tests/conftest.py`).
- `mcp_server/`: FastMCP server + tool implementations under `mcp_server/tools/`.
- `orchestrator/`: `agent.py` (orchestrator + GGUF model loading), `intent_classifier.py`, `rag_agent.py`.
- `api/server.py`: FastAPI wrapper; instantiates the orchestrator eagerly.
- Runtime data dirs created under repo root: `workspace/`, `documents/`, `indexes/`,
  `database/`, `logs/`, `models/`, `adapters/` (see `security.py`).

## Key facts / gotchas

- Model must exist at `models/Qwen3.5-4BQ/model.gguf`; `models/` is gitignored.
  Orchestrator refuses to start without it.
- Workspace jail root defaults to `~/AgentWorkSpace`, overridable via
  `WORKSPACE_JAIL_ROOT`. All FS access goes through `security.py` sandboxing;
  never bypass it or add raw `open()` on user paths.
- `tools.py` deliberately has no heavy deps; retrieval is injected through
  `ToolContext.retriever`. Keep it that way.
- Logging is forced to stderr (`config.py`).
- Ruff: line length 100, target py312; CI only checks critical errors
  (E9/F63/F7/F82), but full ruff uses E,F,I,UP.
- `Multi Agent Server/` is a separate Tauri frontend (Node); not part of Python
  tests/CI.
- On Windows, unset a stray `VIRTUAL_ENV` before `uv` commands if it points at
  another project.

## Environment

- `WORKSPACE_JAIL_ROOT` — workspace jail location.
- GGUF model path fixed relative to repo (see above).