# Research Framework: modeling spec + intellectual lineage

This file holds the modeling spec (the abbreviated three-statement on one tab, the cash-over-EBITDA rule, scenario toggles, what to skip, deep-vs-light) and the intellectual lineage (Gatto / Greenwald / FTI) that grounds the method. Anything that extends the stated design into mechanics the skill needs is flagged `[implementation]`. Anything not verified is flagged `[PLACEHOLDER]` or "unverified".

---

## Part 1: The abbreviated three-statement, on ONE tab

The method explicitly rejects the big-firm multi-tab template style. The design principle: keep the P&L and the cap structure on one tab. The modeling output is a single coherent block, not a workbook of linked tabs.

**Layout, all on one tab:**

```
P&L  ->  cash-flow bridge  ->  cap-stack  ->  scenario toggles
```

**What goes IN:**

- **P&L** -- top line through to the operating-earnings level, enough to drive the cash bridge. Compressed, not full line-item detail.
- **Cash-flow bridge** -- the load-bearing element. Bridges reported / adjusted earnings DOWN to cash from operations, then to cash from operations less capex. A fully banked number that has to tie to actual cash in a bank account.
- **Cap-stack** -- every debt security with amount, coupon, maturity, call schedule, covenants, plus net leverage. (FLL example: the 8.25% 2028 notes, revolver, the IL gaming-licensing PV obligation, cash.)
- **Scenario toggles** -- a single assumption block driving multiple scenario outputs. The whole scenario menu toggles from ONE input block, not separate models.

**What is SKIPPED by default:**

- Full balance-sheet forecast. Not built.
- Full P&L line-item detail. Compressed, not exhaustive.
- Intermediate DCF years. The method goes to the exit math, not a year-by-year discounted build. The abbreviated three-statement gets P&L to cash without forecasting depreciation account-by-account or working every intermediate year.

---

## Part 2: The cash-from-ops-over-EBITDA rule (core, non-negotiable)

- **Adjusted EBITDA is management's currency.** The method uses it but does NOT trust it. Reasoning: you have to speak their language, because management evaluates itself on adjusted EBITDA, so it is the comparison currency for comps and multiples. But it is a constructed number.
- **Always bridge back to cash from operations.** The skill must never present adjusted EBITDA as a terminal number. Every adjusted-EBITDA figure is accompanied by a bridge to cash from ops and cash-from-ops-less-capex. EBITDA is the language; cash is the truth.
- **Hard rule:** any EBITDA-based valuation output is paired with the cash bridge that validates it.

---

## Part 3: Scenario-toggle modeling (incl. the refi-with-cash-out shape)

The scenario block drives the standard credit/equity exit chain:

```
multiple-on-EBITDA  ->  enterprise value  ->  minus debt  ->  equity value  ->  price per share
```

That is a long-equity, DCF-flavored exit expressed through a multiple, NOT an activist / take-private / 13D output.

**The toggles bound the trade with a small number of scenarios off one assumption block.** The FLL case demonstrated: keep the bounding scenarios, cut the redundant middle ones. A clean menu is a downside case and an upside case, not a sprawling tree.

**The refi-with-cash-out worked shape (FLL scenario 4, the FLL base case):**

```
[scenario 4: refi-with-cash-out]
  1. Assume the EBITDA ramp lands (per the property-level ramp paths pulled from transcripts/IR decks).
  2. Apply a multiple on that EBITDA  ->  enterprise value.
  3. The refinancing puts new debt on at the cash-out level (this is the "cash-out" event).
  4. EV minus the post-refi debt  ->  equity value.
  5. Equity value / shares  ->  price per share.
```

The "why now" sat in the binary catalyst: the combined refi-with-cash-out event plus the EBITDA ramp, with a short catalyst window. Note: the FLL specifics (the 8.25% 2028 notes, the IL gaming PV obligation, the five-scenario menu) are illustrative of the SHAPE. The skill encodes the shape (one assumption block, bounding scenarios, the EV-to-equity exit chain), not the FLL numbers.

A fuller distressed scenario menu (when liquidity is binding) ranges across strategic alternatives: keep extending / refi off current cash flow (downside), new-debt, refi, refi-with-cash-out (the FLL base), and sale-leaseback. This is the restructuring-advisor's strategic-alternatives tree, each option toggled from the one assumption block. See the FTI lineage below.

