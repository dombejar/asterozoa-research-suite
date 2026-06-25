# Formula Grammar — exact patterns from the reference model

These are the formula idioms the reference workbook uses throughout. Use them verbatim-in-shape.
They are banker conventions: compact, auditable by eye, and they avoid nested IF sprawl.

## Style basics

- **Leading `=+`** on simple links and arithmetic (`=+Model!D119`, `=+E12/D12-1`). Cosmetic but
  consistent — match it.
- **Whole-column consistency**: a formula row is the SAME formula dragged across all period
  columns. Any column that breaks pattern is a red flag the auditor checks for.
- Cross-sheet links are plain (`=+Actuals!D12`) — color protocol (green font) marks them, not
  formula syntax.

## Scenario selection — CHOOSE + Live column (never scattered IFs)

Numbered scenario toggle (`'Key Assumptions'!$D$5` holds 1–4):

```
Live cell:    =CHOOSE($D$5, G18, H18, I18, J18)
```

Named case toggle (`$C$6` holds "Base"/"Bull"/"Other", enumerated in B9:C11 as name→index):

```
Live cell:    =CHOOSE(VLOOKUP($C$6, $B$9:$C$11, 2, FALSE), P16, U16, Z16)
```

Echoing the toggle on other tabs (self-identifying printouts):

```
C5 =+'Key Assumptions'!$D$5
D5 =VLOOKUP(C5, 'Key Assumptions'!$B$9:$C$12, 2, FALSE)      ' renders the scenario's name
```

Scenario case data lives in **parallel blocks** (horizontal blocks per case on driver tabs;
vertical stacked blocks per scenario on project tabs) with IDENTICAL internal structure so the
CHOOSE offsets stay constant. One scenario's block may alias another's
(`Z26 =+P26` — "Other" starts as a copy of Base, diverge only where it differs).

## Boolean multiplication instead of IF

Compact gates that read as math:

```
Covenant pass flag:        =(F112>F113)*1
Gate revenue on a flag:    =SUM(O16:O17)*(1+P56)*(P56>0)*(P55="Yes")
Zero-when-counterpart-on:  =+J16*(1+P26)*-((P17>0)-1)        ' -((x>0)-1) ≡ NOT(x>0)
```

`-((P17>0)-1)` evaluates to 1 when P17≤0 and 0 when P17>0 — used to shut off the Temp casino's
revenue in years the Permanent is live. Prefer these over IF when the gate is arithmetic.

## Growth/margin rows

```
yoy %:      =+IFERROR(E16/D16-1, "nm")
margin %:   =+IFERROR(D35/D16, "nm")
```

`"nm"` (not meaningful) is the divide-by-zero sentinel — never #DIV/0!, never 0.

## Period headers — EOMONTH chains

One seed date, everything else derived:

```
D7 = 2019-12-31              (hardcoded seed, blue)
E7 =EOMONTH(D7, 12)          (annual axis)
Q7 =EOMONTH(P7, 3)           (quarterly axis)
```

