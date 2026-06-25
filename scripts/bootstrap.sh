#!/usr/bin/env bash
# bootstrap.sh — idempotently create venv + install openpyxl
# Called by SessionStart hook. MUST exit 0 always.

set -euo pipefail

VENV_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.asterozoa-plugin-data}/venv"

if ! command -v python3 &>/dev/null; then
  echo ""
  echo "================================================================"
  echo " Asterozoa Research Suite: Python 3 not found"
  echo "================================================================"
  echo ""
  echo " The model-builder skill requires Python 3 to build and gate"
  echo " Excel models (openpyxl + audit scripts). The securities-research"
  echo " skill does NOT require Python 3 and works without it."
  echo ""
  echo " To install Python 3 on macOS, pick one option:"
  echo ""
  echo "  Option 1 -- Homebrew (recommended):"
  echo "    brew install python"
  echo "    (If Homebrew is not installed, get it at https://brew.sh)"
  echo ""
  echo "  Option 2 -- Official installer:"
  echo "    Download from https://www.python.org/downloads/macos/"
  echo "    Run the .pkg and follow the prompts."
  echo ""
  echo " After installing, start a new Claude Code session -- setup"
  echo " runs automatically on session start."
  echo "================================================================"
  echo ""
  exit 0
fi

if [ -d "$VENV_DIR" ]; then
  # Guard against a partial venv (venv dir present but openpyxl install failed).
  if "$VENV_DIR/bin/python3" -c 'import openpyxl' &>/dev/null 2>&1; then
    echo "[asterozoa] venv already exists at $VENV_DIR — skipping"
    exit 0
  fi
  echo "[asterozoa] venv found but openpyxl missing — reinstalling"
fi

echo "[asterozoa] creating venv at $VENV_DIR ..."
python3 -m venv "$VENV_DIR" \
  && "$VENV_DIR/bin/pip" install --quiet openpyxl \
  && echo "[asterozoa] venv ready (openpyxl installed)" \
  || echo "[asterozoa] venv setup failed — continuing without it"

exit 0
