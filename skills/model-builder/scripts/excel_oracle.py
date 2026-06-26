#!/usr/bin/env python3
"""excel_oracle.py — OS-dispatch layer for the real-Excel recalc oracle.

Excel is the ONLY recalc oracle (no LibreOffice, no formula library). This module
hides the per-OS transport behind two high-level operations that recalc.py and
audit_model.py call:

    recalc_once(path)                       # atomic: open -> iterative calc ->
                                            #   full rebuild -> save -> close
    run_sweep(path, axes, reads,            # one Excel session across the whole
              default_state)                #   scenario grid; returns typed reads
                                            #   per state, then restores default +
                                            #   saves + closes

Backends (chosen by sys.platform):
    darwin  -> AppleScript via osascript (the original, preserved verbatim)
    win32   -> COM via a worker subprocess (_excel_worker_win.py) with a hard
               parent-side timeout + owned-instance zombie cleanup
    else    -> NoExcelError  (Linux: model can be DRAFTED but the ship-gate is
               honestly unavailable; research + drafting still work)

Both backends return UNIFORM typed values (see normalize_value): numbers stay
numbers, blank cells -> None, Excel errors -> canonical literals ('#REF!' ...).
The COM backend converts CVErr variant ints to those literals; the AppleScript
backend coerces its string reads. So downstream code never branches on OS.

Exit-code contract (callers map RuntimeError/NoExcelError -> exit 2):
    NoExcelError   no real-Excel oracle on this host (env/OS failure)
    OracleError    Excel ran but failed (open/recalc/save/lock) — env failure
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

# Canonical Excel error literals (the same set recalc.py/audit_model.py scan for).
ERROR_LITERALS = ("#REF!", "#VALUE!", "#DIV/0!", "#NAME?", "#N/A", "#NUM!", "#NULL!")

SCHEMA_VERSION = 2

# Iterative-calc settings — the valuation-freeze pattern needs these (identical to
# the original AppleScript block). Shared by both backends so Mac/Win match.
ITER_MAX_ITERATIONS = 100
ITER_MAX_CHANGE = 0.001

# Hard timeout (seconds) for a single Excel operation — matches the original
# osascript timeout=600. The COM worker runs the whole sweep in ONE subprocess so
# this bounds the entire grid, not one state.
OP_TIMEOUT = 600

# xlCVErr code -> canonical literal. Excel returns cell errors over COM as VT_ERROR
# variants; win32com surfaces them as ints. Two shapes appear in the wild:
#   small code  : the xlCVErr enum (2000-2043)
#   variant int : 0x800A0000 | code, surfaced signed (e.g. -2146826281 == #DIV/0!)
_CVERR_SMALL = {
    2000: "#NULL!",
    2007: "#DIV/0!",
    2015: "#VALUE!",
    2023: "#REF!",
    2029: "#NAME?",
    2036: "#NUM!",
    2042: "#N/A",
    2043: "#N/A",   # xlErrGettingData -> surfaces as #N/A to the user
}
_VARIANT_BASE = -2147483648 + 0x000A0000  # 0x800A0000 as signed 32-bit


class NoExcelError(RuntimeError):
    """No real-Excel oracle is available on this host (wrong OS, or Excel absent)."""


class OracleError(RuntimeError):
    """Excel is present but the operation failed (open/recalc/save/lock/timeout)."""


# --------------------------------------------------------------------- dispatch

def backend_for_platform(platform: str) -> str:
    """Map sys.platform -> backend name, or raise NoExcelError (fail-honest)."""
    if platform == "darwin":
        return "applescript"
    if platform == "win32":
        return "com"
    raise NoExcelError(
        f"No real-Excel recalc oracle on this platform ({platform!r}). "
        "The model can be DRAFTED here, but it is NOT ship-eligible: the "
        "Excel recalc/sweep ship-gate needs macOS or Windows with Microsoft "
        "Excel. Research and model drafting still work. (No LibreOffice "
        "fallback by design.)"
    )


def current_backend() -> str:
    return backend_for_platform(sys.platform)


# ------------------------------------------------------------------ value norm

def cverr_to_literal(code: int):
    """COM CVErr code (small enum or 0x800A variant int) -> canonical literal,
    or None when the int is not a known Excel error code."""
    if code in _CVERR_SMALL:
        return _CVERR_SMALL[code]
    # variant int: 0x800A0000 | xlCVErr  -> recover the low code
    if code < 0:
        low = code - _VARIANT_BASE
        if low in _CVERR_SMALL:
            return _CVERR_SMALL[low]
    return None


def _coerce_str(s: str):
    """Coerce an AppleScript string read to int/float when numeric, else keep the
    stripped string (error literals + named states stay strings)."""
    t = s.strip()
    if t in ERROR_LITERALS:
        return t
    try:
        f = float(t)
        return int(f) if f.is_integer() else f
    except ValueError:
        return t


def normalize_value(raw):
    """Uniform typed value from a raw oracle read (COM native OR AppleScript str).

    bool stays bool; int/float pass through UNLESS the int is a CVErr variant
    (then -> literal); None stays None; an error-literal string passes through; a
    CVErr small-code int -> literal; any other string is coerced (numeric strings
    from AppleScript -> numbers, named states stay strings)."""
    if isinstance(raw, bool):
        return raw
    if isinstance(raw, int):
        lit = cverr_to_literal(raw)
        return lit if lit is not None else raw
    if isinstance(raw, float):
        return raw
    if raw is None:
        return None
    if isinstance(raw, str):
        if raw.strip() in ERROR_LITERALS:
            return raw.strip()
        return _coerce_str(raw)
    return raw


# ------------------------------------------------------------------ evidence

def oracle_stamp(platform: str | None = None, excel_version: str | None = None) -> dict:
    """Provenance stamp merged into recalc/sweep evidence. model_gate's
    oracle-stamp gate reads oracle_platform + oracle_backend to prove the
    evidence came from a real Excel oracle (closes Linux stale-evidence
    fake-green). Raises NoExcelError on a no-Excel platform."""
    platform = platform or sys.platform
    backend = backend_for_platform(platform)  # raises on Linux/unknown
    return {
        "schema_version": SCHEMA_VERSION,
        "oracle": "excel",
        "oracle_backend": backend,
        "oracle_platform": platform,
        "excel_version": excel_version,
    }


# ------------------------------------------------------------------ AppleScript

def _osa(lines: list[str]) -> str:
    # `with timeout` lifts AppleScript's default 120s AppleEvent limit so a long
    # `calculate full rebuild` doesn't raise -1712; the subprocess timeout
    # (OP_TIMEOUT) is the real outer bound.
    body = "\n".join("\t\t" + l for l in lines)
    script = (
        'tell application "Microsoft Excel"\n'
        f"\twith timeout of {OP_TIMEOUT} seconds\n"
        f"{body}\n"
        "\tend timeout\n"
        "end tell"
    )
    proc = subprocess.run(["osascript", "-e", script], capture_output=True,
                          text=True, timeout=OP_TIMEOUT)
    if proc.returncode != 0:
        raise OracleError(f"osascript failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def _as_quote(val) -> str:
    """Render a Python value as an AppleScript literal for set-value. Strings are
    escaped (quotes/backslashes) so values with quotes don't break the script."""
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        return str(val)
    return _as_lit(val)


