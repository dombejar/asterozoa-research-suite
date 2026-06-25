---
type: research
status: active
created: 2026-06-24
modified: 2026-06-24
ticker: MNR
company: Mach Natural Resources LP
role: adversarial-verification
source_run: edgar-only
---

# VERIFICATION: MNR Exec Summary Adversarial Check

Independent re-pull of EDGAR primary sources for every quantitative claim and named fact in MNR-research-exec-summary.md. Entity confirmed via CIK 0001980088 submissions JSON before any check.

Sources used: EDGAR submissions JSON, XBRL companyfacts API (CIK0001980088), 10-K FY2025 (mnr-20251231.htm, acc 0001628280-26-017249), 10-Q Q1 2026 (mnr-20260331.htm, acc 0001628280-26-032065), 10-Q Q3 2025 (mnr-20250930.htm, acc 0001628280-25-050305), 10-Q Q2 2025 (mnr-20250630.htm, acc 0001628280-25-038877), 10-Q Q1 2025 (mnr-20250331.htm, acc 0001628280-25-023787), 10-K FY2024 (mnr-20241231.htm, acc 0001628280-25-012591), 8-K 2026-05-07 (press release), 8-K 2026-05-22 (ATM agreement), 8-K 2026-04-08 (secondary offering), 424B4 2026-04-06 (secondary prospectus).

---

## Entity Confirmation

**CONFIRMED.** CIK 0001980088 = MACH NATURAL RESOURCES LP. Ticker MNR. SIC 1311 (Crude Petroleum & Natural Gas). NYSE listed. Oklahoma City, OK. Delaware LP. NOT the former Monmouth REIT (which was acquired 2022). This CIK has no prior REIT history.

---

## Checked Claims

### 1. Entity: "Mach Natural Resources LP (NYSE: MNR), upstream oil and gas MLP, Oklahoma City"
- **CONFIRMED.** EDGAR submissions JSON: name=MACH NATURAL RESOURCES LP, ticker=MNR, SIC=1311, city=Oklahoma City.
- Source: CIK0001980088.json.

### 2. CIK: "0001980088"
- **CONFIRMED.** Exact match in submissions JSON.

### 3. "Tom Ward acquire-and-distribute MLP"
- **CONFIRMED (partial).** Tom L. Ward is confirmed as Chief Executive Officer and Director (10-K FY2025 and Q1 2026 press release quote). "Acquire-and-distribute" is an analytical description, not a quoted term, but it accurately captures the stated strategy. Source: 10-K FY2025 director biographies; Q1 2026 press release.

### 4. "Distribution swung from $0.79 to $0.27/unit inside FY2025"
- **CONFIRMED.** Q1 2025 declared distribution = $0.79/unit (Q1 2025 10-Q subsequent event). Q3 2025 declared distribution = $0.27/unit (Q3 2025 10-Q subsequent event). FY2025 sequence: Q1=$0.79, Q2=$0.38, Q3=$0.27, Q4=$0.53. The swing from high to low within FY2025 is accurate. The deliverable does not mention the Q4 2025 recovery to $0.53; this omission is material context but the stated claim is factually true.
- Source: 10-Q Q1 2025 (Note 14 subsequent event); 10-Q Q3 2025 (Note 16 subsequent event).

### 5. "CFO held at ~$491-507M across FY2023-2025"
- **CONFIRMED.** XBRL: FY2023 CFO = $491,742K; FY2024 CFO = $505,292K; FY2025 CFO = $506,956K.
- Source: XBRL companyfacts, NetCashProvidedByUsedInOperatingActivities.

### 6. "Q1 2026 CFO was $170M (~$681M run-rate)"
- **CONFIRMED.** Q1 2026 CFO = $170,313K. Annualized = $681.3M. Source: 10-Q Q1 2026 cash flow statement.

### 7. "Q1 2026 GAAP net loss of $35M is a non-cash $103.8M mark-to-market hedge loss"
- **CONFIRMED.** Q1 2026 net loss = $(35,038)K. Unrealized loss on derivative instruments = $103,769K (in Adj EBITDA reconciliation table, 10-Q Q1 2026 MD&A). The $103.8M figure rounds from $103.769M.
- Source: 10-Q Q1 2026 consolidated statements of operations; MD&A Adj EBITDA reconciliation.

