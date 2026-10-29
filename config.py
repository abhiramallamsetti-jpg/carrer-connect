"""
CareerConnect — Configuration Module
Central configuration for the CareerConnect platform.
"""

import os
from pathlib import Path

# ──────────────────────────────────────────────
# Project Identity
# ──────────────────────────────────────────────
APP_NAME = "CareerConnect"
APP_TAGLINE = "Discover Opportunities. Build Skills. Grow Your Career."
APP_VERSION = "1.0.0"

# ──────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
DELIVERABLES_DIR = BASE_DIR / "deliverables"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)
DELIVERABLES_DIR.mkdir(exist_ok=True)

# Database
DB_PATH = DATA_DIR / "careerconnect.db"

# ──────────────────────────────────────────────
# Workshop Details
# ──────────────────────────────────────────────
WORKSHOP_TITLE = "Build Your First AI Project in 60 Minutes"
WORKSHOP_DESCRIPTION = (
    "Explore how to approach a practical AI project in a beginner-friendly "
    "online workshop designed for engineering students."
)
WORKSHOP_AUDIENCE = "Final-year engineering students interested in practical AI projects and career development."

# ──────────────────────────────────────────────
# Campaign Targets
# ──────────────────────────────────────────────
REGISTRATION_TARGET = 500
CAMPAIGN_BUDGET_INR = 2000
CAMPAIGN_DURATION_DAYS = 7

# ──────────────────────────────────────────────
# Acquisition Channels
# ──────────────────────────────────────────────
ACQUISITION_CHANNELS = [
    "WhatsApp",
    "LinkedIn",
    "Telegram",
    "College Clubs",
    "Student Referral",
    "Other",
]

# ──────────────────────────────────────────────
# Default Referral Codes (for demonstration)
# ──────────────────────────────────────────────
DEFAULT_REFERRAL_CODES = [
    {"code": "CAMPUS01", "description": "Campus Ambassador Demo Code", "channel": "College Clubs"},
    {"code": "WHATSAPP01", "description": "WhatsApp Campaign Demo Code", "channel": "WhatsApp"},
    {"code": "TELEGRAM01", "description": "Telegram Campaign Demo Code", "channel": "Telegram"},
    {"code": "LINKEDIN01", "description": "LinkedIn Campaign Demo Code", "channel": "LinkedIn"},
]

# ──────────────────────────────────────────────
# Admin Access (local development only)
# ──────────────────────────────────────────────
# In production, use environment variables.
# For local demo, default password is used ONLY if env var is not set.
ADMIN_PASSWORD_ENV_VAR = "CAREERCONNECT_ADMIN_PASSWORD"
DEFAULT_ADMIN_PASSWORD = "admin123"  # Local demo only — change for any deployment

def get_admin_password() -> str:
    """Return the admin password from environment or fallback to demo default."""
    return os.environ.get(ADMIN_PASSWORD_ENV_VAR, DEFAULT_ADMIN_PASSWORD)

# ──────────────────────────────────────────────
# Engineering Branches
# ──────────────────────────────────────────────
ENGINEERING_BRANCHES = [
    "Computer Science Engineering (CSE)",
    "Information Technology (IT)",
    "Electronics & Communication (ECE)",
    "Electrical Engineering (EE)",
    "Mechanical Engineering (ME)",
    "Civil Engineering (CE)",
    "Artificial Intelligence & ML",
    "Data Science",
    "Other",
]

# ──────────────────────────────────────────────
# Graduation Years
# ──────────────────────────────────────────────
VALID_GRADUATION_YEARS = list(range(2025, 2031))

# ──────────────────────────────────────────────
# Sample Opportunities (for demonstration)
# ──────────────────────────────────────────────
SAMPLE_OPPORTUNITIES = [
    {
        "title": "Software Development Intern",
        "company": "Sample Tech Corp",
        "type": "Internship",
        "skills": "Python, JavaScript, SQL",
        "eligibility": "Final-year B.Tech/B.E. students",
        "location": "Remote",
        "deadline": "To be confirmed",
        "apply_link": "",
        "description": "Work on real-world software projects and gain hands-on experience with modern development practices.",
        "is_sample": True,
    },
    {
        "title": "Data Analyst — Entry Level",
        "company": "Sample Analytics Inc.",
        "type": "Full-time",
        "skills": "Python, Pandas, SQL, Tableau",
        "eligibility": "2025–2027 graduates with analytics coursework",
        "location": "Bangalore (Hybrid)",
        "deadline": "To be confirmed",
        "apply_link": "",
        "description": "Analyze datasets to generate actionable insights for business stakeholders.",
        "is_sample": True,
    },
    {
        "title": "AI/ML Research Intern",
        "company": "Sample Research Labs",
        "type": "Internship",
        "skills": "Python, TensorFlow/PyTorch, Mathematics",
        "eligibility": "Pre-final & final-year CSE/AI/DS students",
        "location": "Remote",
        "deadline": "To be confirmed",
        "apply_link": "",
        "description": "Contribute to cutting-edge machine learning research projects under expert mentorship.",
        "is_sample": True,
    },
    {
        "title": "Frontend Developer",
        "company": "Sample Web Solutions",
        "type": "Full-time",
        "skills": "React, TypeScript, CSS, Figma",
        "eligibility": "2025–2026 graduates",
        "location": "Hyderabad (On-site)",
        "deadline": "To be confirmed",
        "apply_link": "",
        "description": "Build beautiful, responsive user interfaces for enterprise web applications.",
        "is_sample": True,
    },
    {
        "title": "Cloud Engineering Intern",
        "company": "Sample Cloud Services",
        "type": "Internship",
        "skills": "AWS/Azure, Linux, Docker, Python",
        "eligibility": "Final-year B.Tech students with cloud fundamentals",
        "location": "Remote",
        "deadline": "To be confirmed",
        "apply_link": "",
        "description": "Learn cloud infrastructure management and DevOps practices in a production environment.",
        "is_sample": True,
    },
    {
        "title": "Cybersecurity Analyst Trainee",
        "company": "Sample SecureTech",
        "type": "Full-time",
        "skills": "Networking, Linux, Python, Security Tools",
        "eligibility": "2025–2027 CSE/IT graduates",
        "location": "Chennai (Hybrid)",
        "deadline": "To be confirmed",
        "apply_link": "",
        "description": "Monitor, detect, and respond to security incidents as part of a SOC team.",
        "is_sample": True,
    },
]

# ──────────────────────────────────────────────
# Brand Colors (used in Streamlit custom CSS)
# ──────────────────────────────────────────────
COLORS = {
    "primary": "#6C63FF",
    "primary_dark": "#5A52D5",
    "secondary": "#00C9A7",
    "accent": "#FF6B6B",
    "bg_dark": "#0E1117",
    "bg_card": "#1A1D23",
    "bg_card_hover": "#22262E",
    "text_primary": "#FFFFFF",
    "text_secondary": "#B0B8C1",
    "border": "#2D3139",
    "success": "#00C9A7",
    "warning": "#FFB347",
    "error": "#FF6B6B",
    "info": "#6C63FF",
}
