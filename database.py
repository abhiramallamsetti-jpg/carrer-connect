"""
CareerConnect — Database Module
Handles SQLite initialization, schema management, and all database operations.
Uses parameterized queries throughout to prevent SQL injection.
"""

import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

from config import DB_PATH, DEFAULT_REFERRAL_CODES

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------------

@contextmanager
def get_connection(db_path: Optional[Path] = None):
    """Yield a SQLite connection with row_factory set to Row."""
    path = str(db_path or DB_PATH)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS referral_codes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    code        TEXT    NOT NULL UNIQUE COLLATE NOCASE,
    description TEXT,
    channel     TEXT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS registrations (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name       TEXT    NOT NULL,
    normalized_email   TEXT    NOT NULL UNIQUE COLLATE NOCASE,
    college_name       TEXT    NOT NULL,
    branch             TEXT    NOT NULL,
    graduation_year    INTEGER NOT NULL,
    acquisition_channel TEXT   NOT NULL,
    referral_code      TEXT,
    consent_acknowledged INTEGER NOT NULL DEFAULT 0,
    registered_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    is_synthetic       INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (referral_code) REFERENCES referral_codes(code)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS opportunities (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    company     TEXT NOT NULL,
    opp_type    TEXT,
    skills      TEXT,
    eligibility TEXT,
    location    TEXT,
    deadline    TEXT,
    apply_link  TEXT,
    description TEXT,
    is_sample   INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS campaign_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type  TEXT NOT NULL,
    channel     TEXT,
    details     TEXT,
    recorded_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_registrations_channel
    ON registrations (acquisition_channel);
CREATE INDEX IF NOT EXISTS idx_registrations_referral
    ON registrations (referral_code);
CREATE INDEX IF NOT EXISTS idx_registrations_date
    ON registrations (registered_at);
"""


def init_db(db_path: Optional[Path] = None) -> None:
    """
    Initialize the database: create tables and seed default referral codes.
    Safe to call on every startup — existing data is preserved.
    """
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA_SQL)

        # Seed default referral codes (ignore conflicts)
        for entry in DEFAULT_REFERRAL_CODES:
            conn.execute(
                """INSERT OR IGNORE INTO referral_codes (code, description, channel)
                   VALUES (?, ?, ?)""",
                (entry["code"], entry["description"], entry["channel"]),
            )

    logger.info("Database initialised at %s", db_path or DB_PATH)


# ---------------------------------------------------------------------------
# Referral Code Operations
# ---------------------------------------------------------------------------

def get_all_referral_codes(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Return all referral codes."""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM referral_codes ORDER BY code"
        ).fetchall()
        return [dict(r) for r in rows]


def referral_code_exists(code: str, db_path: Optional[Path] = None) -> bool:
    """Return True if the given referral code exists (case-insensitive)."""
    with get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT 1 FROM referral_codes WHERE code = ? COLLATE NOCASE",
            (code,),
        ).fetchone()
        return row is not None


def add_referral_code(
    code: str,
    description: str = "",
    channel: str = "",
    db_path: Optional[Path] = None,
) -> bool:
    """
    Insert a new referral code. Returns True on success, False if duplicate.
    """
    try:
        with get_connection(db_path) as conn:
            conn.execute(
                "INSERT INTO referral_codes (code, description, channel) VALUES (?, ?, ?)",
                (code.upper().strip(), description.strip(), channel.strip()),
            )
        return True
    except sqlite3.IntegrityError:
        return False


# ---------------------------------------------------------------------------
# Registration Operations
# ---------------------------------------------------------------------------

def normalize_email(email: str) -> str:
    """Lowercase and strip whitespace from an email address."""
    return email.strip().lower()


def register_student(
    student_name: str,
    email: str,
    college_name: str,
    branch: str,
    graduation_year: int,
    acquisition_channel: str,
    referral_code: Optional[str] = None,
    consent_acknowledged: bool = True,
    is_synthetic: bool = False,
    db_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Insert a new workshop registration.

    Returns a dict:
        {"success": True, "id": <id>}  on success
        {"success": False, "error": <message>}  on failure
    """
    norm_email = normalize_email(email)

    # Validate referral code (if provided) — treat invalid as None
    effective_referral = None
    if referral_code and referral_code.strip():
        code_clean = referral_code.strip().upper()
        if referral_code_exists(code_clean, db_path):
            effective_referral = code_clean
        # If invalid, we silently discard it (logged below)

    try:
        with get_connection(db_path) as conn:
            cursor = conn.execute(
                """INSERT INTO registrations
                   (student_name, normalized_email, college_name, branch,
                    graduation_year, acquisition_channel, referral_code,
                    consent_acknowledged, registered_at, is_synthetic)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    student_name.strip(),
                    norm_email,
                    college_name.strip(),
                    branch.strip(),
                    int(graduation_year),
                    acquisition_channel.strip(),
                    effective_referral,
                    1 if consent_acknowledged else 0,
                    datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    1 if is_synthetic else 0,
                ),
            )
            return {"success": True, "id": cursor.lastrowid}
    except sqlite3.IntegrityError:
        return {"success": False, "error": "duplicate_email"}
    except Exception as exc:
        logger.error("Registration failed: %s", exc)
        return {"success": False, "error": str(exc)}


