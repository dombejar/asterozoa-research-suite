# Asterozoa Research Suite: Quickstart

Audience: external analysts (no dev background assumed). Five sections. Read top to bottom once, then use the index to jump back.

---

## Index

1. [Get Claude Code](#1-get-claude-code)
2. [Install the plugin](#2-install-the-plugin)
3. [Model-side setup (macOS + Excel)](#3-model-side-setup-macos--excel)
4. [How to feed sources](#4-how-to-feed-sources)
5. [How to give feedback](#5-how-to-give-feedback)

For a full visual walkthrough, open `docs/walkthrough.html` in any browser.

---

## 1. Get Claude Code

Install the Claude Code CLI: https://claude.ai/download

One command confirms it is working:

```
claude --version
```

---

## 2. Install the plugin

Pick whichever is easier. **No GitHub account, SSH key, or terminal setup is needed for either.**

### Option A: From the Claude app (no commands)

1. Click the **+** button next to the prompt box.
2. Choose **Plugins → Add plugin**.
3. Add a marketplace and choose **Sync via repo**, then paste this URL:
   ```
   https://github.com/dombejar/asterozoa-research-suite.git
   ```
4. Find **asterozoa** in the plugin browser and install it.

### Option B: Three slash commands (Claude Code, any platform)

Inside a running session, run these in order:

```
/plugin marketplace add https://github.com/dombejar/asterozoa-research-suite.git
/plugin install asterozoa@asterozoa-research-suite
/reload-plugins
```

To confirm it worked, the three commands `/asterozoa:research`, `/asterozoa:build-model`, and `/asterozoa:feedback` are now available. (Optional terminal check: run `claude plugin list` and you will see `asterozoa@asterozoa-research-suite`.)

---

## 3. Model-side setup (macOS + Excel)

**Requirements:**

- **macOS** — the model builder drives Microsoft Excel via AppleScript for its recalc oracle. This is a hard macOS requirement; the model builder does not run on Linux or Windows. (The research skill, `/asterozoa:research`, is cross-platform and has no OS requirement.)
- **Microsoft Excel** installed locally (not just a browser)
- **Python 3** (see below if it is missing)

**What happens automatically:** When you start a Claude Code session, the plugin's bootstrap hook runs once in the background. It creates a Python virtual environment and installs `openpyxl` into it. You will see a one-line message:

```
[asterozoa] venv ready (openpyxl installed)
```

On subsequent sessions it silently skips because the environment already exists. You do not need to run any Python commands yourself.

**If python3 is missing:** The bootstrap hook will print:

```
[asterozoa] python3 not found — run /asterozoa:build-model and Claude Code will install it for you
```

When you run `/asterozoa:build-model`, Claude Code detects the missing Python, confirms with you once, and installs it automatically based on your OS:

- **macOS:** via Homebrew (`brew install python`), or the official Homebrew installer if Homebrew is absent.
- **Linux:** via your system package manager (`apt-get`, `dnf`, `yum`, `pacman`, or `zypper`).
- **Windows (Git Bash / WSL):** via `winget install Python.Python.3.12` or `choco install python`.

In every case you confirm once before anything installs. If you prefer to install manually, Python 3 is available at https://python.org/downloads; after that, start a new Claude Code session so the bootstrap hook completes.

**Why Excel is required:** `openpyxl` writes the workbook structure; Excel is required to open, recalculate, and render the final `.xlsx` output. The model gate will not declare a model complete until Excel recalc returns clean. Excel recalc uses AppleScript and requires macOS.

---

## 4. How to feed sources

### The default: EDGAR-first (no setup required)

The `/asterozoa:research` skill defaults to `edgar-only` mode. In this mode, it pulls SEC filings (10-K, 10-Q, 8-K, DEF 14A, indentures) and company-issued earnings transcripts directly from EDGAR. You do not need to download anything or point it at a folder.

To research a ticker in the default mode:

```
/asterozoa:research SNOW
```

The skill fetches the filings itself, works through three passes (ingest from primary sources, build an abbreviated model, synthesize the investment angle), and produces source-tagged output where every fact carries a tier label (Tier 1 = primary filing, Tier 2 = vendor/secondary, Tier 3 = web).

### Optional: point it at a local folder of filings or transcripts

If you already have filings, earnings call transcripts, or IR decks saved locally, you can pass the folder path and the skill will read from it in addition to EDGAR:

```
/asterozoa:research SNOW --folder ~/research/SNOW
```

The expected folder layout for a per-company directory:

```
SNOW/
  sec-filings/        10-K, 10-Q, 8-K, DEF 14A, indentures
  earnings-calls/     transcripts and investor presentations
  comparables/        comp table
  third-party/        sell-side or vendor research (will be flagged Tier 2)
```

Only the folders you have are needed. The skill fills gaps from EDGAR for anything missing.

### Optional: use financial data connectors

If you have financial-data MCP connectors authenticated (Daloopa, Aiera, Moody's, FactSet, and others), add `--connectors full-stack` to activate them:

```
/asterozoa:research SNOW --connectors full-stack
```

Connectors that are not authenticated are logged as skipped and never silently replaced with web search. Bloomberg is not part of this workflow by design.

### Output modes

The default output is an exec-summary. You can request more or less:

```
/asterozoa:research SNOW --mode bullet        # 6-10 lines, key insight first
/asterozoa:research SNOW --mode exec-summary  # condensed, Key Insights first (~600 words)
/asterozoa:research SNOW --mode full          # all three artifacts (ingest + model + synthesis)
```

---

## 5. How to give feedback

Use `/asterozoa:feedback` to turn freeform notes into structured next-run changes.

The command loads the feedback prompt, routes each complaint to a named Feedback Lever (FL1-FL5), and produces a categorized list of adjustments for the next run. It surfaces proposals for review and does not apply any changes automatically.

**Syntax:**

```
/asterozoa:feedback <your notes here>
```

**Worked example:**

```
/asterozoa:feedback Ticker: SNOW. Run date: 2026-06-25. Loop phase: Deep Dive. Artifact: synthesis.md. Section: variant view. The segment-level revenue split came from a sell-side note, not the 10-K. I need Tier-1 sourcing for that number.
```

The feedback prompt will identify this as an FL3 (source-tier discipline) issue, fill the four delta buckets (Correct, Corrected, Killed to real, Stays dead), and propose a durable update if the pattern should change the skill's default for this name class.

For the full feedback template and worked samples, see `skills/securities-research/reference/feedback-prompt.md`.

---

*For the full visual walkthrough of the model gate chain, open `docs/walkthrough.html` in any browser.*