def _as_lit(s) -> str:
    """Escape an ARBITRARY string as an AppleScript double-quoted literal
    (backslash + double-quote). Used for the workbook path and every interpolated
    worksheet name so a path/sheet containing a quote can't break or inject the
    script. Cell refs ("D5") are regex-bounded and safe, but escaping is harmless."""
    s = str(s).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def _excel_version_applescript():
    try:
        return _osa(["return version as string"]) or None
    except Exception:
        return None


def _recalc_applescript(path: Path) -> None:
    _osa([
        f"open POSIX file {_as_lit(path)}",
        "set wb to active workbook",
        "set iteration to true",
        f"set max iterations to {ITER_MAX_ITERATIONS}",
        f"set max change to {ITER_MAX_CHANGE}",
        "set calculation to calculation automatic",
        "calculate full rebuild",
        "save wb",
        "close wb saving no",
    ])


def _sweep_applescript(path: Path, axes, reads, default_state) -> dict:
    """axes: [(sheet, cell, [values...]), ...]; reads: ["Sheet!Cell", ...];
    default_state: [(sheet, cell, value), ...]. Returns {"states":[[v,...]], ...}
    with values normalized."""
    import itertools

    # Capture the opened workbook's NAME once, then reference `workbook <name>`
    # explicitly in EVERY subsequent call. Using `active workbook` across many
    # separate osascript invocations is fragile — if Excel activates another
    # workbook between calls the sweep silently writes/reads the wrong file.
    wb_name = _osa([f"open POSIX file {_as_lit(path)}",
                    "set iteration to true",
                    f"set max iterations to {ITER_MAX_ITERATIONS}",
                    f"set max change to {ITER_MAX_CHANGE}",
                    "set calculation to calculation automatic",
                    "return name of active workbook"])
    wbref = f"workbook {_as_lit(wb_name)}"

    # ASCII Unit Separator (US, 0x1F): a delimiter that cannot appear in Excel
    # numeric/text outputs, so a value containing '|' no longer corrupts the
    # per-state read alignment. Joined in AppleScript via (ASCII character 31).
    SEP = "\x1f"

    state_reads = []
    for combo in itertools.product(*[vals for _, _, vals in axes]):
        lines = []
        for (sheet, cell, _), val in zip(axes, combo):
            lines.append(f'set value of range "{cell}" of worksheet {_as_lit(sheet)} '
                         f"of {wbref} to {_as_quote(val)}")
        lines.append("calculate full rebuild")
        getters = []
        for ref in reads:
            s, c = ref.split("!")
            getters.append(f'(get value of range "{c}" of worksheet {_as_lit(s)} '
                           f"of {wbref})")
        lines.append("return ("
                     + " & (ASCII character 31) & ".join(getters)
                     + ") as string")
        raw = _osa(lines).split(SEP)
        state_reads.append([normalize_value(v) for v in raw])

    restore = []
    for sheet, cell, val in default_state:
        restore.append(f'set value of range "{cell}" of worksheet {_as_lit(sheet)} '
                       f"of {wbref} to {_as_quote(val)}")
    restore += ["calculate full rebuild", f"save {wbref}",
                f"close {wbref} saving no"]
    _osa(restore)
    return {"states": state_reads, "default_restored": True}


