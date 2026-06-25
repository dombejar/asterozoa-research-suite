# Debt Schedules & Scenario Architecture

The two systems that make these models institutional rather than spreadsheet-shaped: a scenario
architecture that turns the thesis's branch points into toggles, and per-instrument debt mechanics
with real dates from real documents.

## Scenario architecture

### Two orthogonal axes

1. **Financing/event scenarios** (numbered toggle, `Key Assumptions!D5`): the discrete *corporate
   actions* the thesis branches on. FLL's four: (1) no Permanent build — run out the Temporary;
   (2) incremental $325M financing by mid-26 + refi 2028 notes by YE27; (3) sale-leaseback funds
   the build; (4) full $800M refi at YE26 covering everything. Each scenario is a coherent WORLD,
   not a sensitivity: dates, amounts, rates, and Yes/No module flags all move together.
2. **Operating ramp cases** (named toggle, `Key Assumptions!D6`: Base/Bull/Other): how well the
   business performs within any world — growth rates and margins on the driver tab.

State space = scenarios × cases. The model computes ONE state at a time (the Live columns);
the sweep harness exercises all of them.

### Building the scenario set (spec phase)

- Read the thesis's "Key Issues/Risks" and "Catalysts" — each catalyst with a materially different
  capital-structure consequence is a scenario candidate. 3–5 scenarios; below 3 the toggle isn't
  earning its structure, above 5 the worlds blur.
- Scenario 1 should usually be the **no-action/downside world** (nothing gets financed, license
  lapses, run-off) — it anchors the asymmetry math.
- Every scenario gets a one-line description in the enumeration block (`B9:C12`) — these render
  on every tab via VLOOKUP, so write them tight.
- Ramp cases: Base = haircut to management targets (FLL Base cut management's $100M AP target to
  ~$90M); Bull = management delivers or beats; keep a third slot ("Other") aliased to Base until
  a real alternative case emerges — structure stays stable, content diverges later.

### Wiring rules

- EVERY scenario-varying assumption lives in Key Assumptions (or the project tab's scenario
  blocks) — never inline in the Model. The Model reads only Live cells.
- Yes/No flags gate whole modules (`Develop Permanent?` → project capex, new-build revenue,
  SLB lines all multiply by `(flag="Yes")`).
- Notes column carries the real-world constraint behind each assumption (call premium 102.063%
  until Feb 14 2026; CEO/CFO refi bonus deadline Mar 30 2027; "any date after 1/1/26 and before
  maturity 2/15/28") — the model documents its own reality checks.

## Per-instrument debt schedules

One block per instrument in the Model's Debt/Equity Schedule section. Instruments = everything in
the cap table TODAY plus every hypothetical instrument any scenario introduces (`New Financing - 1`,
`New Financing - 2` slots exist even in scenarios where they're zero — structure is
scenario-invariant, values vary).

### Block anatomy (per instrument)

```
<Instrument name>                          ' e.g. "8.25% Senior Secured Notes due 2028"
  Key dates row(s)      ← Key Assumptions Live cells (borrow/repay/extension dates)
  Amount row            ← Key Assumptions Live
  Beginning balance     =+<prior period ending>
  Borrowings/(repayments)   date-logic: amount lands in the period containing the date
  Ending balance        =SUM(beginning:net change)
  Issuance at premium/discount   =-borrowing × issuance% (cash cost, CFF line)
  Cash interest:
    Interest rate       ← Key Assumptions Live
    Days outstanding    date-driven day-count (see formula-grammar.md)
    Payment toggle      0/1 row
    Cash interest       = beginning balance × rate × days/365 × toggle
```

Revolver blocks add: commitments (with extension date), letters of credit, availability
(= commitments − LCs − drawn), commitment fee (= availability × fee%), LC fees.
Finance leases: simple roll-forward from Actuals (beginning/net change/ending), interest inside
opex per the filings.

### The rollup block

After all instrument blocks, a rollup that re-links every instrument's lines:

```
Beginning balance     (one row per instrument, =+ links to each block)   + Total
Borrowings/(repayments)  …                                               + Total
Ending balance        …                                                  + Total
Cash interest         …                                                  + Total
Issuance costs        …                                                  + Total
```

ONLY the rollup totals feed the rest of the model (CFF lines, leverage section, covenant tests).
This makes the dependency graph auditable: engine → rollup → instrument blocks → Key Assumptions.

### Mechanics rules

- Interest on **beginning balance** — no intentional circularity in the debt system (the only
  sanctioned iterative-calc use is the valuation freeze pattern).
- Repayment premium: capture in the repayment amount assumption (note documents the call
  schedule), not a separate engine line.
- A refinancing = repayment of instrument A + borrowing of instrument B in the same period, each
  in its own block; never net them.
- Quarterly columns matter here most — an Aug-2027 license expiry or Feb-2026 call-premium step
  is invisible on an annual axis.
- Negative ending balances are impossible by construction (repayment amount = the balance, from
  assumptions). If a cash sweep is ever modeled, cap with MIN(beginning balance, available cash).

## Covenants and leverage

- Leverage section: instruments (linked from rollup) → Total Debt → less cash → Net Debt →
  LTM Adj EBITDA → Net Debt/EBITDA.
- Covenant tests: read the ACTUAL credit agreement / indenture covenant (from the 10-K debt note
  or the filed agreement) and encode the real test. FLL's RCF: LTM Adj EBITDA must exceed the
  utilized RCF portion → `=(F112>F113)*1`. Boolean rows, one per covenant, labeled with the
  covenant's name.
- Liquidity block: cash + RCF availability = total liquidity — the going-concern line the IC
  reads first in stress scenarios.

## Capital-project module (when the thesis has a build)

Vertically stacked scenario blocks (identical structure) + CHOOSE Live block on top:

- Cost stack: site/earthwork, design/admin, hard costs, soft costs, funded contingency
  (~15% of hard), pre-opening (incl. cage cash for a casino). Footnote the budget as-of date.
- Phasing row: % of remaining spend per period (quarterly) — drives capex timing in CFI.
- Event rows: land-option exercise (CFI), SLB funding in/out (CFF), lease cap-rate → quarterly
  cash lease payments (`=-SUM(cumulative SLB funding)*cap_rate/4`) feeding a New-Lease EBITDA
  line in the P&L-by-property section.
- The module's Live outputs are what the Model engine links (`=+'AP Develop. Assumptions'!AA28`)
  — engine never reaches into scenario blocks directly.
