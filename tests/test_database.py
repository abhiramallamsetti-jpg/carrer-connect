"""
Tests for database initialization and basic operations.
Uses a temporary SQLite database so production data is never affected.
"""

import tempfile
import os
import unittest
from pathlib import Path

# Allow imports from project root
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import (
    init_db,
    register_student,
    email_already_registered,
    get_all_registrations,
    get_registration_count,
    get_channel_counts,
    get_daily_registrations,
    get_all_referral_codes,
    referral_code_exists,
    add_referral_code,
    normalize_email,
    seed_opportunities,
    get_opportunities,
)
from config import DEFAULT_REFERRAL_CODES, SAMPLE_OPPORTUNITIES


class TempDBMixin:
    """Provides a fresh temporary database for each test."""

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


class TestDatabaseInit(TempDBMixin, unittest.TestCase):

    def test_init_creates_tables(self):
        """Database tables must exist after init_db."""
        from database import get_connection
        with get_connection(self.db_path) as conn:
            tables = {
                r[0]
                for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            }
        self.assertIn("registrations", tables)
        self.assertIn("referral_codes", tables)
        self.assertIn("opportunities", tables)
        self.assertIn("campaign_events", tables)

    def test_init_seeds_referral_codes(self):
        """Default referral codes must be present after init_db."""
        codes = get_all_referral_codes(db_path=self.db_path)
        code_values = {c["code"].upper() for c in codes}
        for entry in DEFAULT_REFERRAL_CODES:
            self.assertIn(entry["code"].upper(), code_values)

    def test_reinit_preserves_data(self):
        """Calling init_db a second time must not delete existing data."""
        register_student(
            "Alice", "alice@example.com", "IIT", "CSE", 2025,
            "WhatsApp", db_path=self.db_path,
        )
        init_db(self.db_path)  # Second call
        self.assertEqual(get_registration_count(db_path=self.db_path), 1)


class TestRegistrations(TempDBMixin, unittest.TestCase):

    def _reg(self, name="Alice", email="alice@example.com", **kwargs):
        defaults = dict(
            college_name="IIT Hyderabad",
            branch="CSE",
            graduation_year=2025,
            acquisition_channel="WhatsApp",
        )
        defaults.update(kwargs)
        return register_student(name, email, db_path=self.db_path, **defaults)

    def test_successful_registration(self):
        result = self._reg()
        self.assertTrue(result["success"])
        self.assertIn("id", result)

    def test_registration_count_increments(self):
        self.assertEqual(get_registration_count(db_path=self.db_path), 0)
        self._reg()
        self.assertEqual(get_registration_count(db_path=self.db_path), 1)
        self._reg("Bob", "bob@example.com")
        self.assertEqual(get_registration_count(db_path=self.db_path), 2)

    def test_duplicate_email_rejected(self):
        self._reg()
        result2 = self._reg()  # Same email
        self.assertFalse(result2["success"])
        self.assertEqual(result2["error"], "duplicate_email")

    def test_email_case_insensitive_dedup(self):
        """Registration with differently-cased email must be rejected as duplicate."""
        self._reg(email="Alice@Example.COM")
        result = self._reg(email="alice@example.com")
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "duplicate_email")

    def test_consent_stored(self):
        self._reg(consent_acknowledged=True)
        recs = get_all_registrations(db_path=self.db_path)
        self.assertEqual(recs[0]["consent_acknowledged"], 1)

    def test_get_all_registrations(self):
        self._reg("Alice", "alice@ex.com")
        self._reg("Bob", "bob@ex.com")
        all_r = get_all_registrations(db_path=self.db_path)
        self.assertEqual(len(all_r), 2)

    def test_synthetic_records_excluded_from_real_count(self):
        self._reg("Synth", "synth@ex.com", is_synthetic=True)
        self._reg("Real", "real@ex.com", is_synthetic=False)
        self.assertEqual(get_registration_count(only_real=True, db_path=self.db_path), 1)
        self.assertEqual(get_registration_count(only_real=False, db_path=self.db_path), 2)

    def test_channel_counts(self):
        self._reg("A", "a@x.com", acquisition_channel="WhatsApp")
        self._reg("B", "b@x.com", acquisition_channel="LinkedIn")
        self._reg("C", "c@x.com", acquisition_channel="WhatsApp")
        counts = {r["channel"]: r["count"] for r in get_channel_counts(db_path=self.db_path)}
        self.assertEqual(counts["WhatsApp"], 2)
        self.assertEqual(counts["LinkedIn"], 1)

    def test_daily_registrations(self):
        self._reg()
        daily = get_daily_registrations(db_path=self.db_path)
        self.assertGreater(len(daily), 0)
        self.assertIn("date", daily[0])
        self.assertIn("count", daily[0])

    def test_registration_stored_fields(self):
        self._reg("TestUser", "testuser@college.edu",
                  college_name="BITS Pilani", branch="ECE",
                  graduation_year=2026, acquisition_channel="Telegram")
        recs = get_all_registrations(db_path=self.db_path)
        r = recs[0]
        self.assertEqual(r["student_name"], "TestUser")
        self.assertEqual(r["normalized_email"], "testuser@college.edu")
        self.assertEqual(r["college_name"], "BITS Pilani")
        self.assertEqual(r["branch"], "ECE")
        self.assertEqual(r["graduation_year"], 2026)
        self.assertEqual(r["acquisition_channel"], "Telegram")


