# Asterozoa Brand Standards — Excel application

Palette sampled programmatically from the FLL thesis deck (Dec 2025, pixel census of the original
presentation). These are the house colors; `scripts/model_kit.py` encodes them as constants.

## Palette

| Name | Hex | ARGB | Deck usage |
|---|---|---|---|
| Asterozoa Charcoal | `#2E2E2E` | `FF2E2E2E` | Cover/divider backgrounds, dark header bands, body display text |
| Asterozoa Tan | `#CBBBA1` | `FFCBBBA1` | Brand accent: logotype, page titles, table header bands |
| Asterozoa Panel | `#EEEEEE` | `FFEEEEEE` | Light card/panel fill behind content blocks |
| White | `#FFFFFF` | — | Text on charcoal/tan bands; page ground |

Typography in the deck is a clean geometric sans (Montserrat-class) with wide letterspacing on
the logotype. In Excel stay with Calibri — the brand carries through color and structure, not font.

## Where flare goes in a model (tasteful — a model is a working document)

1. **Title block, every tab:** `B2` = `ASTEROZOA CAPITAL` in tan bold; `B3` = company name,
   charcoal bold; `B4` = tab purpose, charcoal; a **tan bottom-border rule** under the purpose row
   spanning the content width. (`model_kit.brand_title()`)
2. **DISCLAIMER tab:** charcoal title, standard fund disclaimer text (canonical copy lives in
   `model_kit.DISCLAIMER_TEXT`), tab color charcoal. (`model_kit.disclaimer_tab()`)
3. **Output-table header bands** (Valuation Summary column headers, Cap Structure header row):
   tan fill `FFCBBBA1`, white bold text — mirrors the deck's table style.
   (`model_kit.brand_band()`)
4. **Section banners on output tabs only** (optional): charcoal fill, white bold text — the deck's
   section-divider look. Engine/assumption tabs keep plain bold section labels (auditors live
   there; keep it quiet).
5. **Tab colors:** assumption tabs tan, engine/actuals neutral (no color), output tabs
   (Valuation Summary, Cap Structure) charcoal, DISCLAIMER charcoal.
6. **Footer stamp** (optional, output tabs): `ASTEROZOA CAPITAL — CONFIDENTIAL` in tan, small,
   below the last content row.

## What flare does NOT override

The working-cell protocol is untouchable: blue inputs / green links / black formulas, the
number-format grammar, check rows, and the near-white data grid all stay exactly per
`format-grammar.md`. Brand lives in titles, bands, and tabs — never in data cells. If brand and
auditability ever conflict, auditability wins.

## Confidentiality line

Prospect/LP-facing exports carry the deck's footer line:
`FOR INSTITUTIONAL INVESTOR USE. CONFIDENTIAL AND PROPRIETARY - DO NOT DISTRIBUTE WITHOUT PRIOR WRITTEN PERMISSION.`
Internal working models may omit it; anything leaving the building goes through
outbound-artifact-gate regardless.
