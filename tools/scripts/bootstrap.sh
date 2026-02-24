#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."

if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found. Install it first:"
  echo "  macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh"
  echo "  Windows PS : irm https://astral.sh/uv/install.ps1 | iex"
  exit 1
fi

echo "Creating/updating .venv and syncing workspace..."
uv sync

echo "Installing pre-commit hooks..."
uv run pre-commit install

echo "Done."
echo "Try: uv run ruff check . && uv run pytest"
