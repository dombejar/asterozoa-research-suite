# Workbook Architecture — the 8-tab spec

The caliber anchor is Asterozoa's Full House Resorts model (Dec 2025). Its tab-by-tab renders are
in `examples/FLL-model/render/` (page_01.png through page_12.png). Every model this skill builds
follows the same architecture, adapted to the company. Tab names may change; the dependency graph
and the role of each layer may not.

## Tab order and dependency graph

```
DISCLAIMER          (static)
Key Assumptions     ──┐  master toggles + per-scenario capital-structure assumptions
P&L Ramp Assumptions ─┤  operating drivers by segment/property, per ramp case
<Project> Assumptions ┤  capital-project module (only if thesis has a build/event)   [situational]
Model               ◄─┘  THE ENGINE: cash-flow model + debt schedules + covenants
Valuation Summary   ◄──  SOTP off Model outputs; MOIC/IRR
Actuals             ◄──  as-reported filings data; everything anchors here
Cap Structure       ◄──  point-in-time instrument table off Actuals + market data
```

Reading order for a human = top to bottom. Build order = `Actuals` → `Key Assumptions` →
driver tabs → `Model` → `Valuation Summary` + `Cap Structure` → `DISCLAIMER`.

## Tab specs

### 1. DISCLAIMER
Single wide column (B, width ~200) of fund boilerplate. Copy Asterozoa's standard text from the
reference workbook. Always first tab.

### 2. Key Assumptions
The control room. Everything an investment-committee reader would toggle lives here.

- **Master scenario toggle** at `D5` (integer 1–N) — these are *financing/event scenarios*
  (e.g., FLL: 1=no build/run out temp, 2=incremental financing, 3=sale-leaseback, 4=full refi).
  Scenario descriptions enumerated right below in `B9:C12` so `VLOOKUP(D5, B9:C12, 2)` renders
  the live scenario's name anywhere.
- **Named ramp toggle** at `D6` (text: Base/Bull/Other) — *operating* cases, orthogonal to
  financing scenarios. N scenarios × M ramp cases = the full state space.
- **Assumption blocks** by capital-structure element (RCF, each existing note, each new financing,
  other): rows carry label (col B), **Live column** `E =CHOOSE($D$5, G, H, I, J)`, then one column
  per scenario (G:J), then a **Notes column** (L) carrying real-world constraints verbatim
  (call premium schedules, maturity dates, management incentive triggers, legislative dates).
- Per-scenario columns hold dates, amounts, rates, issuance costs — and Yes/No flags
  (e.g. `Develop Permanent?`) that gate whole modules downstream.

### 3. P&L Ramp Assumptions (driver tab)
Revenue and EBITDA build at the finest defensible unit — by property for an operator, by segment,
by product, by mine, whatever the company reports and the thesis turns on.

