---
name: securities-research
description: Ticker-in credit/equity research skill encoding an FTI-restructuring-trained, primary-source-first research framework. Runs primary-source-first ingestion (10-K to earnings transcripts/IR decks to comparables to third-party to cap-structure) with every fact carrying a source-tier flag, plus flagged secondary sources, plus a SEPARATE investment-angle synthesis pass (bull / bear / why-now / variant view / key risks / instrument read). Produces an abbreviated three-statement on one tab (P&L to cash-flow bridge to cap-stack to scenario toggles), trusts cash from operations over adjusted EBITDA, uses scenario toggles off one assumption block, runs a cap-structure deep-dive, and branches depth by liquidity (deep for distressed/stressed credits, light for clean ~10% compounders). Grounded in the Gatto (Credit Investor's Handbook) plus Greenwald (Value Investing/EPV-franchise) plus FTI restructuring lineage. Use when researching a single name end-to-end.
version: 0.2.0
modified: 2026-06-25
category: research
tags:
  - asterozoa
  - credit
  - securities-research
  - distressed
  - primary-source
  - ic-memo
---

# Securities Research

A ticker-in research skill built for single-name credit and equity work. Given a ticker, it runs three passes and produces a source-tiered background read, an abbreviated one-tab model, and an investment-angle synthesis: a clear analytical view on the security (mispriced or not, which instrument best expresses the view, what evidence would flip the read). The allocation decision belongs to the reader; the skill provides the analysis.

The spine of the whole skill is one architectural decision: **ingestion and synthesis are two separate passes.** Ingestion produces faithful, source-flagged background. Synthesis produces a view on top of it. Keeping them apart is what makes the view trustworthy.

## The three passes (the spine)

```
PASS 1  INGEST     primary-source-first, every fact source-tier-flagged
PASS 2  MODEL      abbreviated 3-statement on ONE tab, cash-from-ops over adjusted EBITDA
PASS 3  SYNTHESIZE the investment angle: bull / bear / why-now / variant view / key risks
```

1. **Ingest.** Walk sources in the primary-source-first order and flag every fact by source tier. Primary first, secondary supplementary and flagged, web/opinion flagged loudest. This pass reproduces the 8 standard background questions so the artifact is recognizable inside a folder-per-company workflow. Detail: `reference/research-loop.md`.

2. **Model.** Build the abbreviated three-statement on one tab: P&L to cash-flow bridge to cap-stack to scenario toggles. Adjusted EBITDA is the comparison currency for comps, but every EBITDA figure bridges back to cash from operations and cash-from-ops-less-capex. Skip the full balance-sheet forecast, full P&L line-item detail, and intermediate DCF years. Detail: `reference/framework.md`.

3. **Synthesize the angle.** Run AFTER ingestion completes, as a distinct pass that reasons over the source-tiered base (never re-fetching and re-contaminating). Produce the bull case, bear case, why-it-is-interesting / why-now, the variant view ("where do you most see the model break"), ranked key risks tied to the specific assumptions they would break, and the instrument read (which security is the right expression of the view). Take a clear analytical stance: commit to a view, name the falsifying data point. The reader makes the allocation decision. This is the most important output. Detail: `reference/output-templates.md`.

## When to go deep vs light (decide once, early, state it)

The method's rule: the same template over-engineers a clean compounder and under-serves a distressed name. Assess at ingestion time whether liquidity is the binding constraint.

- **GO DEEP (distressed / stressed credits where liquidity is binding).** Signals: elevated net leverage, a near-dated maturity wall, negative or fragile cash from ops, a financing event that must clear in a defined window. Add the full cap-structure deep-dive, maturity ladder, covenant analysis, the scenario tree, and liquidity-runway / recovery-by-seniority work. Cash from ops, the fully-banked number, is the whole game here.
- **GO LIGHT (clean compounders growing ~10%/year).** A simple P&L-to-cash valuation plus a multiple is enough. Do not build the scenario tree, do not over-elaborate the cap structure, do not run the liquidity-stress machinery. Over-modeling a clean compounder adds noise, not insight.

State the depth decision and its reason explicitly in the output so the reader knows which path was taken.

## Cross-cutting principles (preserve these)

1. **Two passes, kept separate.** Ingestion (faithful, source-tiered) and synthesis (the angle) are distinct. This separation IS the product.
2. **Primary-source-first, everything flagged.** Tier 1 primary is the spine; Tier 2 secondary is supplementary and flagged; Tier 3 web/opinion is flagged loudest and never blended invisibly into a primary number. This is the top principle of the method.
3. **Cash over EBITDA, always.** Adjusted EBITDA is management's currency (use it, do not trust it). Cash from ops and cash-less-capex is the truth. Every EBITDA-based output is paired with the cash bridge that validates it.
4. **One tab, abbreviated.** P&L to cash bridge to cap-stack to scenario toggles, single block. Skip the full balance sheet, full P&L detail, intermediate DCF years.
5. **Micro-first.** Single-name security selection. A macro overlay enters only when an assumption depends on it.
6. **Depth follows liquidity.** Deep for distressed/liquidity-binding; light for clean ~10% compounders.
7. **Portable folder structure.** Folder-per-company (SEC filings / earnings calls / comparables / third-party research) so the artifact drops into any analyst's folder-per-company workflow without a tooling change.

## Run folder (containment rule)

STEP 0 of every run: create exactly ONE run-root folder and keep everything inside it.

- If the user provided an existing folder-per-company directory, use that directory as the run root.
- Otherwise, create `<ticker>-research-<YYYY-MM-DD>/` in the current working directory as the run root.

ALL artifacts for the run live INSIDE that root, with no exceptions:

- Every fetched or downloaded filing, transcript, IR deck, comparable, and third-party document goes into the matching subfolder under the root: `sec-filings/`, `earnings-calls/`, `comparables/`, or `third-party/`.
- ALL output files (ingestion.md, model.md, synthesis.md, ic-memo.md, chat-elevator.md, or the artifact produced by `--mode`) go directly inside the root, not in a parent or sibling directory.
- NEVER write filings, raw sources, or output files to the current working directory or any parent directory. The run folder must be fully self-contained and portable.

The folder-structure diagram below shows the correct layout. The containment rule makes it mandatory, not optional.

## Folder structure (folder-per-company layout)

```
{ticker}/
  sec-filings/          10-K, 10-Q, 8-K, DEF 14A, S-1, indentures
  earnings-calls/       transcripts + investor presentations
  comparables/          comp table (multiples + structural differences)
  third-party/          sell-side / data-vendor research (Tier 2, flagged)
  ingestion.md          PASS 1 output: 8 background questions, every fact source-tagged
  model.md (or .xlsx)   PASS 2 output: abbreviated one-tab 3-statement
  synthesis.md          PASS 3 output: the investment angle
  ic-memo.md            compressed argument for the IC (when a name advances)
  chat-elevator.md      6-8 line chat summary
```

## Inputs

The skill accepts:
- A ticker (`FLL`, `SNOW`) as the primary entry point.
- A company name when the ticker is ambiguous.
- An existing folder-per-company directory to refresh or extend.
- A depth override (`--deep` / `--light`) when the analyst wants to force the path; otherwise the skill decides from the liquidity signals.
- `--mode <bullet | exec-summary | full>` (default: `full`): controls the rendering step at the end of PASS 3. `full` renders all three artifacts (preserves existing behavior). `exec-summary` renders a condensed Key-Insights-first format (600 words maximum). `bullet` renders the Artifact C content shape (6-10 lines, approximately 200 words, substantive key insight as line 1, no section headers). All three passes run in full for every mode; mode controls only what is rendered at the end. Detail: `reference/output-templates.md`.
- `--connectors <edgar-only | full-stack | no-vendor>` (default: `edgar-only`): controls which data connectors are activated. `edgar-only` (the default) uses EDGAR and company-issued transcripts/IR decks only, zero vendor MCP calls: the free, no-vendor path that runs with no connectors installed. `full-stack` is opt-in for analysts who already have financial-data MCP connectors authenticated; it adds EDGAR plus all authenticated connectors in priority order, and unauthenticated connectors are logged as skipped and never replaced with web search. `no-vendor` is an alias for `edgar-only` for environments with no MCP connectors configured. Bloomberg is not in the connector roster and is not a fallback path: this is a design constraint tied to the primary-source-first workflow. Detail: `reference/connectors.md`.

## Reference files (progressive disclosure)

Load on demand. SKILL.md stays scannable; the detail lives here.

- **`reference/research-loop.md`** -- the 5-phase loop (Sourcing to Deep Dive to IC Memo to Monitor to Exit) adapted to this method, with the exact ingestion order and the primary-vs-secondary flagging discipline. Now also documents the connector-auth check (Phase 2 gate) that reads `--connectors` and logs active/skipped connectors.
- **`reference/framework.md`** -- the abbreviated-three-statement-on-one-tab spec, the cash-from-ops-over-EBITDA trust rule, scenario-toggle modeling (including the refi-with-cash-out worked shape), what to skip, the deep-vs-light heuristic, and the Gatto / Greenwald / FTI lineage with source attributions.
- **`reference/output-templates.md`** -- the three output artifacts: the investment-angle synthesis (the gap the method targets), the IC memo canonical structure, and the chat-elevator summary. Now also documents the `--mode` dispatch table (bullet / exec-summary / full), the Key Insights first-line contract for exec-summary, and the FLL Worked Sample.
- **`reference/connectors.md`** -- the financial-services connector landscape for primary-source ingestion (EDGAR plus the financial-analysis MCP connector roster), which connectors fit the primary-first workflow, and the source-tier each one lands in. Now also documents the `--connectors` source-selection presets (edgar-only / full-stack / no-vendor) and the Bloomberg-absent design constraint.

## Extending the framework beyond securities (additive)

The two ingestion disciplines that make this skill trustworthy — source-tier flagging and the ingest/synthesize split — generalize past financial filings. When a name-in research task is about a **vendor, a founder, a collaborator, or a software system** rather than a security, apply the same spine with these adaptations.

### Metrics-as-signal: credibility assessment for vendors and systems

A surface metric (lines of code, GitHub stars, repo count, headcount, an impressive dashboard) is to a vendor/system what adjusted EBITDA is to an issuer: it is the **marketed currency, not the truth.** Treat it as a Tier-1-looking number that has not yet been validated, and run the cash-from-ops equivalent — a verification layer — before it enters synthesis.

When a codebase or product metric feeds a recommendation about a person or vendor, run these layers (the non-financial analogue of the cash bridge):

1. **Strip the dependency/generated mass first.** Exclude `node_modules`, build output, vendored and generated directories before measuring (e.g. `pygount --folders-to-skip=".git,node_modules,venv,.venv,dist,build,.next,vendor,third_party"`). Then separately inspect whether the *first-party* directories are themselves generated or template-hydrated. A big LOC number over generated code is the equivalent of an EBITDA add-back stack.
2. **Look for synthesis fingerprints.** Config files declaring target line counts, generator scripts, stochastic word banks, repetitive placeholder functions, fake org/team metadata, code bodies with no real side effects. Report these as **narrative/generated artifacts**, not hardened production systems — the same loud flag a Tier-3 web source gets.
3. **Run cheap maturity probes.** Count visible commits, look for tests, run the repo's own build/test commands if safe (Bash), note missing `tsconfig`, absent test files, or scripts that only print tool help. Do not infer private production quality from a public-repo failure; phrase it as **public-repo maturity evidence**, not a verdict on the company.
4. **Split product/UX signal from engineering-hardening signal.** A polished README, dashboard, or UI is genuine product and storytelling evidence; it is a *different axis* from whether tests, CI, typed builds, releases, and integration depth exist. Keep the two scored separately, exactly as the model keeps EBITDA (comp currency) separate from cash (truth).
5. **Report the delta.** The synthesis output states "claimed / marketed signal" vs "verified local-or-API signal" so the reader assigns trust deliberately. This is the credibility-assessment analogue of the bull/bear/variant-view pass: the delta itself IS the angle.

This does not replace the FTI framework for issuers; it is the parallel track for when the "name" is a system or a counterparty rather than a ticker. The cross-cutting principles (two passes kept separate; everything source-flagged; marketed-number distrusted until validated) hold unchanged.

### Disambiguate domain terminology via internal code-maps BEFORE external lookup

A short string that *looks* like a public ticker or a standard term may be an **internal code** that resolves only against your own glossary or fund/entity map. Resolving it as a public symbol contaminates ingestion with the wrong entity — a Tier-3 mistake wearing a Tier-1 mask.

The rule: when a token is ambiguous between "public market identifier" and "internal/private label," **resolve it against your own code-map first, then external sources.** Concretely:

- If you keep an internal glossary, memory store, or fund/entity code-map, search it for the token's meaning before any market-data or web lookup, and read the source it points to.
- **Private fund codes and internal abbreviations are internal-first.** A short string like a fund's two- or three-letter code can collide with a public ticker. Do not resolve a private-fund label, internal NAV/performance reference, or counterparty shorthand as a public ticker until your internal map either resolves it or confirms it is genuinely a public symbol.
- **Keep separate legal structures separate** — never blend the scope of two distinct entities; confirm which one a term belongs to before ingesting.
- Generalize the pattern: a fund code, a project alias, an internal ticker, or a counterparty shorthand all warrant a code-map check first. The external EDGAR / financial-data API / web lookup (WebSearch / WebFetch) happens only after the internal map either resolves the token or confirms it is genuinely a public symbol.

This sits at the front of PASS 1 (Ingest): disambiguate the entity before you start sourcing it, so every fact you tier-flag is about the right thing.

## Related

This skill encodes a primary-source-first, ingest-then-synthesize research method built for credit and special-situations work. The sibling `model-builder` skill in this plugin builds the number-identical Excel model the MODEL-SPEC feeds. Two cross-cutting disciplines it shares with adjacent research methods:

- **Source-tier discipline** — the same 3-tier evidence hierarchy (Tier 1 primary court/SEC/filing, Tier 2 vendor/wire, Tier 3 opinion/web) applies to any screening or adverse-signal lens, not just security selection.
- **Confidence follows where the evidence points** — scenario base cases and a falsifiable writeup keep conviction sized to the evidence; the credibility-delta synthesis (claimed vs verified) is the vendor/systems analogue.
- **Disambiguate the term before acting** — the front-of-ingest code-map check is the same reflex as surfacing unstated assumptions before locking a plan: confirm you are anchoring on the right entity and the current source before any external pass.

## Worked sample

Canonical mode renderings for FLL (Full House Resorts) live in `reference/output-templates.md` under `## FLL Worked Sample`. That section contains: one bullet rendering (6-10 lines, key insight as line 1), one exec-summary rendering (Key Insights block first, 600 words or fewer, FLL-specific), and one full-mode pointer. Do not reproduce the full sample text here; the canonical version in output-templates.md is the single source of truth to avoid divergence.

## Voice and constraints

- No em dashes in any prose output. Use periods, commas, or colons.
- Do not invent proper nouns (last names, affiliations, titles). Pull from filings or leave a placeholder.
- Mark unverified claims explicitly. A number with no Tier-1 tag is suspect by default.
- This skill encodes the METHOD, not the man. No personal or family detail belongs in any shipped artifact.
