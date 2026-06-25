---
description: Build an institutional valuation model for a ticker or company, gated on recalc-clean + audit CLEAN + model_gate exit 0.
---

Build a valuation model for: $ARGUMENTS

Load and follow the skill at ${CLAUDE_PLUGIN_ROOT}/skills/model-builder/SKILL.md.

Prerequisites (auto-installed by bootstrap.sh at session start):
- macOS
- Microsoft Excel (must be installed; openpyxl alone is not sufficient for final render)
- Python venv with openpyxl at ${CLAUDE_PLUGIN_DATA}/venv

Delivery gate — do NOT declare the model complete until ALL of the following pass:
1. Excel recalc returns 0 errors (no broken references, no #REF!, no #NAME?)
2. Audit CLEAN (all audit checks in the skill pass)
3. model_gate exits 0

Pass $ARGUMENTS through to the skill unchanged so the skill can parse ticker, date range, and any flags.
