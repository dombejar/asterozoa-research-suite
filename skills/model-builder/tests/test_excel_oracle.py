#!/usr/bin/env python3
"""Unit tests for excel_oracle.py — the OS-dispatch Excel oracle.

Pure-logic tests (no real Excel): backend dispatch, value normalization, the
COM CVErr->literal map, and the evidence oracle-stamp. The real-Excel recalc/
sweep behaviour is validated separately on macOS (AppleScript) and Windows (COM).

Run: python3 -m unittest discover -s skills/model-builder/tests -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import excel_oracle as eo  # noqa: E402


class TestBackendDispatch(unittest.TestCase):
    def test_darwin_is_applescript(self):
        self.assertEqual(eo.backend_for_platform("darwin"), "applescript")

    def test_win32_is_com(self):
        self.assertEqual(eo.backend_for_platform("win32"), "com")

    def test_linux_raises_no_excel(self):
        with self.assertRaises(eo.NoExcelError):
            eo.backend_for_platform("linux")

    def test_unknown_raises_no_excel(self):
        with self.assertRaises(eo.NoExcelError):
            eo.backend_for_platform("aix7")

    def test_no_excel_message_is_honest(self):
        """The fail-honest message must say draft-ok but not ship-eligible, and
        must not OFFER LibreOffice as a usable fallback (only deny one)."""
        try:
            eo.backend_for_platform("linux")
        except eo.NoExcelError as e:
            msg = str(e).lower()
            self.assertIn("not ship", msg)
            # may mention libreoffice only to DENY it, never to offer it
            if "libreoffice" in msg:
                self.assertIn("no libreoffice", msg)
        else:
            self.fail("expected NoExcelError")


class TestCVErrMapping(unittest.TestCase):
    """COM returns cell errors as CVErr variant ints, NOT '#REF!' strings.
    Both the small xlCVErr codes (2000-2043) and the 0x800A07Dx variant ints
    must map to the canonical literals."""

    def test_small_codes(self):
        self.assertEqual(eo.cverr_to_literal(2007), "#DIV/0!")
        self.assertEqual(eo.cverr_to_literal(2042), "#N/A")
        self.assertEqual(eo.cverr_to_literal(2029), "#NAME?")
        self.assertEqual(eo.cverr_to_literal(2000), "#NULL!")
        self.assertEqual(eo.cverr_to_literal(2036), "#NUM!")
        self.assertEqual(eo.cverr_to_literal(2023), "#REF!")
        self.assertEqual(eo.cverr_to_literal(2015), "#VALUE!")

    def test_variant_ints(self):
        # 0x800A0000 | code, surfaced by win32com as a signed 32-bit int.
        # 0x800A07D7 (xlErrDiv0=2007) -> signed -2146826281
        self.assertEqual(eo.cverr_to_literal(-2146826281), "#DIV/0!")
        # 0x800A07E7 (xlErrRef=2023) -> signed -2146826265
        self.assertEqual(eo.cverr_to_literal(-2146826265), "#REF!")

    def test_unknown_code_returns_none(self):
        self.assertIsNone(eo.cverr_to_literal(12345))


class TestNormalizeValue(unittest.TestCase):
    """normalize_value turns a raw oracle read (COM native or AppleScript string)
    into the uniform typed form audit_model + recalc consume: numbers stay
    numbers, blanks -> None, error variants/literals -> canonical literal str."""

    def test_numbers_passthrough(self):
        self.assertEqual(eo.normalize_value(3), 3)
        self.assertEqual(eo.normalize_value(3.5), 3.5)

    def test_none_passthrough(self):
        self.assertIsNone(eo.normalize_value(None))

    def test_bool_passthrough(self):
        self.assertIs(eo.normalize_value(True), True)

    def test_error_literal_string_passthrough(self):
        self.assertEqual(eo.normalize_value("#REF!"), "#REF!")

    def test_cverr_int_becomes_literal(self):
        self.assertEqual(eo.normalize_value(-2146826281), "#DIV/0!")

    def test_plain_string_passthrough(self):
        self.assertEqual(eo.normalize_value("Base"), "Base")

    def test_applescript_numeric_string_coerced(self):
        # AppleScript get-value returns strings; numeric ones coerce to number.
        self.assertEqual(eo.normalize_value("2"), 2)
        self.assertEqual(eo.normalize_value("3.14"), 3.14)


class TestOracleStamp(unittest.TestCase):
    def test_darwin_stamp(self):
        s = eo.oracle_stamp("darwin")
        self.assertEqual(s["oracle"], "excel")
        self.assertEqual(s["oracle_backend"], "applescript")
        self.assertEqual(s["oracle_platform"], "darwin")
        self.assertIn("schema_version", s)

    def test_win32_stamp(self):
        s = eo.oracle_stamp("win32")
        self.assertEqual(s["oracle_backend"], "com")
        self.assertEqual(s["oracle_platform"], "win32")

    def test_linux_stamp_raises(self):
        with self.assertRaises(eo.NoExcelError):
            eo.oracle_stamp("linux")


if __name__ == "__main__":
    unittest.main()
