---
type: deliverable
status: active
created: 2026-06-24
modified: 2026-06-25
---

# The Model Gate, in Six Levels (T0 to T5)

A concise reference: how the offline model gate reads a workbook
and what it will not let ship. The long internal write-up (GATES.md, 46 gates) is the verification
artifact: this page is the map.

## What the gate is (and is not)

The gate is an **augmentation**, not a replacement for judgment. It runs after the model is built
and recalced, reads the `.xlsx` twice with openpyxl (the formula view and the cached-value view),
and runs 46 machine checks plus an optional render check. It never drives Excel and never touches
the network: every data source it relies on is fed in as evidence, and every source is swappable.

One rule governs the whole chain: **exit 0 is the only ship-eligible result.** Any block exits
nonzero. A run that is clean but not ship-eligible (for example, the offline two-file test shim used
outside test mode) exits 3 and prints `NON-SHIPPABLE`, never `CLEAN`.

## The six levels

The checks run in a fixed order, cheapest and most foundational first. A block at the environment or
config level stops the rest: there is no point footing the balance sheet if you cannot trust the
file you opened.

| Level | Question it answers | What it catches |
|---|---|---|
| **T0 Environment + config** | Are we running in the locked toolchain, and does the model declare its own shape? | Wrong Python, an undeclared sheet, a config that hides an output (empty or narrowed `outputs[]`). |
| **T1 Structure** | Is the workbook built the way the house standard requires? | External workbook links, hidden sheets, stray merged cells, conditional-format tricks, a structure that drifted from its baseline. |
| **T2 Values** | Did Excel actually recalculate, and do the cached numbers match their formulas? | A never-recalced file, a stale cache, error literals, a label stored as a formula, and the headline catch: an **output whose cached value drifted from what recalc produced even though the formula looks unchanged**. |
| **T3 Actuals tie-outs** | Do the financial statements foot and tie, re-derived from scratch? | Revenue/opex/EBITDA that do not sum, a balance sheet that does not balance, cash that does not tie, and a **mis-keyed row map pointing a subtotal at the wrong line**. |
| **T4 Scenario sweep** | Does the model behave across every scenario, not just the one on screen? | A dead toggle, a scenario that moves the wrong direction, a magnitude that barely moves, an error or a cash shortfall that only appears in an off-screen state. |
| **T5 Format + presentation** | Does it read as an institutional Asterozoa artifact? | Off-protocol cell colors, wrong number formats, a missing confidentiality stamp, a sheet that will not fit the page. |
| **Render (opt-in)** | Does the workbook actually render to a clean PDF? | A page count that does not match the visible sheets, a blank page, a layout that broke fit-to-width. |

## The two checks worth understanding

Two T2/T3 checks are the reason a wrong-but-pretty model cannot sneak through.

**Stale value, unchanged formula (T2).** The most dangerous defect is a cell that *looks* right: the
formula is the correct one, but the cached number next to it is old. The gate fingerprints both the
formula and the recalc-time *value* of every declared output. If the saved value drifts from what
recalc computed, it blocks, even when the formula is untouched. A missing value fingerprint fails
closed (block), never silent-pass.

**Mis-keyed row map (T3).** The gate never trusts a "Check" row inside the model. It re-sums the
statements itself from a declared row map. The row map could still point a subtotal at the wrong
line and foot green by accident, so the gate also verifies that each total row is *labeled* like the
total it claims to be ("Total assets" is on the assets-total row, not a member line). A row map that
lies is caught before the numbers are even added.

## How to run it

After building and recalcing a model, one command decides ship-eligibility:

```
"${CLAUDE_PLUGIN_DATA}/venv/bin/python3" "${CLAUDE_PLUGIN_ROOT}/skills/model-builder/scripts/model_gate.py" \
  "<TICKER> Model.xlsx" \
  --config <cfg.json> --recalc-evidence <recalc.json> --sweep-evidence <sweep.json> \
  [--render --rendered-pdf <render.pdf>]
```

- **Exit 0:** clean and ship-eligible.
- **Exit 3:** ran clean but not ship-eligible (do not ship; read the `NON-SHIPPABLE` line).
- **Any other nonzero:** that many blocks. The output names each gate and the exact cell.

The calibration suite behind the gate is 197 tests with zero skips: every gate has a passing case
and a blocking case, so a green run is a measured result, not a hope.
