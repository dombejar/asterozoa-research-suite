# Connectors: financial-services data for primary-source ingestion

How the skill sources the primary-vs-secondary tiers. The ingestion order (10-K to transcripts/IR decks to comps to third-party to cap-structure) needs data, and the data path determines which source tier each fact lands in. The discipline: a fact from a primary filing is Tier 1; a fact from a data vendor or sell-side note is Tier 2 and flagged; a fact from web search is Tier 3 and flagged loudest.

---

## Source-selection presets

Three named presets control which connectors the skill activates. Pass `--connectors <preset>` in the Inputs block; **default is `edgar-only`** — the free, no-vendor, no-Bloomberg path that needs zero connectors configured. The vendor presets are opt-in for analysts who already have those connectors authenticated.

**Bloomberg is not in the connector roster and is not a fallback path. This is a design constraint tied to the primary-source-first workflow, not a gap to be filled later.**

| preset | connectors active | source-tier ceiling | use when |
|--------|-------------------|---------------------|----------|
| `edgar-only` (DEFAULT) | EDGAR + company-issued transcripts/IR decks | Tier 1 throughout | The default. Zero vendor MCP calls required; fully Bloomberg-free, vendor-free path. The minimum viable configuration, and the only one that needs no connectors. |
| `full-stack` | EDGAR + authenticated connectors in priority order: Daloopa > Aiera > Moody's > FactSet > S&P Global > LSEG; unauthenticated connectors skipped and logged | Tier 1 for EDGAR/vendor-surfaced primary docs (filings, transcripts); Tier 2 for vendor analytics, consensus, ratings, and proprietary data | Opt-in. You have the financial-data MCP connectors authenticated and want them in priority order; unauthenticated ones are logged as skipped, never substituted with web search |
| `no-vendor` | Same as `edgar-only`; no authentication-check stub run | Tier 1 throughout | Alias for the default in environments with no MCP connectors configured |

### Preset definitions

**`edgar-only` (default):** EDGAR full-text search and filing retrieval plus company-issued earnings transcripts and IR decks. Zero vendor MCP calls. Every fact is Tier 1 by definition. This is the Bloomberg-free, vendor-free path and the minimum viable ingestion configuration. The skill runs fully on this preset with no connectors installed.

**`full-stack` (opt-in):** EDGAR (always) plus all authenticated connectors in priority order: Daloopa > Aiera > Moody's > FactSet > S&P Global > LSEG. Enable this only if you have those connectors authenticated. When a connector is not authenticated, it is marked `skipped` and logged explicitly in the ingestion-active log at the top of `ingestion.md`. Skipped connectors are never replaced with web search. The "do not call" rule applies: if a connector is not authenticated, do not call it and do not substitute web search in its place.

**`no-vendor`:** Alias for `edgar-only`. Intended for environments where no MCP connectors are configured. No authentication-check stub is run.

---

## The primary spine: EDGAR (free, Tier 1)

The default and the cheapest. SEC EDGAR full-text search and filing retrieval is the Tier-1 spine: 10-K, 10-Q, 8-K, DEF 14A, S-1, indentures. Every fact pulled here is Tier 1 by definition. The skill starts here for the 10-K business description (the grounding step) and the cap-structure deep-dive (indentures, note terms). For bond-level data, trustee filings and TRACE are Tier 1.

No connector is required to use EDGAR. When the financial-analysis connectors below are unavailable or unauthenticated, the skill still runs the full ingestion order off EDGAR plus the company's own earnings transcripts and IR decks (also Tier 1 when company-issued).

---

## The financial-analysis MCP connectors (optional)

These are optional third-party financial-data MCP connectors you may already have installed (e.g. via a financial-analysis plugin/connector bundle on a paid plan). They are activated only under the `full-stack` preset; the default `edgar-only` path ignores them entirely. Each connector is OAuth-gated. The roster below is identified by its real MCP endpoint hostname; authentication and entitlement are separate from availability.

### High fit (primary-source / credit-core)

- **Daloopa** (`mcp.daloopa.com`) -- granular, sourced fundamental data extracted from filings/decks, deep-history line items tied back to source. The best match to the method's primary-source ethos: line-item fundamentals traced to the source filing. Feeds the abbreviated one-tab three-statement and the cash-from-ops bridge. Because data ties back to the source filing, facts pulled here can be treated as Tier 1 when the underlying source is a primary filing, but cite the filing, not the vendor.
- **Aiera** (`mcp-pub.aiera.com`) -- earnings-call transcripts plus event audio/coverage. The cleanest connector for ingestion step 2 (transcripts + IR decks). Company-issued transcript content is Tier 1; vendor-added summaries are Tier 2.
- **Moody's** (`api.moodys.com/genai-ready-data`) -- proprietary credit ratings plus data on 600M+ public/private companies, built for credit analysis and compliance. The most credit-native of the set; serves the cap-structure / distressed deep-dive. Ratings and vendor analytics are Tier 2 (proprietary third-party); use them flagged.