class TestEmailAlreadyRegistered(TempDBMixin, unittest.TestCase):

    def test_returns_false_for_new_email(self):
        self.assertFalse(email_already_registered("new@user.com", db_path=self.db_path))

    def test_returns_true_after_registration(self):
        register_student("A", "a@b.com", "College", "CSE", 2025, "WhatsApp", db_path=self.db_path)
        self.assertTrue(email_already_registered("a@b.com", db_path=self.db_path))

    def test_case_insensitive(self):
        register_student("A", "a@b.com", "College", "CSE", 2025, "WhatsApp", db_path=self.db_path)
        self.assertTrue(email_already_registered("A@B.COM", db_path=self.db_path))


class TestEmailNormalization(unittest.TestCase):

    def test_lowercase(self):
        self.assertEqual(normalize_email("User@Example.COM"), "user@example.com")

    def test_strips_whitespace(self):
        self.assertEqual(normalize_email("  user@example.com  "), "user@example.com")

    def test_already_normalized(self):
        self.assertEqual(normalize_email("user@example.com"), "user@example.com")


class TestReferralHandling(TempDBMixin, unittest.TestCase):

    def test_valid_referral_attributed(self):
        """A valid referral code should be stored with the registration."""
        code = "CAMPUS01"
        result = register_student(
            "Ref User", "refuser@ex.com", "College", "CSE", 2025,
            "College Clubs", referral_code=code, db_path=self.db_path,
        )
        self.assertTrue(result["success"])
        recs = get_all_registrations(db_path=self.db_path)
        self.assertEqual(recs[0]["referral_code"], code)

    def test_invalid_referral_silently_discarded(self):
        """An invalid referral code must not block registration; code stored as None."""
        result = register_student(
            "No Ref", "noref@ex.com", "College", "CSE", 2025,
            "WhatsApp", referral_code="BADCODE999", db_path=self.db_path,
        )
        self.assertTrue(result["success"])
        recs = get_all_registrations(db_path=self.db_path)
        self.assertIsNone(recs[0]["referral_code"])

    def test_add_referral_code(self):
        ok = add_referral_code("NEWCODE01", "Test Code", "WhatsApp", db_path=self.db_path)
        self.assertTrue(ok)
        self.assertTrue(referral_code_exists("NEWCODE01", db_path=self.db_path))

    def test_duplicate_referral_code_rejected(self):
        add_referral_code("DUPETEST", db_path=self.db_path)
        ok2 = add_referral_code("DUPETEST", db_path=self.db_path)
        self.assertFalse(ok2)

    def test_referral_code_case_insensitive_lookup(self):
        self.assertTrue(referral_code_exists("campus01", db_path=self.db_path))
        self.assertTrue(referral_code_exists("CAMPUS01", db_path=self.db_path))


class TestOpportunities(TempDBMixin, unittest.TestCase):

    def test_seed_opportunities(self):
        seed_opportunities(SAMPLE_OPPORTUNITIES, db_path=self.db_path)
        opps = get_opportunities(db_path=self.db_path)
        self.assertEqual(len(opps), len(SAMPLE_OPPORTUNITIES))

    def test_seed_idempotent(self):
        seed_opportunities(SAMPLE_OPPORTUNITIES, db_path=self.db_path)
        seed_opportunities(SAMPLE_OPPORTUNITIES, db_path=self.db_path)  # Should not duplicate
        opps = get_opportunities(db_path=self.db_path)
        self.assertEqual(len(opps), len(SAMPLE_OPPORTUNITIES))

    def test_search_by_title(self):
        seed_opportunities(SAMPLE_OPPORTUNITIES, db_path=self.db_path)
        opps = get_opportunities(search="Data", db_path=self.db_path)
        self.assertGreater(len(opps), 0)
        for o in opps:
            found = (
                "data" in o["title"].lower()
                or "data" in o["company"].lower()
                or "data" in o["skills"].lower()
            )
            self.assertTrue(found)

    def test_filter_by_type(self):
        seed_opportunities(SAMPLE_OPPORTUNITIES, db_path=self.db_path)
        opps = get_opportunities(opp_type="Internship", db_path=self.db_path)
        self.assertGreater(len(opps), 0)
        for o in opps:
            self.assertEqual(o["opp_type"], "Internship")


class TestEmptyDatabase(TempDBMixin, unittest.TestCase):
    """All queries should handle an empty database without errors."""

    def test_empty_registration_count(self):
        self.assertEqual(get_registration_count(db_path=self.db_path), 0)

    def test_empty_channel_counts(self):
        self.assertEqual(get_channel_counts(db_path=self.db_path), [])

    def test_empty_daily_registrations(self):
        self.assertEqual(get_daily_registrations(db_path=self.db_path), [])

    def test_empty_all_registrations(self):
        self.assertEqual(get_all_registrations(db_path=self.db_path), [])

    def test_empty_opportunities(self):
        self.assertEqual(get_opportunities(db_path=self.db_path), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)

