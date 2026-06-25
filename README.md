# Asterozoa Research Suite

A Claude Code plugin with two skills for single-name investment work. **Research** runs primary-source-first equity/credit research on a ticker (EDGAR filings first, every claim source-tagged, ending in a stance-taking memo). **Build-model** produces an institutional-grade Excel valuation model for that same name (scenario toggles, debt schedules, SOTP, gated on a clean Excel recalc). Both start from primary EDGAR filings, not third-party summaries.

## Install

Either method works with **no GitHub account or SSH key**.

**Option A: From the Claude app (no commands).** Click the **+** next to the prompt box, choose **Plugins → Add plugin**, add a marketplace via **Sync via repo**, and paste this URL:

```
https://github.com/dombejar/asterozoa-research-suite.git
```

Then pick **asterozoa** in the plugin browser and install it.

**Option B: Three lines in Claude Code.** Run these inside a session:

```
/plugin marketplace add https://github.com/dombejar/asterozoa-research-suite.git
/plugin install asterozoa@asterozoa-research-suite
/reload-plugins
```

Either way, the three `/asterozoa:` commands are now available in every session.

## Commands

| Command | What it does | Example |
|---|---|---|
| `/asterozoa:research <ticker>` | Primary-source research on a name. Pulls EDGAR filings, IR materials, comps, and cap structure, tags every fact by source, and writes a stance-taking memo (bull / bear / why-now / risks). | `/asterozoa:research MNR` |
| `/asterozoa:build-model <ticker>` | Builds an institutional Excel model: scenario cases, per-instrument debt schedules, SOTP valuation with MOIC/IRR. Won't declare done until Excel recalcs with zero errors. | `/asterozoa:build-model CLF` |
| `/asterozoa:feedback` | Turns freeform notes about a run ("missed the 8-K", "too hedged", "add a downside case") into a categorized list of changes for the next run. | `/asterozoa:feedback the cap table was stale, use the latest 10-Q` |

## Prerequisites

**Research** needs only Claude Code and an internet connection. It works the moment you install the plugin. Nothing else to set up.

**Build-model** needs more, because it writes and recalculates a real Excel file:

- **macOS**
- **Microsoft Excel** installed (the final recalc/render runs through real Excel, not a Python library)
- A **Python environment with openpyxl**, which the plugin installs automatically the first time a session starts (no action needed from you)

If you only want research, you can ignore the model prerequisites entirely.

## What's in the package

| Path | Contents |
|---|---|
| `skills/securities-research/` | The research skill: primary-source ingestion, source-tier tagging, and the bull / bear / why-now synthesis framework. Driven by `/asterozoa:research`. |
| `skills/model-builder/` | The model skill: scenario architecture, debt schedules, SOTP valuation, and the recalc / audit delivery gate. Driven by `/asterozoa:build-model`. |
| `commands/` | The three slash commands above (`research`, `build-model`, `feedback`). |
| `examples/MNR-research/` | A finished research run (HTML + markdown memo + a verification log) showing the output shape and source-tagging. |
| `examples/FLL-model/render/` | Tab-by-tab PNG renders of a finished Full House Resorts model: the caliber reference for what build-model produces. |
| `examples/CLF-model/renders/` | Tab-by-tab PNG renders of a finished Cleveland-Cliffs model, for a different sector. |
| `docs/walkthrough.html` | A visual, click-through walkthrough of both skills end to end. Open it in a browser. |
| `docs/gate-chain-explainer.md` | Explains the delivery gates: why build-model refuses to call a model "done" until the recalc is clean. |

## Your first run

1. Pick a ticker you already know well.
2. Run `/asterozoa:research <that ticker>`.
3. Read the memo it produces, then open `examples/MNR-research/` to compare against a finished one.
4. When you want the numbers, run `/asterozoa:build-model <same ticker>`.