def email_already_registered(email: str, db_path: Optional[Path] = None) -> bool:
    """Return True if the normalised email is already in the database."""
    norm = normalize_email(email)
    with get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT 1 FROM registrations WHERE normalized_email = ?", (norm,)
        ).fetchone()
        return row is not None


def get_all_registrations(
    include_synthetic: bool = True,
    db_path: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """Return all registrations, optionally excluding synthetic records."""
    query = "SELECT * FROM registrations"
    params: tuple = ()
    if not include_synthetic:
        query += " WHERE is_synthetic = 0"
    query += " ORDER BY registered_at DESC"
    with get_connection(db_path) as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]


def get_registration_count(
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> int:
    """Return the total number of (real) registrations."""
    where = "WHERE is_synthetic = 0" if only_real else ""
    with get_connection(db_path) as conn:
        row = conn.execute(
            f"SELECT COUNT(*) as cnt FROM registrations {where}"
        ).fetchone()
        return row["cnt"] if row else 0


# ---------------------------------------------------------------------------
# Analytics Queries
# ---------------------------------------------------------------------------

def get_channel_counts(
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """Registrations grouped by acquisition channel."""
    where = "WHERE is_synthetic = 0" if only_real else ""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            f"""SELECT acquisition_channel as channel, COUNT(*) as count
                FROM registrations {where}
                GROUP BY acquisition_channel
                ORDER BY count DESC""",
        ).fetchall()
        return [dict(r) for r in rows]


def get_referral_counts(
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """Registrations grouped by referral code."""
    where = "WHERE is_synthetic = 0 AND referral_code IS NOT NULL" if only_real \
            else "WHERE referral_code IS NOT NULL"
    with get_connection(db_path) as conn:
        rows = conn.execute(
            f"""SELECT referral_code as code, COUNT(*) as count
                FROM registrations {where}
                GROUP BY referral_code
                ORDER BY count DESC""",
        ).fetchall()
        return [dict(r) for r in rows]


def get_daily_registrations(
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """Registrations grouped by date (YYYY-MM-DD)."""
    where = "WHERE is_synthetic = 0" if only_real else ""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            f"""SELECT substr(registered_at, 1, 10) as date,
                       COUNT(*) as count
                FROM registrations {where}
                GROUP BY date
                ORDER BY date ASC""",
        ).fetchall()
        return [dict(r) for r in rows]


def get_branch_counts(
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """Registrations grouped by engineering branch."""
    where = "WHERE is_synthetic = 0" if only_real else ""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            f"""SELECT branch, COUNT(*) as count
                FROM registrations {where}
                GROUP BY branch
                ORDER BY count DESC""",
        ).fetchall()
        return [dict(r) for r in rows]


def get_graduation_year_counts(
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """Registrations grouped by graduation year."""
    where = "WHERE is_synthetic = 0" if only_real else ""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            f"""SELECT graduation_year as year, COUNT(*) as count
                FROM registrations {where}
                GROUP BY graduation_year
                ORDER BY graduation_year ASC""",
        ).fetchall()
        return [dict(r) for r in rows]


def get_recent_registrations(
    n: int = 10,
    only_real: bool = True,
    db_path: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """Return the n most recent registrations."""
    where = "WHERE is_synthetic = 0" if only_real else ""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            f"""SELECT student_name, college_name, branch, graduation_year,
                       acquisition_channel, referral_code, registered_at, is_synthetic
                FROM registrations {where}
                ORDER BY registered_at DESC
                LIMIT ?""",
            (n,),
        ).fetchall()
        return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Opportunity Operations
# ---------------------------------------------------------------------------

def seed_opportunities(opportunities: List[Dict[str, Any]], db_path: Optional[Path] = None) -> None:
    """Insert sample opportunities if the table is empty."""
    with get_connection(db_path) as conn:
        count = conn.execute("SELECT COUNT(*) as cnt FROM opportunities").fetchone()["cnt"]
        if count == 0:
            for opp in opportunities:
                conn.execute(
                    """INSERT INTO opportunities
                       (title, company, opp_type, skills, eligibility,
                        location, deadline, apply_link, description, is_sample)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        opp.get("title", ""),
                        opp.get("company", ""),
                        opp.get("type", ""),
                        opp.get("skills", ""),
                        opp.get("eligibility", ""),
                        opp.get("location", ""),
                        opp.get("deadline", ""),
                        opp.get("apply_link", ""),
                        opp.get("description", ""),
                        1 if opp.get("is_sample", True) else 0,
                    ),
                )


def get_opportunities(
    search: str = "",
    opp_type: str = "",
    db_path: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """Return opportunities with optional title/company search and type filter."""
    query = "SELECT * FROM opportunities WHERE 1=1"
    params: list = []

    if search.strip():
        query += " AND (title LIKE ? OR company LIKE ? OR skills LIKE ?)"
        term = f"%{search.strip()}%"
        params.extend([term, term, term])

    if opp_type.strip() and opp_type != "All":
        query += " AND opp_type = ?"
        params.append(opp_type.strip())

    query += " ORDER BY id ASC"
    with get_connection(db_path) as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

