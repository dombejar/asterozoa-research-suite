#!/usr/bin/env python3
"""_excel_worker_win.py — Windows COM worker for the Excel recalc oracle.

Runs in a CHILD PROCESS spawned by excel_oracle._run_worker so the parent can
enforce a hard timeout (excel_oracle.OP_TIMEOUT) and, on hang, kill ONLY the
Excel instance this worker owns (its PID is written to the pid_file handed in the
job, immediately after the dedicated instance is created). DCOM-launched Excel is
not a child of this process, so a Job Object can't capture it — the PID handshake
is the cleanup contract.

Protocol:
  stdin : one JSON job  {"op": "recalc"|"sweep"|"version", "path": ..., ...}
  stdout: one JSON result; for sweep {"states": [[raw read,...],...],
          "default_restored": true}. recalc/version return small dicts.
  exit  : 0 ok; 3 = Excel/COM unavailable (parent -> NoExcelError); 1 = other
          failure (parent -> OracleError). The structured reason is printed to
          stdout on a controlled failure, else to stderr.

This file is import-light on non-Windows (only runs under win32 with pywin32).
Cell reads are returned RAW (native COM types: float/int/str/bool/None, CVErr
ints for errors); excel_oracle.normalize_value canonicalizes them parent-side so
Mac and Windows share one normalization.
"""
import json
import os
import sys

XL_CALCULATION_AUTOMATIC = -4105  # xlCalculationAutomatic


def _fail(reason: str, code: int):
    """Print a structured reason to stdout and exit with the contract code."""
    print(json.dumps({"error": reason}))
    sys.exit(code)


def _claim_pid(app, pid_file):
    """Write this worker's OWNED Excel PID so the parent can kill only it on
    timeout. Best-effort: a failure here must not abort the run."""
    if not pid_file:
        return
    try:
        import win32process
        _, pid = win32process.GetWindowThreadProcessId(app.Hwnd)
        if pid:
            with open(pid_file, "w") as fh:
                fh.write(str(pid))
    except Exception:
        pass


def _to_jsonable(v):
    """COM read -> JSON-safe. Numerics/strings/bools/None pass; CVErr ints pass
    as ints (parent maps them); anything exotic (e.g. pywintypes datetime) -> str."""
    if v is None or isinstance(v, (bool, int, float, str)):
        return v
    return str(v)


def _new_app():
    import pythoncom
    from win32com.client import DispatchEx
    pythoncom.CoInitialize()
    app = DispatchEx("Excel.Application")  # dedicated instance (own process)
    app.Visible = False
    app.DisplayAlerts = False
    app.EnableEvents = False
    try:
        app.AskToUpdateLinks = False
    except Exception:
        pass
    try:
        app.AlertBeforeOverwriting = False
    except Exception:
        pass
    return app


def _set_iter(app, job):
    app.Iteration = True
    app.MaxIterations = int(job.get("max_iterations", 100))
    app.MaxChange = float(job.get("max_change", 0.001))
    app.Calculation = XL_CALCULATION_AUTOMATIC


def _open(app, path):
    ap = os.path.abspath(path)
    if not os.path.exists(ap):
        _fail(f"workbook not found: {ap}", 1)
    wb = app.Workbooks.Open(ap, UpdateLinks=0, ReadOnly=False)
    if wb.ReadOnly:
        _fail(f"workbook opened READ-ONLY (already open / locked?): {ap}", 1)
    try:
        if not os.path.samefile(wb.FullName, ap):
            _fail(f"opened wrong workbook: {wb.FullName} != {ap}", 1)
    except OSError:
        pass  # samefile can fail on some shares; FullName check is best-effort
    return wb


def op_version():
    app = None
    try:
        app = _new_app()
        print(json.dumps({"excel_version": str(app.Version)}))
    finally:
        if app is not None:
            try:
                app.Quit()
            except Exception:
                pass


def op_recalc(job):
    app = wb = None
    try:
        app = _new_app()
        _claim_pid(app, job.get("pid_file"))
        wb = _open(app, job["path"])
        _set_iter(app, job)
        app.CalculateFullRebuild()
        wb.Save()
        wb.Close(SaveChanges=False)
        wb = None
        print(json.dumps({"ok": True}))
    finally:
        _teardown(app, wb)


def op_sweep(job):
    import itertools
    app = wb = None
    try:
        app = _new_app()
        _claim_pid(app, job.get("pid_file"))
        wb = _open(app, job["path"])
        _set_iter(app, job)

        axes = job["axes"]            # [{sheet, cell, values}]
        reads = job["reads"]          # ["Sheet!Cell", ...]
        value_lists = [a["values"] for a in axes]

        states = []
        for combo in itertools.product(*value_lists):
            for ax, val in zip(axes, combo):
                wb.Worksheets(ax["sheet"]).Range(ax["cell"]).Value = val
            app.CalculateFullRebuild()
            row = []
            for ref in reads:
                sheet, cell = ref.split("!")
                row.append(_to_jsonable(wb.Worksheets(sheet).Range(cell).Value))
            states.append(row)

        # restore declared default state, recalc, SAVE (refresh freeze cols), close
        for d in job.get("default_state", []):
            wb.Worksheets(d["sheet"]).Range(d["cell"]).Value = d["value"]
        app.CalculateFullRebuild()
        wb.Save()
        wb.Close(SaveChanges=False)
        wb = None
        print(json.dumps({"states": states, "default_restored": True}))
    finally:
        _teardown(app, wb)


def _teardown(app, wb):
    if wb is not None:
        try:
            wb.Close(SaveChanges=False)
        except Exception:
            pass
    if app is not None:
        try:
            app.Quit()
        except Exception:
            pass
    try:
        import pythoncom
        pythoncom.CoUninitialize()
    except Exception:
        pass


def main():
    try:
        job = json.loads(sys.stdin.read())
    except Exception as e:
        _fail(f"bad job json: {e}", 1)

    # Importing pywin32 is what proves COM is available; failure here => exit 3.
    try:
        import pythoncom  # noqa: F401
        import win32com.client  # noqa: F401
    except Exception as e:
        _fail(f"pywin32/COM not available: {e}", 3)

    op = job.get("op")
    try:
        if op == "version":
            op_version()
        elif op == "recalc":
            op_recalc(job)
        elif op == "sweep":
            op_sweep(job)
        else:
            _fail(f"unknown op: {op!r}", 1)
    except SystemExit:
        raise
    except Exception as e:
        # COM "Excel not installed" style errors surface here on first use.
        msg = str(e)
        code = 3 if ("Excel.Application" in msg or "Invalid class string" in msg
                     or "CO_E_" in msg) else 1
        _fail(f"{type(e).__name__}: {msg}", code)


if __name__ == "__main__":
    main()
