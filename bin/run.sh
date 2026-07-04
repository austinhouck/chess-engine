#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../apps/backend"
uv run python main.py