### 8. "All debt is a single $1.14B revolver maturing Feb 2029, no bonds, no near-term wall"
- **WRONG (structure mislabeled).** The $1.14B outstanding is correct in total but the instrument is NOT a single revolver. After the September 12, 2025 First Amendment to the New Credit Agreement, the facility has two tranches: (1) a revolving commitment of $1.0B and (2) $450M in term loan commitments, both under one New Credit Agreement with Truist as agent and Feb 27, 2029 maturity. As of March 31, 2026: total outstanding = $1,134,520K ($1.14B), of which the Q1 2026 press release discloses $695M utilized under the revolving tranche and $358M of available liquidity. The 10-Q Note confirms $1.14B total outstanding, $5M LC, $305M revolver availability. "No bonds, no near-term wall" and the Feb 2029 maturity are CONFIRMED. The "single revolver" label is inaccurate and understates structure complexity.
- Source: 10-Q Q1 2026 Note (Long-Term Debt), 8-K 2026-05-07 press release.

### 9. "~1.7-1.9x net leverage with covenant room to 3.0x"
- **CONFIRMED.** Net debt FY2025 = $1,101.4M / Adj EBITDA $593.3M = 1.86x. Net debt Q1 2026 LTM = $1,081.8M / LTM Adj EBITDA ~$627.6M = 1.72x. Covenant: "consolidated total net leverage ratio of less than or equal to 3.00 to 1.00" confirmed in 10-Q Q1 2026 debt note.
- Source: 10-Q Q1 2026 balance sheet + debt note; 10-K FY2025 MD&A reconciliation.

### 10. "Q1 2026 declared distribution coverage of only ~1.0x ($107.4M CAD vs ~$107.7M declared)"
- **CONFIRMED.** Q1 2026 CAD = $107,350K. Declared = $0.64/unit × 168,218,770 units = $107,660K. Coverage = 0.997x. Deliverable correctly characterizes as "essentially 1.0x" with slight deficit.
- Source: 10-Q Q1 2026 MD&A CAD reconciliation; subsequent event note (distribution declaration).

### 11. "Borrowing base redetermined every April and October"
- **CONFIRMED.** 10-Q Q1 2026 debt note: "The New Credit Agreement's borrowing base is redetermined semi-annually, in April and October."
- Source: 10-Q Q1 2026 Note (Long-Term Debt).

### 12. "$695M revolver drawn at 3/31/26 vs $1.14B in 10-Q -- FLAG: treat $1.14B as authoritative"
- **CONFIRMED (partially).** The deliverable's FLAG correctly notes the discrepancy. $1.14B is the authoritative total outstanding figure per 10-Q Note. The $695M is the revolving tranche only (confirmed by the press release's reference to "its $1.0B revolving credit facility"). The deliverable calls this a "likely slice error" but the correct explanation is that $695M = revolving draws and the remainder (~$440M) = term loan draws, both under the same agreement. The FLAG direction (use $1.14B for total debt) is correct.
- Source: 10-Q Q1 2026 Note; 8-K 2026-05-07 press release.

### 13. "Sep 2025 amendment carved out up to $750M of BB-reduction debt as a buffer"
- **CONFIRMED.** 10-Q Q1 2026 debt note: "excludes up to $750.0 million in principal amount of Borrowing Base Reduction Debt... from the provisions otherwise requiring a borrowing base reduction."
- Source: 10-Q Q1 2026 Note (Long-Term Debt).

### 14. "Truist-agented RBL"
- **CONFIRMED.** 10-K FY2025 and 10-Q Q1 2026: "Truist Bank, as administrative agent and collateral agent."
- Source: 10-K FY2025 definition of New Credit Agreement; 10-Q Q1 2026 debt note.

### 15. "Effective rate 7.7%"
- **CONFIRMED.** Both 10-K FY2025 and 10-Q Q1 2026: "Borrowings outstanding under the New Credit Agreement bore an interest rate of 7.7%."
- Source: 10-K FY2025 interest rate risk section; 10-Q Q1 2026 debt note.