Label row beneath: `FY19 … FY24 | FY25E … FY29E` and `Q4'23 … Q3'25 | Q4'25E`. The `E` suffix
marks estimates. Forecast-year annual column = sum of its quarters where the quarterly axis covers
it: `J119 =SUM(U119:X119)` (annual FY25E = Q1–Q4'25). The estimated stub quarter is itself a
formula off prior-year same-quarter: `X119 =+T119*(1+X129)`.

## Date-driven day-count interest (debt schedules)

Interest must respect WHEN an instrument exists within the year. `$C$227` = repayment date,
`J$7`/`I$7` = period-end headers:

```
Days outstanding (repayment): =($C$227<=J$7)*($C$227>I$7)*($C$227-I7) + ($C$227>J7)*365
Days outstanding (borrowing): =IF(AND($C244<=K$7,$C244>J$7), K$7-$C244, IF($C244>K$7, 0, 365))
Cash interest:                =+F247*F254*F256          ' beginning balance × rate × toggle
                              (with day-count: balance × rate × days/365)
```

Rules: interest accrues on **beginning balance** (kills circularity); repayment/borrowing dates
come from Key Assumptions Live cells; a payment **toggle row** (0/1) sits beside the rate so a
refi scenario can switch an instrument's interest off without breaking the row structure.

Revolver extras:

```
Commitment fee:  =+F211*F219        ' availability × fee %
LC fees:         =+F206*F222
Availability:    =SUM(commitments, -LCs, -drawn)
```

Issuance costs: `=-F248*$C$251` (new borrowing × issuance %, as negative cash in CFF).

## Roll-forwards

```
Beginning balance:  =+I204            ' prior period's ending — ALWAYS a link, never re-derived
Ending balance:     =SUM(J202:J203)   ' beginning + net change
```

Every stock (cash, each debt instrument, leases) rolls this way. The rollup block re-links each
instrument's schedule lines (`=+F204`, `=+F232`, …) and SUMs — the rollup is the single source
the CFF/covenant sections reference.

## Check rows — the model audits itself

Adjacent to every line that should tie to reported data:

```
B25 "Check"   D25 =D24-Actuals!D120        ' model CFO − reported CFO  → must be ~0
B47 "Check"   D47 =D46-SUM(Actuals!D55:D56)' ending cash − reported cash+restricted → ~0
```

Checks live in HISTORICAL columns (where reported data exists). The audit script asserts every
row labeled "Check" evaluates to |x| < 0.5 ($M tolerance for rounding). Add a check row whenever
a computed line has a reported counterpart: CFO, ending cash, total revenue, Adj EBITDA, total debt.

## Valuation scenario-freeze pattern (advanced — know it, use deliberately)

The reference Valuation Summary shows ALL ramp cases side-by-side even though the Model computes
only the live one. Mechanism — intentional self-reference:

```
G13 =IF(AND($C$2=G$5, $C$3=G$6), SUM(Model!$N139:$N140, 0), G13)
```

When the live toggles match column G's stamped scenario/case (`G5`/`G6`), the cell pulls fresh
from Model; otherwise it KEEPS ITS LAST VALUE. Net effect: toggle through each case once and every
column latches its own number.

**In NEW builds, wrap the self-reference in `N()`:** `=IF($C$6=G$8, <pull>, N(G13))`. Before the
first latch, an uninitialized freeze cell evaluates as an empty string under iterative calc, and
bare `""` poisons every downstream multiplication with `#VALUE!`. `N()` coerces the pre-latch
state to 0; after the first sweep it's a no-op. (The reference workbook gets away without it only
because its cells carry latched values from prior saves.)

**Requires:** Excel → Preferences → Calculation → *Enable iterative calculation* (the recalc
script sets this). openpyxl preserves but cannot evaluate it; values update only inside real Excel.

**Trade-offs:** stale columns if assumptions change after the last sweep (mitigate: the scenario
sweep in `audit_model.py` re-toggles every combo as its final act, then saves); confusing to
auditors who don't know the pattern (mitigate: a note cell beside the table:
"columns latch via iterative calc — sweep all toggles after any change").

**Cold-open gotcha (field-tested 2026-06-11):** Excel adopts calculation settings from the FIRST
workbook opened in a session. Even with `iterate="1"` saved in the file's calcPr, a reader whose
Excel session started elsewhere gets a **circular reference warning on every open**. Never ship
the freeze pattern in a file an external reader (analyst, prospect, LP) will open cold.

**PREFERRED alternative — per-case live decomposition (zero circularity):** the driver tab's case
blocks are always computed regardless of the toggle, so build a small per-case cash walk there:
per-case CFO = case EBITDA + ΔWC − taxes − interest (interest, dev capex, and financing flows are
scenario-only — link them from the engine); per-case FCF = CFO − maint capex + scenario flows;
terminal cash = live FY-anchor cash + Σ per-case FCF; per-case net debt = scenario total debt −
per-case cash. Valuation columns then pull EBITDA and net debt per case directly — both columns
fully live in every state. Validated against the freeze pattern in the MRG demo: identical outputs
to 4 decimals, opens clean on any machine. (Second alternative: single live column + script-stamped
static scenario grid.)

## Returns math

```
MOIC:  =+G34/$E$34                  ' target price / today's price
IRR:   =G35^(1/4)-1                 ' MOIC^(1/years)-1 — horizon from the spec, NOT hardcoded 4
Yield: =YIELD(TODAY()+2, maturity, coupon, price, 100, 2)    ' Cap Structure, T+2 settle
```

## Hardcode policy

Hardcodes (blue) are legal ONLY for: (1) Actuals tab figures, (2) assumption drivers inside
scenario/case blocks, (3) current market data (price, shares, as-of quotes), (4) the period seed
date. Each carries a comment: `Source: <doc>, <date>, <locator>` (see actuals-ingestion.md).
EVERYTHING else is a formula. A number typed into the Model engine, Valuation Summary (except
multiples/dilution inputs), or a rollup is a defect.
