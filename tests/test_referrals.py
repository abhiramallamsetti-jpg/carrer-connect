"""
Tests for referral module functions.
"""

import tempfile
import os
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import init_db, register_student, get_referral_counts
from referrals import (
    generate_referral_message,
    generate_linkedin_message,
    get_referral_summary,
    extract_referral_from_params,
)


class TempDBMixin:
    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = Path(self._tmp.name)
        self._tmp.close()
        init_db(self.db_path)

    def tearDown(self):
        try:
            os.unlink(self.db_path)
        except OSError:
            pass


class TestMessageGeneration(unittest.TestCase):

    def test_referral_message_contains_code(self):
        msg = generate_referral_message("CAMPUS01")
        self.assertIn("CAMPUS01", msg)

    def test_referral_message_contains_url_placeholder(self):
        msg = generate_referral_message("CAMPUS01")
        self.assertIn("?ref=CAMPUS01", msg)

    def test_linkedin_message_contains_code(self):
        msg = generate_linkedin_message("LINKEDIN01")
        self.assertIn("LINKEDIN01", msg)

    def test_custom_url_used(self):
        msg = generate_referral_message("CODE01", "https://myapp.com")
        self.assertIn("https://myapp.com", msg)


class TestReferralSummary(TempDBMixin, unittest.TestCase):

    def test_summary_contains_all_default_codes(self):
        from config import DEFAULT_REFERRAL_CODES
        summary = get_referral_summary(db_path=self.db_path)
        codes = {e["code"] for e in summary["codes"]}
        for entry in DEFAULT_REFERRAL_CODES:
            self.assertIn(entry["code"], codes)

    def test_referral_count_zero_initially(self):
        summary = get_referral_summary(db_path=self.db_path)
        for entry in summary["codes"]:
            self.assertEqual(entry["registrations"], 0)

    def test_referral_count_increments(self):
        register_student(
            "RefUser", "refuser@x.com", "Col", "CSE", 2025,
            "College Clubs", referral_code="CAMPUS01",
            db_path=self.db_path,
        )
        summary = get_referral_summary(db_path=self.db_path)
        entry = next(e for e in summary["codes"] if e["code"] == "CAMPUS01")
        self.assertEqual(entry["registrations"], 1)


class TestExtractReferralFromParams(unittest.TestCase):

    def test_ref_param(self):
        self.assertEqual(extract_referral_from_params({"ref": "CAMPUS01"}), "CAMPUS01")

    def test_referral_param(self):
        self.assertEqual(extract_referral_from_params({"referral": "WHATSAPP01"}), "WHATSAPP01")

    def test_uppercase_conversion(self):
        self.assertEqual(extract_referral_from_params({"ref": "campus01"}), "CAMPUS01")

    def test_missing_param_returns_none(self):
        self.assertIsNone(extract_referral_from_params({}))

    def test_empty_string_returns_none(self):
        self.assertIsNone(extract_referral_from_params({"ref": ""}))


if __name__ == "__main__":
    unittest.main(verbosity=2)

