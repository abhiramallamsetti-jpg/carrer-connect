"""
Tests for analytics metrics computation.
"""

import tempfile
import os
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import init_db, register_student
from analytics import compute_campaign_metrics, compute_cost_per_registration
from config import REGISTRATION_TARGET


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


class TestTargetCalculations(TempDBMixin, unittest.TestCase):

    def test_zero_registrations(self):
        m = compute_campaign_metrics(db_path=self.db_path)
        self.assertEqual(m["total_registrations"], 0)
        self.assertEqual(m["target"], REGISTRATION_TARGET)
        self.assertEqual(m["remaining"], REGISTRATION_TARGET)
        self.assertEqual(m["completion_pct"], 0.0)

    def test_completion_pct_formula(self):
        """Completion % = (total / 500) * 100."""
        for i in range(5):
            register_student(
                f"Student{i}", f"s{i}@x.com",
                "College", "CSE", 2025, "WhatsApp",
                db_path=self.db_path,
            )
        m = compute_campaign_metrics(db_path=self.db_path)
        expected_pct = round((5 / REGISTRATION_TARGET) * 100, 1)
        self.assertAlmostEqual(m["completion_pct"], expected_pct, places=1)

    def test_remaining_never_negative(self):
        """remaining = max(target - total, 0) — never goes below zero."""
        # Register more than target (edge case)
        for i in range(3):
            register_student(
                f"S{i}", f"s{i}@ex.com",
                "Col", "CSE", 2025, "WhatsApp",
                db_path=self.db_path,
            )
        m = compute_campaign_metrics(db_path=self.db_path)
        self.assertGreaterEqual(m["remaining"], 0)

    def test_synthetic_excluded_from_real_metrics(self):
        register_student(
            "Synth", "synth@x.com", "Col", "CSE", 2025, "WhatsApp",
            is_synthetic=True, db_path=self.db_path,
        )
        m = compute_campaign_metrics(only_real=True, db_path=self.db_path)
        self.assertEqual(m["total_registrations"], 0)


class TestCostPerRegistration(unittest.TestCase):

    def test_zero_expenditure_returns_na(self):
        self.assertEqual(compute_cost_per_registration(0, 100), "N/A")

    def test_zero_registrations_returns_na(self):
        self.assertEqual(compute_cost_per_registration(1000, 0), "N/A")

    def test_correct_calculation(self):
        # 1000 INR / 10 registrations = ₹100.00
        result = compute_cost_per_registration(1000.0, 10)
        self.assertEqual(result, "₹100.00")

    def test_fractional_result(self):
        # 1000 / 3 ≈ ₹333.33
        result = compute_cost_per_registration(1000.0, 3)
        self.assertIn("₹", result)
        self.assertIn("333", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