---

## Part 4: Deep-vs-light heuristic

The same template over-engineers a clean compounder and under-serves a distressed name. Branch depth on the credit/business profile.

**GO DEEP -- distressed / stressed credits where liquidity matters:**

- When the credit is distressed or stressed and LIQUIDITY is the binding question, the model goes detailed: full cap-structure deep-dive, maturity ladder, covenant analysis, the scenario tree, and recovery/restructuring optionality. The cash-from-ops focus matters most here: in a liquidity-binding situation, the fully-banked cash number is the whole game. FLL sat near this end (a leveraged regional operator with a refi event that has to clear in a short window).

**GO LIGHT -- clean compounders growing ~10%/year:**

- For a business growing 10% a year, a simple P&L valuation is cleaner. Do not build the full scenario tree, do not over-elaborate the cap structure, do not run the liquidity-stress machinery. The abbreviated P&L-to-cash plus a multiple is enough. Over-modeling a clean compounder adds noise, not insight.

**The trigger `[implementation]`:** assess at ingestion time whether liquidity is binding (signals: elevated net leverage, a near-dated maturity wall, negative or fragile cash from ops, a financing event that must clear in a defined window). If yes, deep path. If a steady grower with comfortable coverage and no binding maturity, light path. Decide once, early, and state the decision and its reason explicitly in the output.

**Micro-first, macro-only-when-material.** The method is micro-first (individual security selection, not broad screening). A macro overlay enters ONLY when the industry backdrop is material to the assumption set (e.g., high-yield credit spreads when the whole thesis hinges on a refi clearing). The skill does not generate a macro section by default; it adds one only when an assumption depends on it.

---

## Part 5: Intellectual lineage (Gatto / Greenwald / FTI)

Three source traditions feed this method. Each is rendered as how it shapes the analysis. Load-bearing claims are source-tagged. Web sources as-of 2026-05-28. Book primary text was accessed via previews / summaries / tables of contents, not full text, so method details are faithfully-summarized-secondary, not verbatim-primary.

### 5.1 Michael Gatto, The Credit Investor's Handbook (Silver Point method)

The leverage-finance how-the-buy-side-underwrites reference (Wiley Finance, 2023). Gatto spent ~25 years in leveraged credit at Silver Point Capital and Goldman's Special Situations Group; adjunct at Columbia and Fordham/Gabelli. Sources: [Amazon listing](https://www.amazon.com/Credit-Investors-Handbook-Leveraged-Distressed/dp/1394196059), [Museum of American Finance event](https://www.moaf.org/events/general/2024-05-30-michael-gatto-on-the-credit-investors-handbook).

