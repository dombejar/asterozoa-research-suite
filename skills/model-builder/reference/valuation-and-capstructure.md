# Valuation Summary & Cap Structure tabs

## Valuation Summary — SOTP with MOIC/IRR

The output tab. It must answer, on one screen: what is this worth in each case, what's the
multiple of money, and at what rate. It is also the tab that must be **number-identical** to the
valuation page of any paired thesis deck (FLL: deck page 5 = this tab, exactly — Base $11.72 /
Bull $28.71, MOIC 4.1x/10.1x, IRR 42.7%/78.5%).

### Structure (rows)

```
Header:    Financing Scenario + P&L Ramp echo (self-identifying)
Columns:   Actual LTM <Qx'yy>  |  Projected FY'<terminal>: Base | Bull | Other

EBITDA            one row per VALUATION segment (≠ reporting segment if thesis demands —
                  FLL: American Place / Bronco Billy's & Chamonix / Other Operations)
Total EBITDA      =SUM

Multiple          per segment per case — BLUE INPUTS, the analyst's judgment cells
Blended Multiple  =Total EV / Total EBITDA   (computed, sanity line)

Enterprise Value  per segment = EBITDA × multiple
Total EV          =SUM

Net Debt          ← Model's FORECAST net debt at the terminal year (this is the lever most
                  generic models miss: deleveraging path flows into equity value)
Equity Value      =EV + net debt (net debt carried negative)

Shares (mm)       = today's shares + assumed cumulative dilution
Price per share   =Equity / shares
MOIC              =target price / today's price
IRR               =MOIC^(1/horizon)-1

Dilution block:   assumed equity-comp issuance (mm sh), cumulative %, annual %
```

LTM column: sum of the trailing four reported quarters from Model quarterly columns
(`=SUM(Model!T138:W140)`); multiples/EV `n/a` for LTM except blended (= today's EV / LTM EBITDA,
which reads as the market's implied multiple — FLL: 11.6x on depressed EBITDA).

### Segment multiples discipline

- Multiples are inputs, justified in the thesis (comps, precedent transactions, quality tier).
  Different multiple per segment is the POINT of SOTP — a ramping flagship asset isn't worth the
  same turn as a declining river boat.
- Bull case may use higher multiples than Base ONLY with stated justification (de-risked story →
  multiple expansion); document in the deck, not just the cell.
- Keep a "no incremental value ascribed to X" list (FLL: Rising Star relocation optionality) —
  free upside stays out of the math and into the prose.

### Scenario display

Default for NEW builds: the **per-case live decomposition** (see formula-grammar.md) — both case
columns fully live via a per-case cash walk on the driver tab, zero circular references, opens
clean on any machine. The reference workbook instead uses the **scenario-freeze pattern**
(iterative calc + self-referencing IFs); understand it to read the reference, but don't ship it
in files external readers open cold — Excel sessions without iteration enabled throw a circular
reference warning on every open.

### Today's price / shares

Blue inputs with as-of comments (`Price per share as of 2025-12-10`, `Shares o/s as of 11/3/25
per 10-Q cover`). The deck footnotes the same dates.

## Cap Structure — point-in-time snapshot

Standalone tab, as-of date in the header row. The "where does it trade today" table for the IC.

### Columns

`Amount | Price | Mkt. Val. | Interest | Maturity | Rate | Yield | EBITDA Multiple (Book) | (Market)`

### Rows

```
One row per instrument:
  RCF             amount drawn; rate "SOFR + x%"; footnote floors/adjustments
  Each bond       amount; PRICE (market quote, blue input, as-of); mkt val = amount × price/100;
                  interest = amount × coupon; YIELD =YIELD(TODAY()+2, maturity, coupon, price, 100, 2)
  Finance leases  book + market estimate
Total Secured Debt / Total Debt        (sums; multiples = level / LTM EBITDA, book & market)
Less: Cash and Equivalents             (negative, blue)
Net Debt                               (multiples)
Market Cap        = shares × price     (raw share count + as-of note)
Enterprise Value  = net debt + mkt cap (book & market variants; multiples)

Operating Metrics:  LTM Revenue / LTM Reported EBITDA  =SUM of trailing 4 quarters from Actuals
Liquidity:          RCF commitments − drawn + cash = Total liquidity
Credit Metrics:     Gross leverage, Net leverage
Notes:              numbered footnotes (rate mechanics, anything bespoke)
```

### Why both book and market multiples

Distressed/stressed names trade at a discount: market-value leverage and market EV/EBITDA are the
real entry math (FLL: notes at 87 → market EV well below book). The pair of columns IS the
mispricing exhibit.

## Tie rules

- Cap Structure LTM EBITDA must equal Valuation Summary's LTM total (both from the same Actuals
  quarters) — audit check.
- Valuation Summary net debt (forecast) and Cap Structure net debt (today) are DIFFERENT numbers
  by design; label the as-of on each.
- Shares outstanding: same raw count source on both tabs.
- Any deck/memo derived from the model quotes ONLY numbers that exist as cells on these two tabs
  (or Model summary rows) — the outbound-artifact-gate provenance rule.