### Medium fit (comps / supplementary, treat as secondary)

- **FactSet** (`mcp.factset.com`) -- company fundamentals plus sell-side analyst estimates/consensus. Useful for the comps table and the consensus side of the variant view. Lands in the Tier-2 supplementary bucket, flagged.
- **S&P Global / Kensho** (`kfinance.kensho.com`) -- Capital IQ tear sheets, fundamentals, funding digests, earnings-preview beta. Fast comps and tear sheets. Tier 2, flagged.
- **LSEG / Refinitiv** (`api.analytics.lseg.com/lfa`) -- fixed income, rates, FX, options analytics (pairs with the `lseg:` skill pack: bond relative value, swap curve, bond-futures basis, FI portfolio). Relevant only when a credit's bonds/rates exposure is material, i.e., the macro-overlay-only-when-material rule. Tier 2.

### Low / out-of-scope for long-credit/long-equity work

- **Morningstar** (`mcp.morningstar.com`) -- funds, ETFs, equities (retail-flavored).
- **PitchBook** (`premium.mcp.pitchbook.com`) -- PE/VC deal and private-company data.
- **Chronograph** (`ai.chronograph.pe`) -- PE portfolio monitoring / fund-level performance.
- **Egnyte** (`mcp-server.egnyte.com`) -- secure internal document repository connector (a firm's own files, not a market-data feed). Only relevant if Asterozoa standardizes a file repo.

---

## The recommended spine

Lean on **Daloopa + Aiera + Moody's** as the credit-primary spine (sourced line items, transcripts, credit/cap-structure), with **FactSet / S&P Global** slotted explicitly into the secondary/flagged tier (comps and consensus). This mirrors the primary-vs-secondary discipline the method is built on and the synthesis-pass gap it targets. EDGAR remains the free Tier-1 foundation under all of them.

| Connector | Ingestion step it serves | Default source tier |
|-----------|--------------------------|---------------------|
| EDGAR | 10-K grounding, cap-structure indentures | Tier 1 |
| Daloopa | Financials / one-tab model line items | Tier 1 (cite the filing) |
| Aiera | Transcripts + IR decks | Tier 1 (company-issued content) |
| Moody's | Cap-structure / credit deep-dive | Tier 2 (proprietary, flagged) |
| FactSet | Comps + consensus | Tier 2 (flagged) |
| S&P Global | Comps + tear sheets | Tier 2 (flagged) |
| LSEG | Bonds/rates, only when material | Tier 2 (flagged) |
| Web search | NOT a connector fallback; Tier 3 only when no Tier-1 or Tier-2 source exists and only with explicit loud flagging | Tier 3 (flag loudest) |

---

## Enabling the optional connector presets

The default path is `edgar-only`: no connectors, no vendor calls, every fact Tier 1. You never need to install anything to run the skill.

If you already have financial-data MCP connectors configured in your environment, switch to `--connectors full-stack` to fold them into ingestion in the priority order above. Each connector authenticates on its own (OAuth); unauthenticated ones are logged as `skipped` and never silently replaced with web search. The exact branding of any connector bundle you use depends on your provider and plan, so this reference identifies each connector by its MCP endpoint hostname rather than by a product name. Use whichever bundle your environment exposes; the per-provider source-tier mapping above holds regardless of the umbrella name.

---

## Operating rule when connectors are unauthenticated

If a financial-analysis connector is installed but not authenticated, do NOT silently fall through to web search for a number a primary filing would carry. Pull it from EDGAR (Tier 1) or the company transcript/IR deck (Tier 1). Web search is the last resort and any web-derived fact is flagged loudest. A number with no Tier-1 tag is suspect by default.

Under the `full-stack` preset: when a connector is unauthenticated, mark it as `skipped` and log it explicitly in `connector-skipped: [list]` at the top of `ingestion.md`. Do not call the connector and do not substitute web search. Under the `edgar-only` or `no-vendor` presets: no vendor MCP calls are made at all; log `connector-active: [EDGAR, company-transcripts]`.