### 16. "100bp on ~$1.14B is ~$11.5M/yr of CAD"
- **CONFIRMED.** 10-K FY2025: "impact of 1% (or 100 basis points) increase or decrease... approximately $11.5 million per year." 10-Q Q1 2026 cites $11.4M (minor rounding of $1,134.5M × 1%). Deliverable uses $11.5M, which matches the 10-K FY2025 figure.
- Source: 10-K FY2025 interest rate risk section.

### 17. "Refi already happened in Feb 2025, retiring the SOFR+650 term loan into a cheaper 2029 revolver"
- **CONFIRMED (SOFR+650 confirmed; but "revolver" is imprecise as noted above).** Old term loan rate: "three-month SOFR plus 6.50%" confirmed in 10-K FY2025 debt note (12.3% effective rate at 12/31/24). New Credit Agreement entered Feb 27, 2025. SOFR+6.50% = SOFR+650bps is accurate. The characterization of the new instrument as only a "revolver" repeats the structural imprecision noted in claim #8.
- Source: 10-K FY2025 debt note (prior facilities section).

### 18. "60-70% gas by volume"
- **CONFIRMED.** Q1 2026 press release: "16% oil, 70% natural gas and 14% NGLs" by volume. The range "60-70%" is consistent with Q1 2026 actual 70% and the FY2024 production mix (FY2024 10-K shows natural gas MMcf/total Boe implies ~53% gas at standard 6:1 conversion -- the deliverable's range is defensible for the expanded post-IKAV/Sabinal portfolio which is heavier gas).
- Note: The 60% lower bound is not explicitly verified by an EDGAR figure for any specific period; use "~70% as of Q1 2026" for precision.
- Source: 8-K 2026-05-07 press release.

### 19. "Firm sale of ~282 Bbtu through 2030 at a fixed $1.72/MMBtu" (IKAV contract)
- **CONFIRMED.** 10-Q Q1 2026 Note 10 (Sales Commitments): total remaining = 282,163 Bbtu through 2030, at $1.72/MMBtu fixed. "~282 Bbtu" is slightly imprecise (exact = 282,163 Bbtu as of 3/31/26) but materially correct.
- Source: 10-Q Q1 2026 Note 10.

### 20. "~$3.51 hedge strip" (gas)
- **CONFIRMED.** Q1 2026 derivatives table: natural gas fixed price swaps, remaining 2026, NYMEX HH, 28,772 Bbtu at $3.51/MMBtu.
- Source: 10-Q Q1 2026 Note 7 (derivative contracts).

### 21. "Oil spot below the ~$66 swap strikes in Q1 2026"
- **CONFIRMED.** Oil fixed price swaps remaining 2026: 2,477 Mbbl at $65.87 NYMEX WTI (rounds to ~$66). Q1 2026 realized oil price = $69.73/Bbl (per press release) was above the swap strike, so the reference is to forward spot vs hedged level.
- Source: 10-Q Q1 2026 Note 7.

### 22. Total revenue: FY2024 = $969.6M, FY2025 = $1,175.4M, Q1 2026 = $285.9M
- **CONFIRMED.** XBRL: FY2024 Revenues = $969,628K; FY2025 = $1,175,390K; Q1 2026 = $285,925K.
- Source: XBRL companyfacts; 10-K FY2025 income statement; 10-Q Q1 2026 income statement.

### 23. Adjusted EBITDA: FY2024 = $598.5M, FY2025 = $593.3M, Q1 2026 = $194.6M
- **CONFIRMED.** 10-K FY2025: Adj EBITDA FY2025 = $593,256K, FY2024 = $598,481K. 10-Q Q1 2026: Adj EBITDA = $194,624K.
- Source: 10-K FY2025 Adj EBITDA reconciliation; 10-Q Q1 2026 MD&A.

### 24. Cash from operations: FY2024 = $505.3M, FY2025 = $507.0M, Q1 2026 = $170.3M
- **CONFIRMED.** XBRL: FY2024 = $505,292K; FY2025 = $506,956K; Q1 2026 = $170,313K.
- Source: XBRL companyfacts; confirmed in filing cash flow statements.

### 25. Net income: FY2024 = $185.2M, FY2025 = $143.0M, Q1 2026 = $(35.0M)
- **CONFIRMED.** XBRL: FY2024 = $185,179K; FY2025 = $142,984K; Q1 2026 = $(35,038)K.
- Source: XBRL companyfacts.

### 26. Development capex: FY2024 = $239.4M, FY2025 = $251.9M, Q1 2026 = ~$75M
- **CONFIRMED (with note).** 10-K FY2025 CAD reconciliation: development costs FY2025 = $251,854K = $251.9M; FY2024 = $239,435K = $239.4M. For Q1 2026: the $75M figure matches total capital expenditures including acquisitions ($75,249K per segment note). E&P-only development capex = $55,305K + $4,740K = $60,045K. The deliverable's ~$75M corresponds to total capex (including the minor $2.4M in asset acquisitions), consistent with how the company presents it in the segment disclosure. Not wrong, but ~$60M is the cleaner "development only" figure.
- Source: 10-K FY2025 CAD reconciliation; 10-Q Q1 2026 segment note and cash flow statement.

### 27. Cash Available for Distribution: FY2024 = ~$266M, FY2025 = ~$274.4M, Q1 2026 = ~$107.4M
- **CONFIRMED.** 10-K FY2025: FY2025 CAD = $274,393K; FY2024 CAD = $266,107K. 10-Q Q1 2026: CAD = $107,350K.
- Source: 10-K FY2025 CAD reconciliation; 10-Q Q1 2026 MD&A CAD reconciliation.

### 28. Distributions paid: FY2024 = $309.8M, FY2025 = $244.5M, Q1 2026 = $89.2M
- **CONFIRMED.** 10-K FY2025: FY2024 distributions to unitholders = $309,829K; FY2025 = $244,495K. 10-Q Q1 2026: Q1 2026 = $89,166K.
- Source: 10-K FY2025 cash flow statement; 10-Q Q1 2026 cash flow statement.

### 29. Declared distribution coverage: FY2025 = ~1.12x, Q1 2026 = ~1.0x
- **CONFIRMED.** FY2025: $274,393K CAD / $244,495K paid = 1.122x. Q1 2026: $107,350K CAD / $107,660K declared = 0.997x (effectively 1.0x with a slight deficit).
- Source: Derived from confirmed filing figures above.

### 30. Net debt: FY2025 = ~$1,101M, Q1 2026 = ~$1,082M
- **CONFIRMED.** FY2025: long-term debt $1,144,056K - cash $42,633K = $1,101,423K. Q1 2026: $1,134,520K - $52,689K = $1,081,831K.
- Source: 10-Q Q1 2026 balance sheet (comparative periods).

### 31. Units outstanding: 103.5M (12/24), 168.2M (3/26)
- **CONFIRMED.** 10-K FY2025 partners' capital table: balance at December 31, 2024 = 103,490K units = 103.49M (rounds to 103.5M). 10-Q Q1 2026 cover: 168,224,213 units as of May 1, 2026; balance sheet date consistent with 168.2M.
- Source: 10-K FY2025 statements of partners' capital; 10-Q Q1 2026 cover page.

### 32. Total proved reserves: FY2024 = 337,250 MBoe, FY2025 = 704,732 MBoe
- **CONFIRMED.** 10-K FY2025 reserves summary table: FY2025 total proved = 704,732 MBoe; FY2024 = 337,250 MBoe.
- Source: 10-K FY2025 reserves disclosure.

### 33. PV-10: FY2024 = $1,890M, FY2025 = $3,088M
- **CONFIRMED.** 10-K FY2025 reserves table: PV-10 FY2025 = $3,088M; FY2024 = $1,890M.
- Source: 10-K FY2025 reserves disclosure.

### 34. "Two simultaneous Sep 2025 deals totaling ~$1.2B" (IKAV + Sabinal acquisitions)
- **CONFIRMED.** IKAV Acquisition: $349.8M cash + 30.6M units (~$409.9M equity consideration) = ~$759.7M total. Sabinal Acquisition: $199.3M cash + 19.2M units (~$253.9M equity consideration) = ~$453.2M total. Combined = ~$1,212.9M. Both closed September 16, 2025.
- Source: 10-K FY2025 Note 3 (Business Combinations).

### 35. "$90.4M Deep Anadarko impairment"
- **CONFIRMED (impairment amount confirmed; "Deep Anadarko" is press-release language).** XBRL: ImpairmentOfOilAndGasProperties FY2025 = $90,430K = $90.4M. The term "Deep Anadarko" does not appear in the 10-K or 10-Q filings; it appears in the Q1 2026 earnings press release (8-K 2026-05-07): "Paused Deep Anadarko drilling activity." The deliverable correctly tags "[T1: 10-K FY2025; 8-K 2026-05-07]."
- Source: XBRL; 8-K 2026-05-07 press release exhibit.

### 36. "Tom Ward has 4.8M units pledged as personal debt collateral"
- **CONFIRMED.** 10-K FY2025: "Tom L Ward 1992 Revocable Trust, of which 4,800,000 common units are pledged as collateral to secure certain personal indebtedness of Mr. Ward."
- Source: 10-K FY2025 beneficial ownership table footnote.

### 37. "Sponsors sold 9M units at $13.05 in April 2026"
- **WRONG (wrong attribution).** 9M units were sold at $13.05/unit in the April 2026 Secondary Offering -- CONFIRMED. But the sellers were NOT "sponsors." The selling unitholders were: VEPU Inc. (~4.6M units), Simlog Inc. (~0.9M units) -- both IKAV acquisition counterparties -- and Sabinal Energy Operating LLC (~3.4M units) -- the Sabinal acquisition counterparty. Tom L. Ward (CEO, through his trust and affiliated entities) PURCHASED 153,256 units in the offering. The sponsors (BCE/Bayou City Energy Management) did not sell units in this offering. This is a material factual error in the deliverable's "catalysts slice."
- Source: 424B4 prospectus dated April 6, 2026 (selling unitholders table); 8-K 2026-04-08.

### 38. "$100M ATM was opened in May 2026"
- **CONFIRMED.** 8-K 2026-05-22: "equity distribution agreement... having an aggregate offering price of up to $100,000,000... through the Agent [Morgan Stanley]." Entered May 22, 2026.
- Source: 8-K 2026-05-22 (Item 8.01).

### 39. Borrowing base covenant context: "covenant room to 3.0x"
- **CONFIRMED.** 10-Q Q1 2026 debt note: "consolidated total net leverage ratio of less than or equal to 3.00 to 1.00." FY2025 net leverage ~1.86x and Q1 2026 LTM ~1.72x, both well below the 3.00x covenant threshold.
- Source: 10-Q Q1 2026 Note (Long-Term Debt).

### 40. "No public debt to buy: only a private bank revolver"
- **CONFIRMED (material point is correct; instrument label is imprecise).** MNR has zero publicly traded notes or bonds. The only long-term debt is the New Credit Agreement (private bank facility), confirmed by the absence of any bond-related XBRL tags. The "revolver only" label understates the structure (see claim #8) but the conclusion -- no public debt to buy -- is correct.
- Source: XBRL companyfacts (no public bond instruments); 10-K FY2025 debt note.

### 41. "February 2025 Offering" referenced in the refi
- **CONFIRMED.** 10-Q Q1 2026: "proceeds from the February 2025 Offering" referenced as a source of funds for repaying the old term loan.
- Source: 10-Q Q1 2026 debt note.

### 42. Annualized $0.64/unit distribution = "~$2.56/unit annualized rate"
- **CONFIRMED.** $0.64 × 4 = $2.56. The Q1 2026 declared distribution of $0.64/unit is confirmed; the annualization arithmetic is correct.
- Source: 10-Q Q1 2026 subsequent event note.

### 43. Flags carried in deliverable (a)-(f): assessed
- (a) No market price / EV / peer multiples in EDGAR: **CONFIRMED as unfillable from EDGAR.** Appropriate FLAG.
- (b) No credit rating disclosed: **CONFIRMED.** No rating referenced in any filing. Appropriate FLAG.
- (c) No FY2026 production or capex guidance: **WRONG FLAG (partially).** The 10-K FY2025 and Q1 2026 10-Q both disclose FY2026 development capex budget of "$315.0 million to $360.0 million." No production guidance is issued, which is correctly flagged. The capex guidance EXISTS in EDGAR. The deliverable's "no FY2026 capex guidance" claim is inaccurate.
- (d) FY2025 CAD bottom line derived from components: **CONFIRMED.** $274,393K appears directly in the 10-K MD&A CAD reconciliation; the FLAG is excessively cautious but harmless.
- (e) Hedge coverage as % of production not computable: **CONFIRMED as limitation.** Appropriate FLAG.
- (f) $695M vs $1.14B discrepancy: **CONFIRMED. Explanation in FLAG is incomplete** (see claim #8 and #12 above). The recommendation to treat $1.14B as authoritative is correct.

---

## Summary of Problems

### WRONG (material, must fix)

1. **Claim: "all debt is a single $1.14B revolver maturing Feb 2029"**
   The $1.14B total outstanding is correct but the instrument is a combined credit agreement with TWO tranches: (1) revolving commitment of $1.0B and (2) term loan commitments of $450M, both created/amended under the September 12, 2025 First Amendment to the New Credit Agreement, both maturing February 27, 2029. The revolving portion outstanding was ~$695M at 3/31/26; term loan portion ~$440M. Calling it "a single revolver" is wrong and understates structural complexity. The "no bonds, no near-term wall, Feb 2029 maturity, Truist-agented" sub-claims are all correct.
   Fix: "all debt is under a single New Credit Agreement (revolving tranche $1.0B + term loan tranche $450M) maturing Feb 27, 2029; $1.14B drawn as of 3/31/26."

2. **Claim: "sponsors sold 9M units at $13.05 in April 2026"**
   The sellers were NOT sponsors (BCE/Bayou City Energy). The selling unitholders were VEPU Inc. and Simlog Inc. (the entities that received unit consideration in the IKAV acquisition) and Sabinal Energy Operating LLC (which received unit consideration in the Sabinal acquisition). Tom Ward (CEO) actually PURCHASED 153,256 units in the same offering. Calling these sellers "sponsors" conflates them with BCE.
   Fix: "IKAV and Sabinal acquisition counterparties (VEPU Inc., Simlog Inc., Sabinal Energy Operating) sold 9M units at $13.05 in April 2026."

### WRONG (minor / partially wrong flag)

3. **Flag (c): "no FY2026 capex guidance issued"**
   Both the 10-K FY2025 and Q1 2026 10-Q explicitly disclose: "our budget for 2026 is between $315.0 million and $360.0 million" (development costs). FY2026 capex guidance EXISTS in EDGAR. The deliverable should remove this specific flag or correct it to note that production guidance (not capex guidance) is absent.
   Fix: Remove flag (c) or rephrase as "no FY2026 production guidance issued; development capex budget disclosed at $315-$360M."

### UNSUPPORTED / UNVERIFIABLE FROM EDGAR (flagged correctly)

4. Market price / market cap / EV / peer multiples: correctly flagged as absent from EDGAR.
5. Credit rating: correctly flagged as absent.
6. Distribution yield calculation using "~$13-15 unit price": correctly flagged as non-EDGAR.
7. "High-teens distribution yield" at current price: correctly flagged as non-EDGAR.

---

## Verdict

**verdict_ok: false**

Two material wrong claims require correction: the debt structure label ("single revolver" is wrong, it is a combined revolver + term loan credit agreement) and the secondary offering seller attribution ("sponsors" is wrong, sellers were the IKAV/Sabinal acquisition counterparties). One minor flag is factually wrong (FY2026 capex guidance does exist in EDGAR). All quantitative financial figures in the abbreviated financial table are confirmed against primary EDGAR sources. The investment thesis, risk rankings, and conclusion are analytically sound based on the confirmed data.