**Book structure (verified, three parts):** Part 1 Building Blocks of the Leveraged Credit Markets, Part 2 The Seven-Step Process of Evaluating a Debt Investment, Part 3 Distressed Debt Investing. Source: [Perlego TOC](https://www.perlego.com/book/4315998/).

**The seven-step process, components verified; full 1-to-7 numbering partially confirmed:**
- Named analytical components: qualitative industry and business analysis, financial statement analysis, forecasting, corporate valuation, relative value analysis, debt structuring. Sources: [Amazon](https://www.amazon.com/Credit-Investors-Handbook-Leveraged-Distressed/dp/1394196059), [Everand preview](https://www.everand.com/book/696405255/).
- Confirmed chapter anchors: Step 3 = Financial Statement Analysis, split into 3(a) Profitability, 3(b) Cash Flow and Liquidity, 3(c) Capital Structure; Step 4 = Forecasting. Source: web search of chapter titles, 2026-05-28.
- `[PLACEHOLDER / unverified]` the exact 1-to-7 ordering beyond Steps 3 and 4 is NOT verified from open web. Present the seven steps as a named sequence; do not assert a specific number for a step beyond 3 and 4 unless cross-checked against the book itself.

**How it shapes the analysis:**
- Cash flow and liquidity get their own dedicated step (3b), separate from profitability (3a). This is the textual root of the trust-cash-from-ops-not-adjusted-EBITDA rule.
- Capital structure is a first-class analysis step (3c), not an afterthought: every tranche, maturity ladder, amortization, covenant. Maps directly to the cap-structure deep-dive stage.
- Recovery / distressed mechanics live in Part 3: bankruptcy, subordination, creditor-on-creditor dynamics. The frame: where does value break in the cap stack, who holds the fulcrum security, and what is recovery by seniority. (`[unverified]` "fulcrum security" is standard distressed-credit vocabulary consistent with the book's scope, but a verbatim Gatto definition was not pulled from open web; use as a general term.) Sources: [Everand](https://www.everand.com/book/696405255/), [ny-alt summary](https://ny-alt.org/2025/08/25/the-credit-investors-handbook/).
- Relative value across the cap structure is its own step: comparing yields/spreads/price across tranches and vs comparables. The credit analogue to the comparables table.

**Takeaway for the skill:** Gatto justifies the ingestion sequence (business to financials to cap structure to relative value) and the cash-over-EBITDA discipline. For distressed/stressed names, add a recovery-by-seniority pass; for healthy ~10% growers, that pass is skippable, matching the go-detailed-only-when-liquidity-matters rule.

### 5.2 Bruce Greenwald, Value Investing: From Graham to Buffett and Beyond (Columbia method)

The canonical post-Graham valuation framework. Supplies the valuation theory for the multiple-to-EV-to-equity-value-to-price-per-share exit chain, and (more importantly) supplies the investment-angle synthesis layer the method targets. Source: [Columbia Business School](https://business.columbia.edu/insights/chazen-global-insights/greenwald-explains-value-investing-principles).

**Three-phase process (verified):** Search, Valuation, Review/Risk Management. Source: [Medium notes on the book](https://medium.com/@peter.simon419/).

**Phase 1, Search:** small-caps overlooked by institutions, spin-offs sold for non-fundamental reasons, boring/obscure companies, distressed situations, year-end window-dressing sales. Screen on fundamentals disconnected from price (ROE, margins, asset/earnings growth), not momentum.

**Phase 2, three-tier valuation (the core engine):**
- **Tier 1, Asset (Reproduction) Value:** what it would cost to recreate the assets. Reproduction cost in stable/growing industries, liquidation value in declining ones. The most reliable, most-knowable number.
- **Tier 2, Earnings Power Value (EPV):** `EPV = Adjusted Earnings / Cost of Capital`, a zero-growth perpetuity on sustainable current earnings. Adjusted Earnings = NOPAT minus Maintenance Capex plus Excess Depreciation; NOPAT = Normalized EBIT times (1 minus tax rate). Normalize EBIT over 5+ years, strip one-time items, add back growth-driving spend to isolate maintenance earnings. Greenwald prefers a personal required return over CAPM/beta for the discount rate. Sources: [StableBread](https://stablebread.com/earnings-power-value/), [GuruFocus](https://www.gurufocus.com/tutorial/article/216/).
- **Tier 3, Value of Growth:** growth only creates value inside a competitive moat. Only franchise value creates growth value. Outside a moat, growth merely recovers cost of capital.

**The franchise / barriers-to-entry test (the linchpin):**
- EPV greater than Asset Value means a franchise exists (the gap is franchise value).
- EPV roughly equal to Asset Value means no franchise (commodity economics).
- EPV less than Asset Value means value is eroding/being destroyed.
- Moat sources: economies of scale, customer captivity/switching costs, brand, access to capital. Moats fade under competition. Sources: [StableBread](https://stablebread.com/earnings-power-value/), [MOI Global](https://moiglobal.com/bruce-greenwald-on-the-second-edition-of-value-investing/), [Columbia Business School](https://business.columbia.edu/insights/chazen-global-insights/greenwald-explains-value-investing-principles).

**Phase 3, margin of safety / risk:** buy at 33-50% below intrinsic value, concentrate 8-10 names within circle of competence, treat margin of safety (not diversification) as the primary risk control.

**Takeaway for the skill:** Greenwald supplies the investment-angle synthesis layer the method targets. The bull/bear pass is structured as (a) does a franchise exist (EPV vs asset-value test), (b) what are the barriers to entry, (c) is growth value real or illusory, (d) where is the margin of safety. `[unverified]` An unnamed barriers-to-entry text is plausibly within the Greenwald lineage (Greenwald's Competition Demystified is the standard barriers-to-entry text), but no specific reference is confirmed. Flag as a likely match, not a confirmed one.

### 5.3 FTI Consulting restructuring method (the scenario-tree muscle)

FTI's Turnaround and Restructuring practice advises distressed companies on liquidity, business-plan rebuilds, financing, and complex debt restructurings. This is the origin of the scenario-tree instinct in the method. Source: [FTI Turnaround and Restructuring](https://www.fticonsulting.com/services/turnaround-and-restructuring).

**The 13-week cash flow forecast (the signature tool):**
- A rolling, forward-looking model of every inflow/outflow over 13 weeks to compute liquidity runway (how many weeks until cash depletes). Sources: [WSO restructuring modeling](https://www.wallstreetoasis.com/forum/investment-banking/restructuringdistressed-debt-modeling), [Road to Offer FTI guide](https://www.roadtooffer.com/blog/fti-consulting-case-interview-guide).
- Outflows categorized by flexibility: fixed (hard to cut), deferrable (capex, non-critical SG&A/IT), and debt service (cannot be eliminated).
- Sequencing principle: cash before strategy, always. Week 1 controllable costs, weeks 2-4 working-capital unlock, weeks 6-10 structural (asset sales). Source: [Road to Offer](https://www.roadtooffer.com/blog/fti-consulting-case-interview-guide).

**Recovery / returns waterfall:** restructuring engagements model equity valuation plus a returns waterfall and recovery analysis by creditor seniority alongside the 13-week. This is the where-does-value-break, who-recovers-what analysis, upstream of Gatto's fulcrum-security framing. Source: [WSO](https://www.wallstreetoasis.com/forum/investment-banking/restructuringdistressed-debt-modeling).

**Four-phase arc:** diagnose burn, stabilize liquidity, restructure operations, reposition for recovery, with strategic alternatives (refinance, asset sale, sale-leaseback, recapitalization) modeled as discrete scenarios. Sources: [Road to Offer](https://www.roadtooffer.com/blog/fti-consulting-case-interview-guide), [FTI Company Advisory](https://www.fticonsulting.com/services/turnaround-and-restructuring/company-advisory).

**Takeaway for the skill:** this explains the FLL scenario menu (keep-extending, new-debt, refi, refi-with-cash-out, sale-leaseback) as a restructuring-advisor's strategic-alternatives tree, each toggled from one assumption block, and the go-detailed-only-when-liquidity-matters rule (the 13-week / runway machinery is reserved for stressed credits). When a name is distressed, the synthesis pass adds (a) a liquidity-runway estimate, (b) a strategic-alternatives scenario set, (c) recovery-by-seniority. For healthy names, a simple P&L-to-cash valuation suffices.

### 5.4 How the three lineages compose

- **Gatto** is the ingestion + cap-structure discipline: business to cash (not EBITDA) to every debt tranche to relative value. Justifies the folder-per-company primary-source order and the cash-over-adjusted-EBITDA rule.
- **Greenwald** is the investment-angle synthesis layer the method targets: franchise test (EPV vs asset value), barriers to entry, real-vs-illusory growth, margin of safety. The bull/bear pass bolted on top of ingestion.
- **FTI** is the scenario-tree + liquidity machinery: 13-week runway, strategic-alternatives toggles, recovery waterfall. Engaged only for stressed/distressed names.

**One line for the design:** ingestion pass (Gatto-ordered, primary-source-flagged) + synthesis pass (Greenwald franchise / margin-of-safety bull-bear) + a conditional distressed module (FTI runway + recovery waterfall) that activates only when liquidity is material.

---

## Verification flags (do not overstate)

- Gatto's exact Step 1-to-7 numbering beyond Steps 3 and 4 is NOT verified from open web. Present as named components in sequence.
- The "fulcrum security" verbatim Gatto definition was NOT pulled; it is standard distressed vocabulary, use as a general term.
- An unnamed barriers-to-entry text is unidentified; Greenwald's Competition Demystified is the strongest candidate by lineage but is NOT confirmed.
- All web sources as-of 2026-05-28. Book primary text accessed via previews / summaries / TOC, not full text; treat method details as faithfully-summarized-secondary, not verbatim-primary.