# ------------------------------------------------------------------ COM (win32)

def _worker_path() -> Path:
    return Path(__file__).resolve().parent / "_excel_worker_win.py"


def _run_worker(job: dict) -> dict:
    """Run the COM worker subprocess with a hard parent-side timeout. On timeout
    the worker's owned-Excel PID (written to job['pid_file']) is killed so a hung
    run never leaves a zombie Excel holding the file — and ONLY that owned
    instance, never a user's other Excel session."""
    import os
    import tempfile

    pid_file = Path(tempfile.mkstemp(prefix="asterozoa-excel-pid-", suffix=".txt")[1])
    job = dict(job, pid_file=str(pid_file))
    try:
        proc = subprocess.run(
            [sys.executable, str(_worker_path())],
            input=json.dumps(job), capture_output=True, text=True,
            timeout=OP_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        _kill_owned_excel(pid_file)
        raise OracleError(
            f"Excel COM operation exceeded {OP_TIMEOUT}s and was killed "
            "(modal dialog, recalc hang, or protected-view prompt?)")
    finally:
        owned = _read_pid(pid_file)
        try:
            pid_file.unlink()
        except OSError:
            pass
    if proc.returncode != 0:
        # worker prints a structured error on stdout when it can; fall back to stderr
        detail = proc.stdout.strip() or proc.stderr.strip()
        # a clean worker exit-3 means "no Excel / COM unavailable" -> NoExcelError
        if proc.returncode == 3:
            raise NoExcelError(detail or "Microsoft Excel not available via COM")
        raise OracleError(detail or f"Excel worker failed (rc={proc.returncode})")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise OracleError(f"Excel worker returned non-JSON: {proc.stdout[:200]}")


def _read_pid(pid_file: Path):
    try:
        return int(pid_file.read_text().strip())
    except (OSError, ValueError):
        return None


def _kill_owned_excel(pid_file: Path) -> None:
    pid = _read_pid(pid_file)
    if pid is None:
        return  # worker died before claiming an instance; nothing owned to kill
    try:
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                       capture_output=True, text=True, timeout=30)
    except Exception:
        pass


def _recalc_com(path: Path) -> None:
    _run_worker({"op": "recalc", "path": str(path),
                 "max_iterations": ITER_MAX_ITERATIONS, "max_change": ITER_MAX_CHANGE})


def _sweep_com(path: Path, axes, reads, default_state) -> dict:
    job = {
        "op": "sweep",
        "path": str(path),
        "max_iterations": ITER_MAX_ITERATIONS,
        "max_change": ITER_MAX_CHANGE,
        "axes": [{"sheet": s, "cell": c, "values": list(v)} for s, c, v in axes],
        "reads": list(reads),
        "default_state": [{"sheet": s, "cell": c, "value": v}
                          for s, c, v in default_state],
    }
    out = _run_worker(job)
    # worker returns raw per-state reads; normalize here so the COM CVErr ints
    # become canonical literals uniformly with the AppleScript path.
    states = [[normalize_value(v) for v in st] for st in out["states"]]
    return {"states": states, "default_restored": out.get("default_restored", True)}


def _excel_version_com():
    try:
        out = _run_worker({"op": "version"})
        return out.get("excel_version")
    except Exception:
        return None


# ------------------------------------------------------------------ public API

def excel_version() -> str | None:
    """Best-effort Excel version string for the evidence stamp (None on failure)."""
    b = current_backend()
    return _excel_version_applescript() if b == "applescript" else _excel_version_com()


def recalc_once(path: Path) -> None:
    """Open the workbook in real Excel, force a full iterative rebuild, save, close.
    Raises NoExcelError (no oracle) / OracleError (Excel failed)."""
    path = Path(path)
    b = current_backend()  # raises NoExcelError on Linux
    if b == "applescript":
        _recalc_applescript(path)
    else:
        _recalc_com(path)


def run_sweep(path: Path, axes, reads, default_state) -> dict:
    """Drive Excel across the full scenario grid in ONE session.

    axes:          [(sheet, cell, [typed values...]), ...]
    reads:         ["Sheet!Cell", ...]  (outputs + min-cash + covenant refs)
    default_state: [(sheet, cell, typed value), ...]
    Returns {"states": [[normalized read, ...] per Cartesian state],
             "default_restored": True}. After the grid it restores default_state,
    recalcs, and SAVES (refreshing valuation-freeze columns) before closing."""
    path = Path(path)
    b = current_backend()  # raises NoExcelError on Linux
    if b == "applescript":
        return _sweep_applescript(path, axes, reads, default_state)
    return _sweep_com(path, axes, reads, default_state)
