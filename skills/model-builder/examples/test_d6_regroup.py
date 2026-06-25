#!/usr/bin/env python3
"""test_d6_regroup.py -- D6 segment regroup acceptance tests.

Usage:
    python3 test_d6_regroup.py <path-to-built-workbook.xlsx>

The workbook must have been built by build-demo-model.py AND recalced by
scripts/recalc.py (data_only=True reads Excel-computed values, not openpyxl
formula results).

Assertions (two groups):
  T2: After recalc, check rows in the segment regroup block evaluate to ~0
      for all AN_COLS (confirming segment totals == property totals).
  T3: Segment regroup cells (data_only=False) contain no direct Actuals!
      reference and contain at least one row number within the property block
      range read from the sidecar JSON.

Row metadata is read from a sidecar JSON file written by build_property_level_example:
  <workbook-stem>.d6meta.json  (next to the workbook)

NOTE on two-pass pattern (Risk R4): openpyxl cannot give both computed values
and raw formula strings from the same open() call. This script opens the
workbook twice: once with data_only=True to read computed values, once with
data_only=False to read raw formula strings. This is the correct pattern.

NOTE on recalc dependency (Risk R2): recalc.py requires macOS with Microsoft
Excel installed. If recalc has not been run before this test, data_only=True
values will be None for formula cells. The test will fail loudly in that case
rather than silently passing.
"""

import json
import re
import sys
from pathlib import Path

AN_COLS = ["D", "E", "F", "G", "H", "I", "J"]


def _load_meta(wb_path: str):
    """Read row map from the sidecar JSON written by build_property_level_example.

    The sidecar lives next to the workbook: <workbook-stem>.d6meta.json
    """
    sidecar = Path(wb_path).with_name(Path(wb_path).stem + ".d6meta.json")
    if not sidecar.exists():
        raise AssertionError(
            f"FAIL: sidecar metadata file not found: {sidecar}\n"
            "Was the workbook built with build_property_level_example?\n"
            "Run: python3 build-demo-model.py <out.xlsx>"
        )
    try:
        meta = json.loads(sidecar.read_text())
    except json.JSONDecodeError as exc:
        raise AssertionError(f"FAIL: sidecar JSON is not valid: {exc!r}")
    required_keys = [
        "prop_rev_start", "prop_rev_end", "prop_eb_start", "prop_eb_end",
        "seg_rev_start", "seg_rev_end", "seg_eb_start", "seg_eb_end",
        "rev_check", "ebitda_check",
    ]
    missing = [k for k in required_keys if k not in meta]
    if missing:
        raise AssertionError(f"FAIL: sidecar JSON missing keys: {missing}")
    return meta


def check_t2_check_rows_near_zero(path: str):
    """T2: check rows in segment regroup block evaluate to ~0 after recalc."""
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    meta = _load_meta(path)
    m = wb["Model"]

    errors = []
    for check_key, label in (("rev_check", "Revenue check row"),
                               ("ebitda_check", "EBITDA check row")):
        row = meta[check_key]
        for col in AN_COLS:
            cell = m[f"{col}{row}"]
            val = cell.value
            if val is None:
                errors.append(
                    f"  {label} {col}{row}: value is None "
                    f"(recalc not run? or formula error)"
                )
            elif abs(val) >= 0.01:
                errors.append(
                    f"  {label} {col}{row}: |{val}| >= 0.01 "
                    f"(segment total does not match property total)"
                )

    if errors:
        raise AssertionError("T2 FAIL:\n" + "\n".join(errors))
    print(f"T2 PASS: all check rows in rows {meta['rev_check']} and "
          f"{meta['ebitda_check']} are ~0 across {len(AN_COLS)} columns.")


def check_t3_no_actuals_link_and_property_row_refs(path: str):
    """T3: segment rows do not link to Actuals and do reference property block rows."""
    import openpyxl
    wb_formulas = openpyxl.load_workbook(path, data_only=False)
    meta = _load_meta(path)
    m = wb_formulas["Model"]

    errors = []

    # Revenue segment rows (excluding header and total rows):
    # seg_rev_start = first segment label row; seg_rev_end = total segment rev row
    # We check the interior data rows (start+1 to end-1 inclusive).
    seg_rev_rows = list(range(meta["seg_rev_start"] + 1, meta["seg_rev_end"]))
    seg_eb_rows = list(range(meta["seg_eb_start"] + 1, meta["seg_eb_end"]))
    prop_rev_range = (meta["prop_rev_start"], meta["prop_rev_end"])
    prop_eb_range = (meta["prop_eb_start"], meta["prop_eb_end"])

    def check_cell(col, row, allowed_row_range, context):
        cell = m[f"{col}{row}"]
        formula = str(cell.value) if cell.value is not None else ""
        # Assertion (a): no direct Actuals link
        if "Actuals!" in formula:
            errors.append(
                f"  T3a FAIL {context} {col}{row}: formula contains 'Actuals!' "
                f"(chain-of-custody violation): {formula!r}"
            )
        # Assertion (b): formula must be a SUM (D6 contract: segment rows are always SUMs)
        upper = formula.upper()
        if not upper.startswith("=SUM("):
            errors.append(
                f"  T3b FAIL {context} {col}{row}: formula is not a SUM "
                f"(D6 contract violation): {formula!r}"
            )
        # Assertion (c): formula references at least one row within property block
        row_nums_in_formula = [int(x) for x in re.findall(r"\d+", formula)]
        lo, hi = allowed_row_range
        if not any(lo <= rn <= hi for rn in row_nums_in_formula):
            errors.append(
                f"  T3c FAIL {context} {col}{row}: formula does not reference any row "
                f"in property block [{lo},{hi}]. Row nums found: {row_nums_in_formula}. "
                f"Formula: {formula!r}"
            )

    for row in seg_rev_rows:
        for col in AN_COLS:
            check_cell(col, row, prop_rev_range, "seg_rev")

    for row in seg_eb_rows:
        for col in AN_COLS:
            check_cell(col, row, prop_eb_range, "seg_eb")

    if errors:
        raise AssertionError("T3 FAIL:\n" + "\n".join(errors))

    print(f"T3 PASS: segment revenue rows {seg_rev_rows} and EBITDA rows {seg_eb_rows} "
          f"all reference property block rows and contain no Actuals! links.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 test_d6_regroup.py <workbook.xlsx>")
        sys.exit(1)
    path = sys.argv[1]
    if not Path(path).exists():
        print(f"ERROR: file not found: {path}")
        sys.exit(1)

    passed = 0
    failed = 0
    for test_fn, name in ((check_t2_check_rows_near_zero, "T2"),
                           (check_t3_no_actuals_link_and_property_row_refs, "T3")):
        try:
            test_fn(path)
            passed += 1
        except AssertionError as exc:
            print(str(exc))
            failed += 1
        except Exception as exc:
            print(f"{name} ERROR: {type(exc).__name__}: {exc}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
