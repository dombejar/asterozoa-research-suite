# Research Loop

The five-phase loop from idea to exit. The loop here is the canonical Asterozoa securities-research loop (Sourcing to Deep Dive to IC Memo to Monitor to Exit), built around a primary-source-first ingestion order and a two-pass separation of background from angle.

```
1. SOURCING    idea generated, briefly scored, kept or killed
2. DEEP DIVE    primary-source-first ingestion + abbreviated one-tab model
3. IC MEMO      the investment angle compressed into a sized, trigger-tagged pitch
4. MONITOR      catalysts tracked, thesis decay scored, position re-sized
5. EXIT          triggered exit (thesis broken, target hit, opportunity cost)
```

Loops, not lines. A name in Monitor can fall back to Deep Dive when something material changes. A name killed in Sourcing can return next quarter when the setup shifts.

---

## The ingestion order (the method's process, in order)

The method is consistently primary-source first. The skill walks sources in this exact order, and every fact it surfaces carries a source-tier flag. Primary-vs-secondary flagging is the trust contract of the whole tool, not a nice-to-have. The core principle: flag where the skill is using a web search or incorporating material that is not as reliable.

1. **10-K business description (the grounding step, every time).** Start here before any number is touched. Pull the business description, segment definitions, property/asset descriptions, and risk factors. This establishes what the company actually is.

2. **Earnings transcripts + investor presentations.** Mined specifically for property-level / segment-level / unit-level data that does NOT show up in headline segment reporting. This is where granular operating data lives (in the FLL case, the per-casino EBITDA ramp paths). Treat transcripts and IR decks as the place to recover granular operating data, not just narrative color.

3. **Comparables table.** Built for two purposes: (a) valuation multiples, and (b) understanding STRUCTURAL differences from peers (owns-vs-leases its real estate, lease economics, capital intensity). The comp table is a structural-understanding tool as much as a multiples tool.

4. **Third-party research.** Supplementary ONLY. The analyst needs to know precisely when a number came from third-party research versus a primary filing. This tier gets flagged most aggressively.

5. **Cap-structure deep-dive.** Every debt security, amortization schedule, maturity ladder, covenants, call schedule. The last ingestion step and the one that feeds the credit/scenario work downstream. (FLL example: the 8.25% 2028 notes, issue history, taps, call price schedule, covenant baskets.)

---

## The source-tier taxonomy (the flagging discipline)

Every claim, number, and statement in the ingestion output carries an inline source tag. The default reading posture: **a number with no Tier-1 tag is suspect.**

- **TIER 1 -- PRIMARY (the trusted spine).** SEC filings (10-K, 10-Q, 8-K, DEF 14A, S-1, indentures), company-issued earnings-call transcripts, company investor presentations, regulatory filings (gaming-commission, court dockets), trustee/TRACE bond data. Pulled first; the default basis for every claim.
- **TIER 2 -- SECONDARY / SUPPLEMENTARY (used, flagged).** Third-party sell-side or buy-side research, data-vendor screens, news/wire reporting. Allowed in, but every fact sourced here gets an explicit secondary flag.
- **TIER 3 -- UNRELIABLE (flag loudest).** Web search, blogs, opinion. Web-search contamination is the key risk, so any web-search-derived fact must be visibly marked and never blended invisibly into a Tier-1 number.

**Inline tag convention:** `[10-K, p.X]`, `[Q1'26 call]`, `[IR deck]`, `[3rd-party: <name>]`, `[web search]`. The tag travels with the fact through every downstream pass so a synthesis point resting on a Tier-3 web fact is visibly weaker than one resting on a 10-K.

---

## Phase 1: Sourcing

A name enters the loop from a screen, a referral, a catalyst surface (refi event, maturity wall, management change, regulatory unlock), an earnings-call anomaly, or a peer that surfaced from an already-owned name. The method is micro-first: this is single-name selection, not broad screening.

**Sourcing output:** a one-page screen that answers, in three sentences, how the company makes money; whether liquidity looks binding (the deep-vs-light trigger, assessed early); whether there is a catalyst in a 12-18 month window; and one suspected variant view. If the variant view cannot be articulated after a first pass, kill the name. Pitching a name where your view matches consensus wastes a slot.

**The depth decision is made here.** Assess whether liquidity is binding (elevated net leverage, near-dated maturity wall, fragile cash from ops, a financing event that must clear in a window). Deep path if yes; light path if it is a steady grower with comfortable coverage and no binding maturity.

---

## Phase 2: Deep Dive (PASS 1 ingest + PASS 2 model)

This phase runs the first two of the three passes.

## Connector-auth check (Phase 2 gate)

Before ingestion begins, read the `--connectors` value from the Inputs block and configure the connector surface for this run.

**If `edgar-only` or `no-vendor`:** do not call any vendor MCP. Log `connector-active: [EDGAR, company-transcripts]` at the top of `ingestion.md`. Proceed directly to PASS 1 using EDGAR and company-issued transcripts/IR decks only.

**If `full-stack`:** iterate the priority list in order: Daloopa > Aiera > Moody's > FactSet > S&P Global > LSEG. For each connector, mark it as `authenticated` or `skipped`. Log at the top of `ingestion.md`:

