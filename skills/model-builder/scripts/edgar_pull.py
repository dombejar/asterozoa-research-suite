#!/usr/bin/env python3
"""edgar_pull.py — SEC EDGAR XBRL fetch for the Actuals tab (see reference/actuals-ingestion.md).

Pulls companyfacts for a ticker, extracts annual (10-K) and quarterly (10-Q) values for the
core cross-check concepts, and prints/exports them. This SCAFFOLDS and CROSS-CHECKS the Actuals
tab; the as-reported line detail is still keyed from the filings themselves.

Usage:
    python3 edgar_pull.py FLL                      # summary table of core concepts
    python3 edgar_pull.py FLL --concept Revenues   # one concept, all periods
    python3 edgar_pull.py FLL --json out.json      # dump everything extracted
    python3 edgar_pull.py FLL --list | grep -i rev # discover available concept names

EDGAR etiquette: identifying User-Agent, ≤10 req/s (we make 2 requests total).
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request

UA = {"User-Agent": "Asterozoa Capital research contact@asterozoa.com"}

CORE_CONCEPTS = [
    # (label, [candidate us-gaap tags in preference order])
    ("Revenue", ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
                 "RevenueFromContractWithCustomerIncludingAssessedTax"]),
    ("Operating income", ["OperatingIncomeLoss"]),
    ("Net income", ["NetIncomeLoss", "ProfitLoss"]),
    ("Total assets", ["Assets"]),
    ("Cash", ["CashAndCashEquivalentsAtCarryingValue"]),
    ("Total debt (LT)", ["LongTermDebtNoncurrent", "LongTermDebt"]),
    ("CFO", ["NetCashProvidedByUsedInOperatingActivities"]),
    ("Capex", ["PaymentsToAcquirePropertyPlantAndEquipment"]),
    ("Interest expense", ["InterestExpense", "InterestExpenseNet",
                          "InterestIncomeExpenseNet"]),
    ("Shares outstanding", ["CommonStockSharesOutstanding",
                            "EntityCommonStockSharesOutstanding"]),
]


def get_json(url: str):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def cik_for(ticker: str) -> str:
    data = get_json("https://www.sec.gov/files/company_tickers.json")
    for row in data.values():
        if row["ticker"].upper() == ticker.upper():
            return f"{row['cik_str']:010d}", row["title"]
    sys.exit(f"FATAL: ticker {ticker} not found in SEC company_tickers.json")


def extract(facts: dict, tag: str):
    """Return {'annual': [(end, val, form, accn)...], 'quarterly': [...]} for a us-gaap tag."""
    node = facts.get("facts", {}).get("us-gaap", {}).get(tag) \
        or facts.get("facts", {}).get("dei", {}).get(tag)
    if not node:
        return None
    out = {"annual": [], "quarterly": []}
    for unit, items in node.get("units", {}).items():
        for it in items:
            if "end" not in it or it.get("val") is None:
                continue
            rec = (it["end"], it["val"], it.get("form", ""), it.get("accn", ""),
                   it.get("start", ""), it.get("fy"), it.get("fp"))
            dur = None
            if it.get("start"):
                from datetime import date
                s = date.fromisoformat(it["start"]); e = date.fromisoformat(it["end"])
                dur = (e - s).days
            if dur is None or dur > 300:
                out["annual"].append(rec)
            elif dur < 100:
                out["quarterly"].append(rec)
    # dedupe by (end,val), keep latest filing's view
    for k in out:
        seen, dedup = set(), []
        for rec in sorted(out[k], key=lambda r: r[0]):
            if (rec[0], rec[1]) not in seen:
                seen.add((rec[0], rec[1])); dedup.append(rec)
        out[k] = dedup
    return out


def fmt_m(v):
    return f"{v/1e6:,.1f}" if abs(v) >= 1e5 else f"{v:,.0f}"


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    ticker = args[0]
    cik, title = cik_for(ticker)
    print(f"{ticker.upper()} — {title} (CIK {cik})")
    time.sleep(0.15)
    facts = get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json")

    if "--list" in args:
        for tag in sorted(facts.get("facts", {}).get("us-gaap", {})):
            print(tag)
        return

    if "--concept" in args:
        tag = args[args.index("--concept") + 1]
        data = extract(facts, tag)
        if not data:
            sys.exit(f"concept {tag} not found")
        for kind in ("annual", "quarterly"):
            print(f"\n{tag} — {kind}")
            for end, val, form, accn, start, fy, fp in data[kind][-12:]:
                print(f"  {start or '':>10} → {end}  {fmt_m(val):>14}  {form:<6} "
                      f"FY{fy} {fp or ''}  accn {accn}")
        return

    dump = {}
    print(f"\n{'concept':<22}{'tag used':<52}{'latest FY':<14}{'latest Q':<14}")
    for label, tags in CORE_CONCEPTS:
        data, used = None, None
        for tag in tags:
            data = extract(facts, tag)
            if data and (data["annual"] or data["quarterly"]):
                used = tag; break
        if not data:
            print(f"{label:<22}{'— none found —'}")
            continue
        dump[used] = data
        la = data["annual"][-1] if data["annual"] else None
        lq = data["quarterly"][-1] if data["quarterly"] else None
        print(f"{label:<22}{used:<52}"
              f"{(la[0][:4] + ': ' + fmt_m(la[1])) if la else '—':<22}"
              f"{(lq[0] + ': ' + fmt_m(lq[1])) if lq else '—'}")
        if "--full" in args:
            for end, val, form, *_ in data["annual"]:
                print(f"    A {end}  {fmt_m(val):>14}  {form}")

    if "--json" in args:
        out = args[args.index("--json") + 1]
        with open(out, "w") as f:
            json.dump(dump, f, indent=1, default=str)
        print(f"\nwritten: {out}")
    print("\nStamp keyed cells: Source: EDGAR XBRL <tag>, <form> <period-end>, accn <accession>")


if __name__ == "__main__":
    main()
