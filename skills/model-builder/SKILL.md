---
name: asterozoa-model-builder
description: Builds institutional-grade Excel operating + valuation models to the Asterozoa house standard. The caliber target is illustrated by the FLL (Full House Resorts) example renders in examples/FLL-model/render/ — tab-by-tab PNG screenshots of a finished model. Scenario-first architecture (financing scenarios x ramp cases via CHOOSE/Live columns), actuals anchored to filings with tie-out check rows, per-instrument debt schedules with day-count interest, SOTP valuation with MOIC/IRR, Asterozoa branding. Delivery is hard-gated on real-Excel recalc (zero formula errors), machine audit, and a full scenario sweep. Use when building or extending a financial model for any name Asterozoa underwrites, or when a thesis deck needs its number-identical model sibling.
version: 0.1.0
category: research
tags:
  - asterozoa
  - financial-modeling
  - excel-openpyxl
  - scenario-analysis
  - valuation
  - debt-schedules
---

# asterozoa-model-builder

Build Excel models of the caliber shown in the FLL example renders (`examples/FLL-model/render/`)
— every time, no shortcuts. The Full House Resorts model (Dec 2025) is the caliber anchor; its
tab-by-tab PNG renders illustrate the finished layout, color protocol, and branding. The
conventions are distilled from that model plus Anthropic's financial-services modeling skills
(github.com/anthropics/financial-services).

## Hard rules (non-negotiable)

1. **Every calculation cell is a live formula.** Hardcodes only for: Actuals figures, assumption
   drivers in scenario/case blocks, market data, the period seed date — each with a `Source:`
   comment. A typed number in the engine, a rollup, or a valuation computed row is a defect.
2. **Color protocol:** blue font = input, green = cross-sheet link, black = formula, bold =
   totals/headers. Yellow fill marks scenario input blocks. (`reference/format-grammar.md`)
3. **Scenario architecture via CHOOSE + Live columns** — never scattered IFs. Financing scenarios
   (numbered) × operating ramp cases (named) are orthogonal toggles on Key Assumptions.
   (`reference/debt-and-scenarios.md`)
4. **Check rows are mandatory** wherever a computed line has a reported counterpart (CFO, ending
   cash, totals), and must evaluate ≈ 0. The model audits itself.
5. **No circular references in files external readers open cold.** The reference workbook's
   valuation freeze pattern is legacy — new builds use the per-case live decomposition.
   (`reference/formula-grammar.md`)
6. **Model ↔ thesis number identity:** any paired deck/memo quotes only numbers that exist as
   cells in the model.
7. **Delivery is BLOCKED until:** `scripts/recalc.py` reports zero formula errors in real Excel,
   `scripts/audit_model.py` reports zero criticals, the `--sweep` matrix runs clean across
   every scenario × case state, AND `scripts/model_gate.py` exits 0 (the single offline shipping
   gate). `model_gate.py` is a pure offline linter — it
   never drives Excel; it CONSUMES `recalc-evidence.json` + `sweep-evidence.json` (emitted by
   `recalc.py --emit-evidence` and `audit_model.py --sweep --emit-evidence`) and reads the
   recalced workbook twice with openpyxl. Exit 0 = ship-eligible. Exit 3 = ran clean but stamped
   non-shippable (e.g. unlocked env / two-file shim outside `--test`) — never read as green. Any
   nonzero exit blocks the send. Run any outbound-artifact provenance check you have before a send.

## PREFLIGHT (verify before you build)

Run this checklist before writing a single cell or kicking off MODEL-SPEC. If anything is missing, STOP and walk the user through installing it step by step. Do not silently proceed or fake-green a missing piece.

