#!/usr/bin/env bash
# bootstrap.sh — idempotently create venv + install openpyxl
# Called by SessionStart hook. MUST exit 0 always.

set -euo pipefail

VENV_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.asterozoa-plugin-data}/venv"

if ! command -v python3 &>/dev/null; then
  echo "[asterozoa] python3 not found — run /asterozoa:build-model and Claude Code will install it for you"
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