- Header: financing scenario + ramp case echoed from Key Assumptions (`=+'Key Assumptions'!$D$5`
  with the VLOOKUP'd name beside it) so a printout is self-identifying.
- Time axis: historical years (linked FROM `Model`, which itself links from `Actuals` — keeps a
  single chain of custody) + forecast years.
- **Live forecast columns** (K:N in FLL) = `CHOOSE(VLOOKUP($C$6,$B$9:$C$11,2,FALSE), P16, U16, Z16)`
  — selecting between **horizontal case blocks** laid side-by-side with spacer columns:
  Base (P:S), Bull (U:X), Other (Z:AC). Header row above each block names it.
- Drivers per unit: **yoy growth %** rows and **EBITDA margin %** rows. Historical growth/margin
  rows are computed (`=+IFERROR(E16/D16-1,"nm")`); forecast driver cells are blue hardcoded inputs
  inside the case blocks.
- Event gating by boolean multiplication, not IF: a new asset's revenue =
  `SUM(prior units)*(1+g)*(g>0)*(flag="Yes")` so a "No" in Key Assumptions zeroes the module.
- Corporate overhead = its own (negative) row in the EBITDA block.

### 4. Capital-project module (situational; FLL: "AP Develop. Assumptions")
Only exists when the thesis includes a discrete build/acquisition/event. Pattern:

- **Live block** at top: every line `=CHOOSE($C$4, <scenario1 row>, <scenario2 row>, …)`.
- **One full block per scenario stacked vertically below**, identical row structure, so the
  CHOOSE offsets are constant. Each block: cost categories (earthwork, design, hard, soft,
  contingency ~15% of hard, pre-opening incl. cage cash), total, quarterly/annual spend phasing
  (% of remaining spend per period), land-option exercise, sale-leaseback funding rows,
  lease cap-rate → cash lease payment math (`=-SUM($I53:K53)*$C55/4` per quarter).
- Footnote the budget's as-of date (`*Remaining construction budget as of 6/30/25`).

### 5. Model (the engine)
One long sheet, sections in this order. **Dual time axis**: annual columns (D:N, FY-h to FY+f)
AND quarterly columns (P:X) when intra-year events matter (license expirations, refis, openings).
Spacer column (O) between them; Notes column (Z, wide) at far right. Period headers are
`EOMONTH` chains off one seed date; label row beneath (FY19 … FY25E …, Q4'23 … Q4'25E).

Sections:
1. **P&L and Cash Flow Summary** — Revenue, yoy%, Adj EBITDA, margin, yoy% (linked from the
   P&L-by-property section below / Actuals for history). Then the **Adj EBITDA → CFO bridge**:
   `+ ΔWC + cash taxes + preopening&other + cash interest = Cash from operations`, with a
   **Check row** `=D24-Actuals!D120` (model CFO vs reported CFO) for historical columns.
   This is a *cash-first* model: EBITDA down to cash, NOT a net-income indirect build.
2. **CFI** — capex, land option (from project module), intangibles, asset sales, other → sum.
3. **CFF** — borrowings, repayments, revolver moves, SLB funding, equity, issuance costs → sum.
4. **Net cash flow → Beginning/Ending cash**, with Check vs Actuals.
5. **Liquidity** — cash + RCF availability.
6. **Bridge support blocks** — each non-EBITDA bridge line decomposed against Actuals lines
   (interest expense vs amortization-of-DIC vs accrued-interest change, tax expense vs payable vs
   deferred, D&A/SBC/disposals add-back pairs). Col-A `x` markers flag the subtotal rows the
   summary pulls. This is where reconciliation rigor lives.
7. **Leverage and Covenants** — debt by instrument (linked from schedules below), total, net,
   LTM EBITDA, Net Debt/EBITDA; covenant tests as boolean rows (`=(F112>F113)*1`).
8. **P&L by Property/Unit** — revenue, yoy%, EBITDA, margin%, yoy% per unit. History from
   `Actuals`/hardcoded quarterly estimates; forecast from the ramp tab's Live columns. The
   estimate-year annual column = `SUM(quarterly cols)` (e.g. `J119=SUM(U119:X119)`) so the
   forecast year is built from reported quarters + estimated stub.
9. **P&L by reporting segment** — regroups the same rows to match the company's segment reporting.
   Note: when a segment regroup block is built in addition to a property-level primary (the
   regroup mode), section 9 rows must be derived from section 8 property/unit rows via SUM
   formulas — they are never independently sourced from Actuals. When section 9 is built as the
   primary (segment-only companies with no property disclosure), rows may source from Actuals
   directly; note the data limitation in the Notes column.
10. **Debt/Equity Schedule** — ONE BLOCK PER INSTRUMENT (RCF, each note, each hypothetical new
    financing, finance leases): extension/repayment/borrowing dates (from Key Assumptions),
    beginning balance ← prior-period ending, borrowings/(repayments), ending balance,
    issuance premium/discount, **date-driven day-count interest** (see formula-grammar.md),
    payment toggles, commitment/LC fees for revolvers. Then a **rollup block**: beginning /
    borrowings / ending / cash interest / issuance costs, each by instrument with totals —
    these totals are what the CFF and covenant sections reference.
11. **Other Assumptions** — maintenance vs growth capex split, project capex, preopening,
    license fees and similar event costs (e.g. `=-50/6` with a note).

### 6. Valuation Summary
Sum-of-the-parts off the Model's terminal forecast year:

- Rows: EBITDA by valuation segment → Multiple by segment → EV by segment → Total EV →
  Net debt (from Model's forecast net debt — captures the deleveraging path) → Equity value →
  Shares (current + cumulative dilution assumption) → Price/share → **MOIC** (vs today's price)
  → **IRR** `=MOIC^(1/horizon)-1`.
- Columns: **Actual LTM** (sum of last 4 reported quarters from Model/Actuals) + one column per
  ramp case (Base/Bull/Other) at the projected year.
- Multiples are blue inputs per segment per case. Blended multiple = EV/EBITDA computed, not input.
- **Scenario-freeze pattern** (advanced, optional): each case column wraps its pulls as
  `=IF(AND($C$2=G$5,$C$3=G$6), <live pull from Model>, G13)` — a deliberate self-reference that
  LATCHES the value last computed when that case was live, so all case columns display
  simultaneously. Requires Excel iterative calculation ON. See formula-grammar.md for the
  trade-offs and the safer alternative.
- Dilution block at bottom: assumed equity-comp issuance, cumulative %, annual %.
- This table must be **number-identical** to the valuation page of any paired thesis deck.

### 7. Actuals
The ground truth. As-reported P&L, Balance Sheet, and Cash Flow statement — line-for-line with
the company's filings, no reclassification. Annual columns (FY-h…) AND quarterly columns for the
recent ~8 quarters. ALL values are blue hardcoded inputs (or EDGAR-scripted — still "input" in
color protocol) with source comments. Includes the company's own **Adjusted EBITDA reconciliation**
(net loss → adjustments → Adj EBITDA) exactly as disclosed. Everything upstream links here;
nothing here links anywhere.

### 8. Cap Structure
Point-in-time snapshot table (as-of date in header):

- One row per instrument: Amount, Price, Mkt Val, Interest (`=amount*rate`), Maturity, Rate,
  **Yield** (`=YIELD(TODAY()+2, maturity, coupon, price, 100, 2)`), Book & Market EBITDA multiples.
- Subtotals: secured / total debt; Less cash → Net debt; Market cap (price × shares, shares
  hardcoded with as-of note); Enterprise value. Multiples column = each level / LTM EBITDA.
- Operating metrics (LTM revenue/EBITDA from Actuals quarters), Liquidity block, Credit metrics
  (gross/net leverage), numbered footnotes for anything bespoke (rate floors, adjustments).

## Generalization map

**Universal (every model):** Actuals anchoring + check rows; Key Assumptions scenario architecture
(even if only 2 scenarios); driver tab at the unit the thesis turns on; cash-first engine
(EBITDA→CFO bridge) with per-instrument debt schedules whenever leverage matters; Valuation Summary
with MOIC/IRR; Cap Structure tab; dual time axis whenever an intra-year event matters.

**Situational (derive from the thesis):** capital-project module (build/acquisition);
**property/segment granularity** (decision tree: (1) If the company reports at the
property/unit level in its filings (e.g. individual casino properties, mine sites, stores),
build section 8 property-level primary and add a section 9 segment regroup only if the IC
reader needs the company's own segment view. (2) If the company reports only at the segment
level and individual properties are not disclosed, build section 9 segment-level primary and
note the data limitation in the Notes column. The decision must be declared in the MODEL-SPEC
before any cell is written.); covenant section contents (read the actual credit docs); SLB
mechanics; license/regulatory event costs; the scenario-freeze pattern.

**The left column is where alpha lives:** the scenario set and the driver decomposition ARE the
thesis. Before any cell is written, the MODEL-SPEC must state: which scenarios, which units, which
events, which instruments, what valuation method, what horizon — each traceable to the thesis
document or a filing.
