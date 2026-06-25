# Actuals Ingestion — EDGAR-first, tie-out gated

The Actuals tab is the ground truth every other tab anchors to. Get it wrong and the whole model
is decoration. No shortcuts here: every figure as-reported, every figure sourced, every statement
tied out before any forecast cell exists.

## Sourcing hierarchy

1. **SEC EDGAR (default)** — `scripts/edgar_pull.py` hits the XBRL APIs
   (`data.sec.gov/api/xbrl/companyfacts/CIK##########.json` + per-concept `companyconcept`).
   Free, authoritative, machine-readable. Annual (10-K) and quarterly (10-Q) facts.
2. **Dom/Jaron-provided files** (filings PDFs, broker models, Bloomberg exports) — override EDGAR
   when supplied; same tie-out gates apply.
3. **Company IR releases** — for the latest quarter when the 10-Q isn't filed yet; flag any figure
   sourced from a press release rather than a filing.
4. **NEVER** web-search numbers into the Actuals tab. A figure with no filing locator doesn't go in.

## What EDGAR gives you vs what the tab needs

XBRL company facts give standardized concepts (us-gaap:Revenues, …) — good for scaffolding and
cross-checks, but the Actuals tab must mirror the company's **as-reported line items**
(e.g. FLL: Casino / Food and beverage / Hotel / Other operations revenue; the company's own
Adjusted EBITDA reconciliation). Workflow:

1. `edgar_pull.py <ticker>` → fetch companyfacts, dump candidate concepts + values per period.
2. Read the actual 10-K/10-Q financial statements (EDGAR filing index → R-file or the financial
   statements section) for the as-reported line structure, segment/property detail, and the
   non-GAAP reconciliation (Adj EBITDA detail usually lives in the earnings release / MD&A,
   NOT in XBRL).
3. Key the tab to the as-reported structure; use the XBRL pull as the cross-check that nothing
   was fat-fingered (script compares keyed totals vs XBRL concepts).

## Tab structure (mirror the reference)

- Sections in order: **P&L** (as-reported lines → operating income → other income/expense →
  pre-tax → tax → net income), **EBITDA reconciliation** (net loss + each disclosed adjustment →
  Adjusted EBITDA — copy the company's own recon line-for-line), **BS** (full as-reported),
  **CF** (full as-reported indirect statement, including the supplemental cash-paid-for-interest/
  taxes lines — the Model's bridge needs them).
- Columns: annual FY for the full history window (thesis-dependent; FLL used FY19–FY24, capturing
  pre-COVID baseline) + quarterly for the recent ~8 quarters (enough for LTM math + seasonality).
- Every cell: blue font, hardcoded, with the source comment.

## Source comment protocol

Every hardcoded input cell gets an Excel comment (openpyxl `Comment`):

```
Source: 10-Q Q3'25, filed 2025-11-06, Consolidated Statements of Operations
Source: FY24 10-K, filed 2025-03-10, Note 8 Long-Term Debt
Source: Q3'25 earnings release, 2025-11-05, Adj EBITDA reconciliation table
Source: Bloomberg, 2025-12-10, FLL US Equity last price   [market data]
```

For script-loaded figures, edgar_pull.py stamps `Source: EDGAR XBRL <concept>, <form> <period>,
accn <accession#>`. One comment per cell minimum on the Actuals tab; assumption cells on other
tabs carry `Source: Asterozoa estimate — <one-line basis>` or the thesis-doc reference.

## Tie-out gates (phase 2 cannot close until ALL pass)

Run via `audit_model.py --actuals-only`:

| # | Gate | Test |
|---|---|---|
| 1 | Revenue foots | Sum of revenue lines = reported Total Revenues, every column |
| 2 | OpEx foots | Sum of expense lines = reported Total operating expenses |
| 3 | P&L chains | Operating income = revenues − opex; pre-tax = OI + other; NI = pre-tax − tax |
| 4 | EBITDA recon foots | Net loss + adjustments = disclosed Adjusted EBITDA |
| 5 | BS balances | Total assets = Total liabilities + equity, every column |
| 6 | BS subtotals | Current assets/liabilities sections foot |
| 7 | CF sections foot | CFO/CFI/CFF line sums = reported section totals |
| 8 | Cash ties | CF beginning + net change = CF ending; CF ending = BS cash (+ restricted, match the company's definition) |
| 9 | Quarterly↔annual | Sum of 4 quarters = annual, for every line in overlap years (allow ±0.5 rounding) |
| 10 | XBRL cross-check | Keyed Total Revenues / NI / Total Assets / CFO match XBRL concepts (±0.1) |

Tolerance: ±$0.05M exact-keying lines; ±$0.5M for quarterly-sum-vs-annual (rounding in filings).
Any gate failure → fix the keying, never plug. There are no plugs anywhere in this system.

## Practical notes

- CIK lookup: `https://www.sec.gov/files/company_tickers.json` (script handles it).
- EDGAR requires a User-Agent header with contact email — script sets
  `Asterozoa Capital research contact@asterozoa.com`. Rate limit 10 req/s; script throttles.
- Fiscal-year companies: align column labels to the company's FY, label calendar overlap in notes.
- Restatements: use the LATEST filing's version of any restated period; comment notes the
  restatement.
- Units: model is $M with one decimal of precision in storage (key exact thousands ÷ 1000,
  e.g. `3.771`); display format rounds.
