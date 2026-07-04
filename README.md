# Chess Engine

A chess engine — a pluggable search/evaluation core with an interactive CLI
and a FastAPI + Postgres API, plus a React frontend.

- `apps/backend/` — the engine, CLI, and API. See `apps/backend/README.md`.
- `apps/frontend/` — the web UI. See `apps/frontend/README.md`.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — manages the backend's Python environment, including downloading the pinned Python version
- [Docker](https://docs.docker.com/get-docker/) — for the API's Postgres database
- [Bun](https://bun.com) — for the frontend

## Setup

```
./bin/run.sh
```

This launches the interactive chess CLI; `uv` sets up the Python environment
on first run automatically, no manual `venv`/`pip install` step required.

For running the API server and database, see `apps/backend/README.md`. For
the frontend, see `apps/frontend/README.md`.
