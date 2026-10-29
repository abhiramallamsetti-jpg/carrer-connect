"""
CareerConnect — Referrals Module
Referral code helpers and shareable promotional message generation.
"""

from typing import Optional, Dict, Any
from pathlib import Path

from database import (
    get_all_referral_codes,
    referral_code_exists,
    add_referral_code,
    get_referral_counts,
)


# ---------------------------------------------------------------------------
# Shareable Message Generator
# ---------------------------------------------------------------------------

REGISTRATION_URL_PLACEHOLDER = "[REGISTRATION_URL]"


def generate_referral_message(
    referral_code: str,
    registration_url: str = REGISTRATION_URL_PLACEHOLDER,
) -> str:
    """Return a pre-formatted WhatsApp/Telegram sharing message."""
    return (
        f"🚀 *Free AI Workshop for Engineering Students!*\n\n"
        f"📌 *Build Your First AI Project in 60 Minutes*\n\n"
        f"✅ Free | ✅ Online | ✅ Beginner-friendly\n\n"
        f"👉 Register here: {registration_url}?ref={referral_code}\n\n"
        f"Use referral code: *{referral_code}*\n\n"
        f"Perfect for final-year engineering students exploring AI and career opportunities.\n\n"
        f"_Details such as date, time, and speaker will be confirmed by the organiser. "
        f"Verify before registering._"
    )


def generate_linkedin_message(
    referral_code: str,
    registration_url: str = REGISTRATION_URL_PLACEHOLDER,
) -> str:
    """Return a LinkedIn post draft."""
    return (
        f"🎯 Calling all final-year engineering students!\n\n"
        f"I came across a free online workshop — "
        f"\"Build Your First AI Project in 60 Minutes\" — "
        f"that looks like a great starting point for anyone curious about AI.\n\n"
        f"It's beginner-friendly and designed for students like us who want "
        f"practical experience with AI development.\n\n"
        f"🔗 Register (free): {registration_url}?ref={referral_code}\n\n"
        f"#AI #Engineering #StudentLife #FreeWorkshop #CareerGrowth\n\n"
        f"_(Workshop details to be confirmed by the organiser.)_"
    )


# ---------------------------------------------------------------------------
# Referral Performance Summary
# ---------------------------------------------------------------------------

def get_referral_summary(db_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Return a summary dict of referral code performance.
    """
    codes = get_all_referral_codes(db_path=db_path)
    counts = {r["code"]: r["count"] for r in get_referral_counts(db_path=db_path)}

    summary = []
    total_via_referral = 0
    for code_row in codes:
        code = code_row["code"]
        count = counts.get(code, 0)
        total_via_referral += count
        summary.append(
            {
                "code": code,
                "description": code_row["description"],
                "channel": code_row["channel"],
                "registrations": count,
                "message": generate_referral_message(code),
                "linkedin_message": generate_linkedin_message(code),
            }
        )

    return {
        "codes": summary,
        "total_via_referral": total_via_referral,
    }


# ---------------------------------------------------------------------------
# URL Query Parameter Parsing (for auto-fill)
# ---------------------------------------------------------------------------

def extract_referral_from_params(query_params: Dict[str, Any]) -> Optional[str]:
    """
    Extract the referral code from URL query parameters.
    Supports both ?ref=CODE and ?referral=CODE.
    Returns None if not present or invalid.
    """
    code = query_params.get("ref") or query_params.get("referral")
    if not code:
        return None
    if isinstance(code, list):
        code = code[0]
    return str(code).strip().upper() or None

