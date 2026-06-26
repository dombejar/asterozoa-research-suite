#!/usr/bin/env python3
"""Unit tests for model_gate.g02_oracle — the real-Excel oracle / Linux fail-honest gate.

Run: python3 -m unittest discover -s skills/model-builder/tests -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import model_gate as mg  # noqa: E402
import excel_oracle as eo  # noqa: E402

DARWIN_EV = {"oracle": "excel", "oracle_platform": "darwin",
             "oracle_backend": "applescript", "schema_version": 2}
WIN_EV = {"oracle": "excel", "oracle_platform": "win32",
          "oracle_backend": "com", "schema_version": 2}


def blocks(findings):
    return [f for f in findings if f.severity == "BLOCK"]


class TestG02HostLinuxFailHonest(unittest.TestCase):
    def test_linux_host_blocks_even_with_valid_evidence(self):
        f = mg.g02_oracle(DARWIN_EV, DARWIN_EV, demo=False, test_mode=False,
                          host_platform="linux")
        b = blocks(f)
        self.assertTrue(b)
        self.assertTrue(any("without a real Excel oracle" in x.message for x in b))

    def test_darwin_host_with_stamped_evidence_passes(self):
        f = mg.g02_oracle(DARWIN_EV, DARWIN_EV, demo=False, test_mode=False,
                          host_platform="darwin")
        self.assertFalse(blocks(f))

    def test_win32_host_with_stamped_evidence_passes(self):
        f = mg.g02_oracle(WIN_EV, WIN_EV, demo=False, test_mode=False,
                          host_platform="win32")
        self.assertFalse(blocks(f))

    def test_cross_platform_evidence_ok(self):
        # build on Windows, gate on Mac: host has oracle, evidence is real -> OK
        f = mg.g02_oracle(WIN_EV, WIN_EV, demo=False, test_mode=False,
                          host_platform="darwin")
        self.assertFalse(blocks(f))


class TestG02ProvenanceStamp(unittest.TestCase):
    def test_missing_stamp_blocks(self):
        stale = {"path": "x.xlsx"}  # no oracle stamp
        f = mg.g02_oracle(stale, stale, demo=False, test_mode=False,
                          host_platform="darwin")
        self.assertTrue(blocks(f))

    def test_forged_platform_blocks(self):
        forged = {"oracle_platform": "linux", "oracle_backend": "libreoffice"}
        f = mg.g02_oracle(forged, forged, demo=False, test_mode=False,
                          host_platform="darwin")
        self.assertTrue(blocks(f))

    def test_one_missing_evidence_does_not_itself_block(self):
        # absence is gated by G21/G49, not G02; G02 only checks provenance of
        # evidence that IS present.
        f = mg.g02_oracle(DARWIN_EV, None, demo=False, test_mode=False,
                          host_platform="darwin")
        self.assertFalse(blocks(f))

    def test_mismatched_pair_blocks(self):
        # darwin+com is NOT an exact valid pair (darwin->applescript, win32->com)
        bad = {"oracle": "excel", "oracle_platform": "darwin",
               "oracle_backend": "com", "schema_version": 2}
        f = mg.g02_oracle(bad, bad, demo=False, test_mode=False,
                          host_platform="darwin")
        self.assertTrue(blocks(f))

    def test_missing_schema_version_blocks(self):
        nover = {"oracle": "excel", "oracle_platform": "darwin",
                 "oracle_backend": "applescript"}  # no schema_version
        f = mg.g02_oracle(nover, nover, demo=False, test_mode=False,
                          host_platform="darwin")
        self.assertTrue(blocks(f))

    def test_oracle_not_excel_blocks(self):
        notexcel = {"oracle": "libreoffice", "oracle_platform": "darwin",
                    "oracle_backend": "applescript", "schema_version": 2}
        f = mg.g02_oracle(notexcel, notexcel, demo=False, test_mode=False,
                          host_platform="darwin")
        self.assertTrue(blocks(f))


class TestOracleStampMatchesGate(unittest.TestCase):
    def test_stamp_emits_schema_2_and_exact_pairs(self):
        for plat, backend in (("darwin", "applescript"), ("win32", "com")):
            st = eo.oracle_stamp(platform=plat)
            self.assertEqual(st["schema_version"], mg.EXPECTED_ORACLE_SCHEMA)
            self.assertEqual(st["schema_version"], 2)
            self.assertEqual(st["oracle"], "excel")
            self.assertEqual(st["oracle_platform"], plat)
            self.assertEqual(st["oracle_backend"], backend)
            self.assertIn((st["oracle_platform"], st["oracle_backend"]),
                          mg.VALID_ORACLE_PAIRS)
            # a stamp produced by oracle_stamp must PASS g02 on a matching host
            f = mg.g02_oracle(st, st, demo=False, test_mode=False, host_platform=plat)
            self.assertFalse(blocks(f))


class TestG02DemoTestSkip(unittest.TestCase):
    def test_demo_skips(self):
        f = mg.g02_oracle(None, None, demo=True, test_mode=False, host_platform="linux")
        self.assertFalse(blocks(f))

    def test_test_mode_skips(self):
        f = mg.g02_oracle(None, None, demo=False, test_mode=True, host_platform="linux")
        self.assertFalse(blocks(f))


if __name__ == "__main__":
    unittest.main()
