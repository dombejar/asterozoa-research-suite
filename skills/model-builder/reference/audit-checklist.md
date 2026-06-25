# Audit Checklist — the delivery gate

A model ships only when ALL of this passes. Machine checks run via `scripts/audit_model.py` and
`scripts/recalc.py`; judgment checks are performed by reading the recalced workbook. Adapted from
anthropics/financial-services `audit-xls`, extended with this skill's check-row and scenario-sweep
requirements.

## Stage 1 — Recalc (machine, blocking)

`python3 scripts/recalc.py <model.xlsx>`

- Excel opens the file, enables iterative calculation (for the valuation freeze pattern),
  full-rebuild recalc, saves, and the script re-reads cached values.
- **Gate: zero error values** — no `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#N/A`, `#NUM!`
  anywhere. Every error is reported with sheet+cell. No acceptable-error list; `IFERROR(...,"nm")`
  exists precisely so legitimate div-by-zero never surfaces as an error.

## Stage 2 — Formula-level checks (machine)

| Check | Test |
|---|---|
| Check rows | Every row labeled `Check` evaluates to \|x\| < 0.5 in all populated columns |
| Hardcodes in calc zones | No constant cells in Model engine / Valuation computed rows / rollups (whitelist: labels, dates row seeds, blue-flagged inputs) |
| Hardcodes inside formulas | Flag `=A1*1.05`-style embedded constants (allow structural ones: `*365`, `/4`, `^(1/horizon)`, `*-1`, `(…)*1`) |
| Formula consistency | Within a formula row, period columns share the same shape (R1C1 comparison); breaks reported (estimate-stub columns like `X119` are expected breaks — flag for eyeball, not failure) |
| Color protocol | Constants without blue font in data regions; cross-sheet formulas without green font; blue formulas that aren't scenario-block aliases |
| Source comments | Every blue input on Actuals + market-data cells carries a `Source:` comment |
| Cross-sheet integrity | All references resolve (no `#REF!` — covered by recalc; openpyxl pass also catches dangling sheet names) |
| Hidden things | No hidden rows/columns/sheets |
| External links | None (no references to other workbooks) |

## Stage 3 — Model-integrity ties (machine, on recalced values)

| Tie | Test |
|---|---|
| Actuals gates 1–10 | The full tie-out table in actuals-ingestion.md |
| CFO check | Model CFO = Actuals CFO, historical columns |
| Cash check | Model ending cash = Actuals cash (+restricted), historical columns |
| Debt rollup | Rollup totals = sum of instrument blocks; leverage section = rollup |
| Quarterly bridge | Estimate-year annual = SUM(quarters) wherever both axes cover the year |
| Valuation foots | Segment EV = EBITDA×multiple; Total EV = sum; Equity = EV + net debt; price = equity/shares; MOIC = price ratio; IRR = MOIC^(1/h)-1 |
| LTM agreement | Valuation LTM EBITDA = Cap Structure LTM EBITDA |
| Cap Structure foots | Totals, net debt, EV, multiples columns recompute |

## Stage 4 — Scenario sweep (machine, the no-shortcuts centerpiece)

`python3 scripts/audit_model.py <model.xlsx> --sweep`

For EVERY financing-scenario × ramp-case combination:
1. Set both toggles via Excel scripting, recalc.
2. Assert zero error values in that state.
3. Record key outputs (Total EBITDA terminal year, Net Debt, Equity Value, Price/share, MOIC,
   covenant flags, minimum cash across forecast).
4. Assert outputs MOVE across states (a toggle nobody feels is miswired) and move in the right
   direction (Bull ≥ Base on EBITDA/price within each scenario; the no-action scenario shouldn't
   out-earn the build scenario by construction).
5. Flag any state with negative cash in any forecast period (financing hole) — not auto-fail,
   but must be a KNOWN result stated in the spec (e.g. "scenario 1 runs out of cash in FY28 —
   that's the point"), not a surprise.
6. Final act: re-toggle through all states once more, ending on the spec's default state, save —
   this refreshes the valuation freeze columns so no latched value is stale.

Sweep results print as a matrix; paste it into the build log / PHASE summary.

## Stage 5 — Judgment review (human/agent, reading the recalced workbook)

- [ ] Drivers vs history: forecast growth/margins read sane against the historical rows directly
      above them; any step-change traces to a thesis event (opening, refi, license)
- [ ] Scenario set matches the spec; each scenario's Notes column documents its real-world basis
- [ ] Covenants encode the actual credit-doc tests, not generic leverage ratios
- [ ] Multiples justified (comps in thesis); blended multiple sane vs where the name trades today
- [ ] Terminal-year EBITDA vs management targets: haircut documented (Base) or parity documented (Bull)
- [ ] MOIC/IRR pass the smell test for the thesis class (an "asymmetric upside" pitch with 1.3x
      Base MOIC isn't asymmetric)
- [ ] Every number in any paired deck/memo exists as a cell in the model (number-identity rule)
- [ ] Spec compliance: walk the MODEL-SPEC line by line — every required scenario, driver,
      instrument, event, and output exists and is wired
- [ ] File naming `<TICKER> Model.xlsx`; lands in the research folder for the name (one folder per company)

## Severity protocol (mirrors audit-xls)

- **Critical** (blocks delivery): recalc errors, failed check rows, failed ties, sweep errors,
  spec items missing.
- **Warning** (fix or justify in writing in the build log): formula-consistency breaks beyond
  expected stubs, color violations, missing comments, surprise negative-cash states.
- **Info**: style drift from format-grammar.md.

Zero criticals + zero unjustified warnings = ship. Then the **outbound-artifact-gate** skill
governs anything leaving the building (sends to Joe/Kevin/Jaron/prospects).
