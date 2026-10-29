"""
Tests for CSV export functions.
Verifies exports work on both empty and populated databases.
"""

import tempfile
import os
import csv
import io
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import init_db, register_student
from exports import (
    export_registrations_csv,
    export_channel_performance_csv,
    export_referral_performance_csv,
    export_daily_summary_csv,
    export_campaign_metrics_csv,
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

    def _parse_csv(self, data: bytes) -> list:
        """Parse CSV bytes (with BOM) into list of dicts."""
        text = data.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))
        return list(reader)


class TestExportsEmptyDB(TempDBMixin, unittest.TestCase):
    """All exports must succeed with zero records."""

    def test_registrations_csv_empty(self):
        data = export_registrations_csv(db_path=self.db_path)
        rows = self._parse_csv(data)
        self.assertEqual(rows, [])

    def test_channel_csv_empty(self):
        data = export_channel_performance_csv(db_path=self.db_path)
        rows = self._parse_csv(data)
        self.assertEqual(rows, [])

    def test_referral_csv_empty(self):
        data = export_referral_performance_csv(db_path=self.db_path)
        rows = self._parse_csv(data)
        self.assertEqual(rows, [])

    def test_daily_csv_empty(self):
        data = export_daily_summary_csv(db_path=self.db_path)
        rows = self._parse_csv(data)
        self.assertEqual(rows, [])

    def test_campaign_metrics_csv_empty(self):
        data = export_campaign_metrics_csv(db_path=self.db_path)
        rows = self._parse_csv(data)
        # Should have header rows even with 0 registrations
        self.assertGreater(len(rows), 0)


class TestExportsWithData(TempDBMixin, unittest.TestCase):

    def setUp(self):
        super().setUp()
        register_student("Alice", "alice@x.com", "IIT", "CSE", 2025,
                         "WhatsApp", referral_code="WHATSAPP01",
                         db_path=self.db_path)
        register_student("Bob", "bob@x.com", "NIT", "ECE", 2026,
                         "LinkedIn", db_path=self.db_path)

    def test_registrations_csv_contains_data(self):
        rows = self._parse_csv(export_registrations_csv(db_path=self.db_path))
        self.assertEqual(len(rows), 2)

    def test_registrations_full_has_name(self):
        rows = self._parse_csv(
            export_registrations_csv(include_personal=True, db_path=self.db_path)
        )
        names = {r["Student Name"] for r in rows}
        self.assertIn("Alice", names)

    def test_registrations_analytical_no_email_column(self):
        rows = self._parse_csv(
            export_registrations_csv(include_personal=False, db_path=self.db_path)
        )
        self.assertGreater(len(rows), 0)
        self.assertNotIn("Email", rows[0].keys())
        self.assertNotIn("Student Name", rows[0].keys())

    def test_channel_csv_has_both_channels(self):
        rows = self._parse_csv(export_channel_performance_csv(db_path=self.db_path))
        channels = {r["Channel"] for r in rows}
        self.assertIn("WhatsApp", channels)
        self.assertIn("LinkedIn", channels)

    def test_referral_csv_has_referral(self):
        rows = self._parse_csv(export_referral_performance_csv(db_path=self.db_path))
        codes = {r["Referral Code"] for r in rows}
        self.assertIn("WHATSAPP01", codes)

    def test_daily_csv_running_total(self):
        rows = self._parse_csv(export_daily_summary_csv(db_path=self.db_path))
        self.assertGreater(len(rows), 0)
        self.assertIn("Running Total", rows[-1])

    def test_campaign_metrics_csv_shows_total(self):
        rows = self._parse_csv(export_campaign_metrics_csv(db_path=self.db_path))
        metric_row = next(
            (r for r in rows if "Total Unique" in r.get("Metric", "")), None
        )
        self.assertIsNotNone(metric_row)
        self.assertEqual(metric_row["Value"], "2")


if __name__ == "__main__":
    unittest.main(verbosity=2)

