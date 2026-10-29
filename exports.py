"""
CareerConnect — Exports Module
Generates CSV downloads from live SQLite data.
"""

import io
import csv
from typing import Optional
from pathlib import Path
from datetime import datetime

from database import (
    get_all_registrations,
    get_channel_counts,
    get_referral_counts,
    get_daily_registrations,
    get_registration_count,
)
from config import REGISTRATION_TARGET, CAMPAIGN_BUDGET_INR


def _make_csv_bytes(headers: list, rows: list) -> bytes:
    """Write a CSV to an in-memory bytes buffer."""
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)
    return buf.getvalue().encode("utf-8-sig")  # BOM for Excel compatibility


# ---------------------------------------------------------------------------
# Individual Exports
# ---------------------------------------------------------------------------

def export_registrations_csv(
    include_personal: bool = True,
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> bytes:
    """
    Export workshop registrations.
    Set include_personal=False for an analytical export without student names/email.
    """
    records = get_all_registrations(include_synthetic=not only_real, db_path=db_path)

    if include_personal:
        headers = [
            "ID",
            "Student Name",
            "Email",
            "College",
            "Branch",
            "Graduation Year",
            "Channel",
            "Referral Code",
            "Consent Given",
            "Registered At (UTC)",
            "Is Synthetic",
        ]
        rows = [
            [
                r["id"],
                r["student_name"],
                r["normalized_email"],
                r["college_name"],
                r["branch"],
                r["graduation_year"],
                r["acquisition_channel"],
                r["referral_code"] or "",
                "Yes" if r["consent_acknowledged"] else "No",
                r["registered_at"],
                "Yes" if r["is_synthetic"] else "No",
            ]
            for r in records
        ]
    else:
        # Analytical export — no PII
        headers = [
            "ID",
            "College",
            "Branch",
            "Graduation Year",
            "Channel",
            "Referral Code",
            "Registered At (UTC)",
            "Is Synthetic",
        ]
        rows = [
            [
                r["id"],
                r["college_name"],
                r["branch"],
                r["graduation_year"],
                r["acquisition_channel"],
                r["referral_code"] or "",
                r["registered_at"],
                "Yes" if r["is_synthetic"] else "No",
            ]
            for r in records
        ]

    return _make_csv_bytes(headers, rows)


def export_channel_performance_csv(
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> bytes:
    """Export registrations per acquisition channel."""
    data = get_channel_counts(only_real=only_real, db_path=db_path)
    total = sum(r["count"] for r in data)

    headers = ["Channel", "Registrations", "Percentage of Total"]
    rows = [
        [
            r["channel"],
            r["count"],
            f"{(r['count']/total*100):.1f}%" if total > 0 else "N/A",
        ]
        for r in data
    ]
    return _make_csv_bytes(headers, rows)


def export_referral_performance_csv(
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> bytes:
    """Export registrations per referral code."""
    data = get_referral_counts(only_real=only_real, db_path=db_path)
    total = get_registration_count(only_real=only_real, db_path=db_path)

    headers = ["Referral Code", "Registrations", "% of All Registrations"]
    rows = [
        [
            r["code"],
            r["count"],
            f"{(r['count']/total*100):.1f}%" if total > 0 else "N/A",
        ]
        for r in data
    ]
    return _make_csv_bytes(headers, rows)


def export_daily_summary_csv(
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> bytes:
    """Export daily registration counts with running total."""
    data = get_daily_registrations(only_real=only_real, db_path=db_path)
    headers = ["Date", "New Registrations", "Running Total", "Remaining to Target"]
    rows = []
    running = 0
    for entry in data:
        running += entry["count"]
        remaining = max(REGISTRATION_TARGET - running, 0)
        rows.append([entry["date"], entry["count"], running, remaining])
    return _make_csv_bytes(headers, rows)


def export_campaign_metrics_csv(
    expenditure_inr: float = 0.0,
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> bytes:
    """Export a campaign metrics summary."""
    total = get_registration_count(only_real=only_real, db_path=db_path)
    target = REGISTRATION_TARGET
    remaining = max(target - total, 0)
    pct = round((total / target) * 100, 1) if target > 0 else 0.0

    if total > 0 and expenditure_inr > 0:
        cpr = f"₹{expenditure_inr/total:.2f}"
    else:
        cpr = "N/A"

    generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    headers = ["Metric", "Value", "Notes"]
    rows = [
        ["Total Unique Registrations", total, "Excluding synthetic records" if only_real else "Including synthetic records"],
        ["Registration Target", target, "Campaign goal"],
        ["Remaining to Target", remaining, "max(500 - total, 0)"],
        ["Target Completion (%)", f"{pct}%", "(total / 500) × 100"],
        ["Campaign Budget (INR)", f"₹{CAMPAIGN_BUDGET_INR}", "Maximum available"],
        ["Expenditure (INR)", f"₹{expenditure_inr:.2f}", "Actual spend recorded"],
        ["Cost per Registration", cpr, "expenditure / registrations, or N/A"],
        ["Report Generated At", generated_at, "UTC"],
    ]
    return _make_csv_bytes(headers, rows)