1. **Python 3 present.** Run `command -v python3`. If the command returns nothing, guide the user through installation:
   - Option 1 (Homebrew, recommended): `brew install python` (get Homebrew at https://brew.sh if it is not installed).
   - Option 2 (official installer): download from https://www.python.org/downloads/macos/ and run the .pkg.
   - Then ask the user to start a new Claude Code session so the SessionStart hook re-runs `scripts/bootstrap.sh` and creates the venv automatically.

2. **Plugin venv and openpyxl present.** The plugin venv lives at `${CLAUDE_PLUGIN_DATA:-$HOME/.asterozoa-plugin-data}/venv` (bootstrap.sh uses the same default). Check that `<venv>/bin/python3 -c 'import openpyxl'` succeeds. If not:
   - Run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/bootstrap.sh"` to create it, or
   - Install manually: `python3 -m venv "${CLAUDE_PLUGIN_DATA:-$HOME/.asterozoa-plugin-data}/venv" && <venv>/bin/pip install openpyxl`.
   - The venv is what gives `model_gate.py` the openpyxl it needs offline. Without it, the gate stamps the environment "unlocked" and the model is not ship-eligible.

3. **Microsoft Excel (macOS) present.** `recalc.py` and `audit_model.py` drive Excel via AppleScript for the live recalc oracle and the sweep matrix. Without Excel on this machine, STOP: do not proceed with deliverable model work. The only exception is if the user explicitly asks for a non-ship-eligible draft (e.g. a skeleton to hand off to a machine that does have Excel); state the limitation clearly and get explicit acknowledgment before continuing. openpyxl can write the file, but without real-Excel recalc and sweep evidence, `model_gate.py` will block and the model cannot be shipped.

## Workflow (phase gates — show work at each gate, don't build end-to-end)

1. **MODEL-SPEC.** Before any cell: write the spec — entity, thesis question, scenario set (3–5
   coherent worlds, scenario 1 = no-action), ramp cases, driver decomposition (the unit the
   thesis turns on), debt instruments with real terms/dates from the credit docs, capital
   projects/events, valuation method, horizon. Every item traceable to the thesis or a filing.
   Get Dom's sign-off. The build is audited against this spec.
   **granularity** (required declared choice): one of (a) property/unit-level primary — the
   default for companies that disclose individual property or unit data in their filings (e.g.
   individual casino properties, mine sites, stores); (b) reported-segment-level primary — for
   companies that report only at the segment level with no property-level disclosure; or (c)
   both — property-level primary with a segment regroup block added for the IC reader (see
   `reference/architecture.md` sections 8 and 9). For companies in category (a) or (c), segment
   regroup rows are always derived from property rows via SUM formulas; they are never
   independently sourced from Actuals.
2. **Actuals.** EDGAR-first (`scripts/edgar_pull.py`), as-reported line structure keyed from the
   filings, annual + recent quarterly, source comment on every cell. Gate: the 10 tie-outs in
   `reference/actuals-ingestion.md` (implemented as Check rows + `audit_model.py --actuals-only`).
3. **Key Assumptions.** Toggles, per-scenario capital-structure blocks, Yes/No module flags,
   Notes column carrying real-world constraints. Gate: toggle flips propagate.
4. **Driver tabs.** P&L ramp by unit (+ project module if the thesis has a build/event), case
   blocks side-by-side, per-case cash walk for the valuation. Gate: historical margins reconcile
   to Actuals; drivers match spec.
5. **Model engine.** EBITDA→CFO bridge, CFI/CFF, cash roll, liquidity, per-instrument debt
   schedules with day-count interest, rollup, covenants from the actual credit docs. Gate: all
   Check rows ≈ 0 in a real-Excel recalc.
6. **Valuation Summary + Cap Structure.** SOTP off the terminal year, MOIC/IRR, dilution; cap
   table with YIELD and book/market multiples. Gate: foots, ties, sanity
   (`reference/valuation-and-capstructure.md`).
7. **Audit + sweep + gate.** `recalc.py` → `audit_model.py --sweep` (every toggle combo; outputs
   must move and move sanely). Fix and re-run until CLEAN. (`reference/audit-checklist.md`) Then
   emit evidence and run the offline shipping gate:

   The three commands MUST run in this order (discovered in integration): **audit `--sweep`
   FIRST** (it re-saves the workbook), **THEN recalc** on the post-sweep file, **THEN
   `model_gate.py`** — otherwise the file-hash gate G21 blocks on a stale workbook.

   ```sh
   # PY is the plugin venv installed by the SessionStart bootstrap; falls back to
   # system python3 if the venv is absent (the gate then stamps the env "unlocked").
   PY="${CLAUDE_PLUGIN_DATA}/venv/bin/python3"; [ -x "$PY" ] || PY=python3

   # 1. sweep + emit sweep-evidence (this drives Excel and RE-SAVES the file last)
   "$PY" "${CLAUDE_PLUGIN_ROOT}/skills/model-builder/scripts/audit_model.py" \
       "<TICKER> Model.xlsx" --sweep \
       --config <model-config.json> --emit-evidence sweep-evidence.json
   # 2. recalc + emit recalc-evidence AFTER the sweep, so the evidence binds (sha256 +
   #    mtime) to the FINAL post-sweep workbook the gate will read (ordering matters:
   #    the sweep re-saves the file, which rebinds its hash + mtime — emitting
   #    recalc-evidence before the sweep makes G21 BLOCK on a stale/older file)
   "$PY" "${CLAUDE_PLUGIN_ROOT}/skills/model-builder/scripts/recalc.py" \
       "<TICKER> Model.xlsx" --in-place \
       --config <model-config.json> --canary "<a formula cell>" \
       --emit-evidence recalc-evidence.json
   # 3. run the gate (offline; consumes both evidence files; never drives Excel)
   "$PY" "${CLAUDE_PLUGIN_ROOT}/skills/model-builder/scripts/model_gate.py" \
       "<TICKER> Model.xlsx" \
       --config <model-config.json> \
       --recalc-evidence recalc-evidence.json --sweep-evidence sweep-evidence.json
   #    add --render --rendered-pdf <pdf> to also run the G70 render-verify gate
   ```

   Exit 0 = ship-eligible. Exit 3 = ran clean but NON-SHIPPABLE (do NOT ship). Any other nonzero
   exit = BLOCKED (resolve every finding, re-emit, re-run). Invoke through the interpreter
   (`"$PY" .../model_gate.py ...`), never bare `model_gate.py` (the source file is not marked
   executable). The `--config` is the per-model gate config the build scaffolds in step 0 (see
   "Gate config the build must emit" below): a JSON declaring `scenario_axes`, `outputs`,
   `expected_sheets` (every visible sheet → a role), `actuals_rowmap`, `min_cash_refs`,
   `covenant_flag_refs`. The build scaffolds this config (see "Gate config the build must emit"
   below); its full field-by-field shape is documented there.
8. **Deliver.** `<TICKER> Model.xlsx` → your research folder for the name (one folder per
   company). Run the outbound-artifact gate before any send.

## Toolchain (verified against the encoded format grammar and FLL example renders)

| Tool | Role |
|---|---|
| `scripts/model_kit.py` | openpyxl helpers: format grammar, brand layer, CHOOSE/Live blocks, period headers, check rows. Build with these — never restyle by hand. |
| `scripts/recalc.py` | Real-Excel recalc oracle (AppleScript). Zero-error gate. `--in-place` during builds; default is a temp copy. `--emit-evidence <path> --config <cfg>` writes `recalc-evidence.json` (workbook hash + canary + per-output formula/value fingerprints) for `model_gate.py`. |
| `scripts/audit_model.py` | Structure checks (color protocol, hardcodes, consistency, hidden things) + value checks (errors, Check rows) + `--sweep` scenario matrix via live Excel. `--sweep --emit-evidence <path> --config <cfg>` writes `sweep-evidence.json` (full-grid per-state outputs/min-cash/covenant + default-restored) for `model_gate.py`. |
| `scripts/model_gate.py` | The single OFFLINE shipping gate. Never drives Excel; consumes `recalc-evidence.json` + `sweep-evidence.json` and reads the recalced workbook twice with openpyxl (formula + cached views), running the full T0–T5 gate chain + the `--render` G70 render-verify gate. Exit 0 = ship-eligible; exit 3 = non-shippable; other nonzero = blocked. Run through the plugin venv (`"${CLAUDE_PLUGIN_DATA}/venv/bin/python3" scripts/model_gate.py`), system python3 as fallback. |
| `scripts/edgar_pull.py` | SEC XBRL companyfacts: scaffolds and cross-checks the Actuals tab. |

Environment: requires macOS with Microsoft Excel installed (the recalc/sweep oracle) and
openpyxl. Excel is the only evaluator trusted for delivery claims — openpyxl writes, Excel proves.

Python interpreter: the scripts run under the plugin venv created by the SessionStart bootstrap at
`${CLAUDE_PLUGIN_DATA}/venv/bin/python3` (openpyxl pre-installed there). If that venv is missing,
they fall back to the system `python3` (you must then have openpyxl on it); `model_gate.py` will
stamp the env "unlocked" when run outside a dedicated venv. Always invoke scripts by their
`${CLAUDE_PLUGIN_ROOT}/skills/model-builder/scripts/<name>.py` path so sibling-script resolution
(recalc → audit → model_gate) works regardless of your working directory.

### Gate config the build must emit (step 0 of the gate)

`model_gate.py` is not runnable without a per-model `--config` JSON, and the user should never have
to hand-write it. **Building a model SCAFFOLDS this gate config as part of delivery** — emit
`<TICKER>-model-config.json` next to the workbook, declaring:

- `expected_sheets` — every visible sheet mapped to its role (e.g. `engine`, `actuals`,
  `assumptions`, `valuation`, `output`); fail-closed role assignment, so unmapped sheets block.
- `actuals_rowmap` — the Actuals tab line labels mapped to their row coordinates (drives the T3
  tie-out gate).
- `outputs` — the cell refs of the headline outputs the gate value-checks (a non-empty list; an
  empty `outputs:[]` blocks because nothing can be value-gated).
- `scenario_axes` — the toggle cells + their valid states (drives the T4 sweep grid).
- `min_cash_refs`, `covenant_flag_refs` — the liquidity / covenant cells the sweep asserts on.

Scaffold the config from the model you just built: read the visible sheets, the Actuals labels,
the headline output cells, and the toggle cells straight out of the workbook. With the config
emitted at build time, the full gate chain (audit → recalc → model_gate) is runnable cold, with no
hand-written config required from the user. The MRG demo workbook
(generated by `examples/build-demo-model.py` into `examples/MRG-demo-output/`) is the reference build to scaffold a config against. Run `python3 examples/build-demo-model.py` to generate the workbook before inspecting it.

## Brand

Asterozoa charcoal `#2E2E2E` / tan `#CBBBA1` — title blocks, tan table bands on output tabs, tab
colors, branded DISCLAIMER first. Brand lives in titles and bands, never in data cells.
(`reference/brand-standards.md`)

## Worked example

`examples/build-demo-model.py` generates `examples/MRG-demo-output/MRG Model.xlsx` — a fictional
casino operator (Meridian Resorts Group) exercising every element: 3 financing scenarios × 2 ramp
cases, development module, day-count debt schedules, check rows, live two-case SOTP, branding.
Run `python3 examples/build-demo-model.py` to produce the workbook, then recalc and audit it per
the gate chain. Read it as the canonical model_kit usage pattern.

## Reference map (read on demand)

- `reference/architecture.md` — the 8-tab spec + generalization map (universal vs situational)
- `reference/formula-grammar.md` — `=+`, CHOOSE patterns, day-count interest, boolean gates,
  check rows, freeze-pattern lore + the live decomposition
- `reference/format-grammar.md` — exact fonts/fills/number formats/layout/freeze panes
- `reference/actuals-ingestion.md` — EDGAR pipeline + the 10 tie-out gates + source comments
- `reference/debt-and-scenarios.md` — scenario architecture + per-instrument debt mechanics
- `reference/valuation-and-capstructure.md` — SOTP/MOIC/IRR + cap structure tab
- `reference/audit-checklist.md` — the 5-stage delivery gate
- `reference/brand-standards.md` — palette + where flare goes

Related: the bundled `securities-research` skill (the research that feeds the MODEL-SPEC). Run any
outbound-artifact provenance check you have before sending a model to a stakeholder. The recalc /
sweep / gate chain proves the model is formula-correct; a separate visual design pass (house
grammar + headless render-verify) answers the distinct question of how it LOOKS.
