"""
CareerConnect — Analytics Module
Computes campaign metrics and KPIs from the database.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path

from config import REGISTRATION_TARGET
from database import (
    get_registration_count,
    get_channel_counts,
    get_referral_counts,
    get_daily_registrations,
    get_branch_counts,
    get_graduation_year_counts,
    get_recent_registrations,
)


def compute_campaign_metrics(
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Return a dictionary of campaign KPIs computed from the live database.

    All metrics are derived from stored registrations — never hardcoded.
    """
    total = get_registration_count(only_real=only_real, db_path=db_path)
    target = REGISTRATION_TARGET
    remaining = max(target - total, 0)

    if target > 0:
        completion_pct = round((total / target) * 100, 1)
    else:
        completion_pct = 0.0

    channel_data = get_channel_counts(only_real=only_real, db_path=db_path)
    referral_data = get_referral_counts(only_real=only_real, db_path=db_path)
    daily_data = get_daily_registrations(only_real=only_real, db_path=db_path)
    branch_data = get_branch_counts(only_real=only_real, db_path=db_path)
    year_data = get_graduation_year_counts(only_real=only_real, db_path=db_path)
    recent = get_recent_registrations(n=10, only_real=only_real, db_path=db_path)

    referral_total = sum(r["count"] for r in referral_data)
    organic_total = total - referral_total

    return {
        "total_registrations": total,
        "target": target,
        "remaining": remaining,
        "completion_pct": completion_pct,
        "referral_total": referral_total,
        "organic_total": organic_total,
        "channel_data": channel_data,
        "referral_data": referral_data,
        "daily_data": daily_data,
        "branch_data": branch_data,
        "year_data": year_data,
        "recent_registrations": recent,
    }


def compute_cost_per_registration(
    expenditure_inr: float,
    registrations: int,
) -> str:
    """Return cost per registration as a formatted string, or 'N/A' if zero."""
    if registrations <= 0 or expenditure_inr <= 0:
        return "N/A"
    cpr = expenditure_inr / registrations
    return f"₹{cpr:.2f}"


# ──────────────────────────────────────────────
# Proposed Experiment Definitions
# ──────────────────────────────────────────────

PROPOSED_EXPERIMENTS: List[Dict[str, Any]] = [
    {
        "id": "EXP-01",
        "name": "Message Variation Test",
        "hypothesis": (
            "A message emphasizing a hands-on, 60-minute format will produce a "
            "higher registration click-through rate than a message emphasizing "
            "career benefits alone."
        ),
        "variable": "WhatsApp promotional message wording",
        "variants": [
            "Variant A: Emphasises '60-minute hands-on AI project' (action-focused)",
            "Variant B: Emphasises 'Boost your career with AI skills' (outcome-focused)",
        ],
        "success_metric": "Registration conversion rate per message variant",
        "minimum_data": "≥ 50 clicks per variant to observe a meaningful difference",
        "action_if_positive": "Scale the winning variant to all remaining communities",
        "action_if_negative": "Test a third variant combining both messages",
        "status": "Proposed — not yet executed",
    },
    {
        "id": "EXP-02",
        "name": "Channel Attribution Comparison",
        "hypothesis": (
            "WhatsApp college communities will deliver more registrations per "
            "outreach message than LinkedIn posts during the first three days."
        ),
        "variable": "Acquisition channel (WhatsApp vs LinkedIn)",
        "variants": [
            "Variant A: WhatsApp community posts with referral code WHATSAPP01",
            "Variant B: LinkedIn posts/articles with referral code LINKEDIN01",
        ],
        "success_metric": "Registrations attributed per channel (tracked via referral code)",
        "minimum_data": "≥ 30 registrations per channel for initial comparison",
        "action_if_positive": "Increase effort on the higher-performing channel",
        "action_if_negative": (
            "Investigate message quality and posting time; try Telegram as a "
            "comparison channel"
        ),
        "status": "Proposed — not yet executed",
    },
]


def get_channel_target_allocation() -> List[Dict[str, Any]]:
    """Return the proposed registration allocation per channel."""
    return [
        {
            "channel": "WhatsApp Communities",
            "proposed_target": 180,
            "referral_code": "WHATSAPP01",
            "notes": "Largest reach; high engagement in engineering student groups",
        },
        {
            "channel": "LinkedIn",
            "proposed_target": 100,
            "referral_code": "LINKEDIN01",
            "notes": "Professional audience; good for final-year students job-seeking",
        },
        {
            "channel": "Telegram Communities",
            "proposed_target": 100,
            "referral_code": "TELEGRAM01",
            "notes": "Active tech student communities; easy to share links",
        },
        {
            "channel": "College Clubs & Referrals",
            "proposed_target": 120,
            "referral_code": "CAMPUS01",
            "notes": "High-trust channel; student coordinators drive personal referrals",
        },
    ]

