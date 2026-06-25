# Format Grammar — exact visual spec (counted from the reference workbook)

The model must LOOK like an Asterozoa model. These values were extracted programmatically from
the FLL Full House Resorts reference model (Dec 2025); the finished visual is illustrated by the
renders in `examples/FLL-model/render/`. `scripts/model_kit.py` encodes all constants — use it
rather than re-deriving styles.

## Font color protocol (the load-bearing convention)

| Font color | ARGB | Meaning |
|---|---|---|
| Blue | `FF0000FF` | Hardcoded input (actuals, assumptions, market data) |
| Green | `FF008000` | Cross-sheet link (`=+Actuals!D12`, `=+'Key Assumptions'!$E$20`) |
| Black / theme default | — | Same-sheet formula / calculation |
| Bold (any color) | — | Totals, subtotals, section headers, key outputs |

Reference-workbook census (audit_model.py re-checks this signature): blue cells are
overwhelmingly inputs (384 input vs 68 formula — the 68 are scenario-block aliases like `=+P26`,
acceptable: they're "input by reference"); green cells are overwhelmingly formulas (682 links).
A blue formula that is NOT a block alias, or a green hardcode, is a protocol violation.

## Number formats (verbatim strings)

| Use | Format string |
|---|---|
| Figures, $M (default everywhere) | `_(* #,##0_);_(* \(#,##0\);_(* "   -"?_);_(@_)` |
| Figures, one decimal | `_(* #,##0.0_);_(* \(#,##0.0\);_(* "   -"?_);_(@_)` |
| Percent, one decimal (growth/margin rows) | `* #,##0.0%;* \(#,##0.0\)%;* "   -"?_)` |
| Percent, two decimals (rates) | `* #,##0.00%;* \(#,##0.00\)%;* "   -"?_)` |
| Percent, whole | `* #,##0%;* \(#,##0\)%;* "   -"?_)` |
| Multiples | `* #,##0.0\x;* \(#,##0.0\)\x;* "   -"?_)` |
| Dollars (valuation per-share, cap structure) | `* "$"\ #,##0_);* "$"\ \(#,##0\);* """$"\ \ \-""?_);_(@_)` |
| Dollars, cents (price per share) | `* "$"\ #,##0.00_);* "$"\ \(#,##0.00\);* """$"\ \ \-""?_);_(@_)` |
| Dates (period headers) | `m/d/yy;@` |
| Yes/No flags | `"Y";"N";"N"` |

Grammar: negatives in parentheses, zeros render as aligned `-`, `$` only on valuation/cap-structure
sheets, everything space-aligned (`_(`/`* `). Numbers right-align by format; don't set alignment
manually.

## Fills

| Fill | ARGB | Use |
|---|---|---|
| Light yellow | `FFFFF2CC` | Scenario/case assumption blocks (the editable input zones) |
| Pale blue | `FFEBF3FB` | Occasional header banding |
| (most cells) | none | Formulas and labels sit on white |

The yellow fill is the visual "type here" signal — apply it to the full rectangle of each
scenario/case block on assumption tabs, NOT to Live columns (those are formulas).

## Sheet layout

| Element | Spec |
|---|---|
| Column A | Width **2.7** — left margin; also holds `x` markers on subtotal rows in bridge-support blocks |
| Column B | Labels — width 27–62 depending on tab (Model: 33.9, Actuals: 61.9, project tab: 44.4) |
| Column C | Secondary label / instrument terms column, ~9.7–13.9 |
| Spacer columns | Width 1.7–4.7 between time-axis blocks and between scenario case blocks (FLL: O between annual/quarterly, T/Y between case blocks) |
| Notes column | Far right, wide (Z on Model: 50.7; L on Key Assumptions) |
| Period columns | ~9.6–10.6 uniform |

Freeze panes per tab (freeze where labels meet data): Key Assumptions `E15`, P&L Ramp `D15`,
project tab `D9`, Model `D9`, Actuals `C6`. Valuation Summary and Cap Structure: none (fit on
one screen).

## Sheet header block (every tab)

```
B2  <Company Legal Name>            (bold)
B3  <Tab purpose>                   (bold; e.g. "Financial Model", "Key Assumptions")
B4  Live Scenario:   C4 =+'Key Assumptions'!$D$5   D4 =VLOOKUP(...)    (echo, where relevant)
B5  P&L Ramp Assumptions:  C5 ='Key Assumptions'!$D$6
B7  Period Ended:    <EOMONTH date row>
B8  ($ in Millions)  <FY/Q label row>               (units line, italic ok)
```

## Section structure

- Section titles in column B, bold (e.g. `P&L and Cash Flow Summary`, `Leverage and Covenants`,
  `Debt/Equity Schedule`) — top border or blank row above; no heavy fills on the Model sheet.
- Totals: bold, with top border (single) on the cells; `Total X` label.
- Check rows: label "Check" in B, value formatted as default figures; leave unformatted/unbolded
  (they should read as machinery, not output).
- Footnote markers: `(1)` suffix in labels, `Notes:` block at sheet bottom (Cap Structure).

## What NOT to do

- No conditional formatting, no data bars, no cell styles beyond the above.
- No merged cells anywhere in data regions (labels can span visually by overflow).
- No colors beyond the protocol (the anthropic 3-blues palette is for THEIR house style;
  Asterozoa's house style is the near-white grid above — match the reference, not the repo).
- No hidden rows/columns/sheets (auditor flags them).
- Tab color: none.