```
connector-active: [list of authenticated connectors, always includes EDGAR]
connector-skipped: [list of unauthenticated connectors, if any]
```

The "do not call" rule: a skipped connector is never replaced with web search. If a connector is not authenticated, do not call it and do not substitute web search in its place. Silent absence is not acceptable because it hides data-provenance degradation.

### Containment: write every fetched source into the run folder

Before fetching any primary source, confirm the run-root folder exists (created in STEP 0 per the SKILL.md containment rule). Every filing, transcript, IR deck, comparable, and third-party document fetched in this pass is written into the matching subfolder of the run root:

- SEC filings (10-K, 10-Q, 8-K, indentures): `<run-root>/sec-filings/`
- Earnings-call transcripts and investor presentations: `<run-root>/earnings-calls/`
- Comparable company documents: `<run-root>/comparables/`
- Third-party research: `<run-root>/third-party/`

NEVER write a fetched primary source to the current working directory or to any parent directory. If a fetch step would write to cwd, redirect it explicitly into the appropriate subfolder. The run folder is the single container for every artifact this run produces.

### PASS 1: Ingest (the 8 background questions, source-flagged)

The skill reproduces these 8 standard background questions as the ingestion-pass deliverable so the artifact is recognizable inside any analyst's folder-per-company workflow:

1. Company overview
2. Industry
3. Mode / moat
4. Timeline
5. Cap structure
6. Management / board
7. Ownership
8. Financials

Every answer is grounded in the ingestion order above, and every fact carries its source tag. This pass produces BACKGROUND INFORMATION only. It does not produce a view. Keeping the view out of this pass is deliberate: the synthesis pass (Phase 3) reasons over this flagged base rather than re-fetching and re-contaminating.

### PASS 2: Model (abbreviated one-tab three-statement)

Build the abbreviated three-statement on a single tab: P&L to cash-flow bridge to cap-stack to scenario toggles. Adjusted EBITDA is the comparison currency for comps, but every EBITDA figure bridges back to cash from ops and cash-less-capex. Skip the full balance-sheet forecast, the full P&L line-item detail, and the intermediate DCF years. Full spec in `framework.md`.

On the deep path, the model adds the full cap-structure deep-dive, maturity ladder, covenant analysis, the scenario tree, and (when liquidity is binding) a liquidity-runway estimate. On the light path, the abbreviated P&L-to-cash plus a multiple is the whole model.

**Deep Dive output:** the source-tiered ingestion file plus the abbreviated one-tab model, both in the per-company folder, both committed to version control.

---

## Phase 3: IC Memo (PASS 3 synthesize, then compress)

The investment-angle synthesis pass runs here, AFTER ingestion completes, as a distinct pass. It consumes the source-tiered background and the model and produces the opinion layer: bull case, bear case, why-now, the variant view ("where do you most see the model break"), and ranked key risks. The source tiers travel with every claim. Full spec in `output-templates.md`.

The synthesis is then compressed into the IC memo (the canonical structure: recommendation, thesis, business, variant view, catalysts, valuation, risks, sizing, exit triggers, appendix) and the 6-8 line chat elevator that actually gets read. Exit triggers are operational and named, written at memo time, so Phase 4 is actually doable.

**IC Memo output:** the synthesis file, the IC memo, and the chat elevator.

**--mode dispatch note:** After PASS 3 synthesis completes, dispatch to the `Output-length mode dispatch` table in `reference/output-templates.md` to render the correct artifact. `--mode bullet` renders only the Artifact C content shape (6-10 lines, key insight as line 1, no headers). `--mode exec-summary` renders the condensed Key-Insights-first format (600 words maximum, Key Insights as the first rendered block). `--mode full` (default) renders all three artifacts: Artifact A (investment-angle synthesis), Artifact B (IC memo), and Artifact C (chat elevator).

---

## Phase 4: Monitor

Per-print and quarterly. Track the named catalysts against their windows, score whether operational watch-fors moved in the direction the thesis required, and write a short thesis-decay note each quarter (intact / partially intact / broken, with the confidence delta). Once a quarter, deliberately go look for the bear case. On the deep path, the liquidity-runway and refi-clearing milestones are the load-bearing catalysts to track.

**Monitor output:** a quarterly thesis-update note per name plus a portfolio-level rollup of which names are decaying and which are strengthening.

---

## Phase 5: Exit

Three exit modes: triggered exit (a pre-defined operational trigger from the memo fires; honor it), target hit (re-underwrite at the new price or exit fully depending on whether the runway extended), and opportunity-cost exit (a better idea with higher expected return and similar risk). Be wary of the boredom exit, the anchor-on-cost-basis exit, and the catalyst-fatigue exit.

**Exit output:** a short exit memo (post-mortem) capturing what the trigger was and what the loop got right or wrong, for future reference.

---

## How the loop maps to the three passes

| Loop phase | Pass | Output |
|------------|------|--------|
| Sourcing | (pre-pass) | one-page screen + depth decision |
| Deep Dive | PASS 1 ingest + PASS 2 model | source-tiered ingestion file + one-tab model |
| IC Memo | PASS 3 synthesize | synthesis (the angle) + IC memo + chat elevator |
| Monitor | (re-runs PASS 3 lightly) | quarterly thesis-decay note + rollup |
| Exit | (post-mortem) | exit memo |
