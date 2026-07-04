#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../src/backend"
uv run python main.py
