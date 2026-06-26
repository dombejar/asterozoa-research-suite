#!/usr/bin/env bash
# bootstrap.sh — idempotently create venv + install openpyxl
# Called by SessionStart hook. MUST exit 0 always.
# POSIX/cross-shell safe: no brew/BSD-isms; handles python vs python3 (Windows).

set -euo pipefail

VENV_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.asterozoa-plugin-data}/venv"

# On Windows (Git Bash / MSYS) the Excel oracle drives Excel via COM, which needs
# pywin32 in the venv. macOS uses AppleScript (no extra dep); Linux has no oracle.
PKGS="openpyxl"
case "$(uname -s 2>/dev/null)" in
  MINGW*|MSYS*|CYGWIN*|Windows_NT) PKGS="openpyxl pywin32" ;;
esac

# Locate a Python 3 interpreter (python3 on Unix/macOS, python on Windows Git Bash).
if command -v python3 &>/dev/null; then
  PY=python3
elif command -v python &>/dev/null && python --version 2>&1 | grep -q "^Python 3"; then
  PY=python
else
  echo "[asterozoa] python3 not found — run /asterozoa:build-model and Claude Code will install it for you"
  exit 0
fi

# Resolve the venv interpreter path.
# Unix/macOS: bin/python3  |  Windows Git Bash: Scripts/python or Scripts/python.exe
_venv_py() {
  for p in "$VENV_DIR/bin/python3" "$VENV_DIR/bin/python" \
            "$VENV_DIR/Scripts/python3.exe" "$VENV_DIR/Scripts/python.exe"; do
    [ -f "$p" ] && { echo "$p"; return; }
  done
  echo ""
}

# Resolve the venv pip path.
_venv_pip() {
  for p in "$VENV_DIR/bin/pip" "$VENV_DIR/Scripts/pip.exe" "$VENV_DIR/Scripts/pip"; do
    [ -f "$p" ] && { echo "$p"; return; }
  done
  echo ""
}

if [ -d "$VENV_DIR" ]; then
  VENV_PY="$(_venv_py)"
  # Guard against a partial venv (dir present but openpyxl install failed).
  if [ -n "$VENV_PY" ] && "$VENV_PY" -c 'import openpyxl' &>/dev/null 2>&1; then
    echo "[asterozoa] venv already exists at $VENV_DIR — skipping"
    exit 0
  fi
  echo "[asterozoa] venv found but openpyxl missing — reinstalling"
fi

echo "[asterozoa] creating venv at $VENV_DIR ..."
$PY -m venv "$VENV_DIR" || { echo "[asterozoa] venv setup failed — continuing without it"; exit 0; }

VENV_PY="$(_venv_py)"
VENV_PIP="$(_venv_pip)"

if [ -n "$VENV_PIP" ]; then
  "$VENV_PIP" install --quiet $PKGS \
    && echo "[asterozoa] venv ready (openpyxl installed)" \
    || echo "[asterozoa] openpyxl install failed — continuing without it"
elif [ -n "$VENV_PY" ]; then
  "$VENV_PY" -m pip install --quiet $PKGS \
    && echo "[asterozoa] venv ready (openpyxl installed)" \
    || echo "[asterozoa] openpyxl install failed — continuing without it"
else
  echo "[asterozoa] venv setup failed — continuing without it"
fi

exit 0
