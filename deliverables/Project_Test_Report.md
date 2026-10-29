# Project Test Report
## CareerConnect — NxtWave Growth Intern Challenge

**Generated:** 2026-10-29  
**Python version:** 3.11.9  
**pytest version:** 8.3.3  
**Platform:** Windows 11

---

## Test Summary

| Category | Tests | Passed | Failed | Skipped |
|----------|-------|--------|--------|---------|
| Database (init & schema) | 3 | 3 | 0 | 0 |
| Registration logic | 10 | 10 | 0 | 0 |
| Email checks | 3 | 3 | 0 | 0 |
| Email normalisation | 3 | 3 | 0 | 0 |
| Referral handling | 5 | 5 | 0 | 0 |
| Opportunities | 4 | 4 | 0 | 0 |
| Empty database | 5 | 5 | 0 | 0 |
| Analytics metrics | 4 | 4 | 0 | 0 |
| Cost per registration | 4 | 4 | 0 | 0 |
| Referral messages | 4 | 4 | 0 | 0 |
| Referral summary | 3 | 3 | 0 | 0 |
| URL param extraction | 5 | 5 | 0 | 0 |
| CSV exports (empty DB) | 5 | 5 | 0 | 0 |
| CSV exports (with data) | 7 | 7 | 0 | 0 |
| **TOTAL** | **65** | **65** | **0** | **0** |

**Result: 65/65 PASSED in 1.68 seconds**

---

## Test Files

| File | Description |
|------|-------------|
| `tests/test_database.py` | DB init, registrations, email dedup, referrals, opportunities, empty DB |
| `tests/test_analytics.py` | Target completion, remaining calc, cost-per-registration, synthetic exclusion |
| `tests/test_referrals.py` | Message generation, referral summary, URL param extraction |
| `tests/test_exports.py` | All 6 CSV export types on empty and populated databases |

---

## Key Behaviors Verified

### Registration
- [x] Successful registration saves all fields to SQLite
- [x] Duplicate email rejected with `duplicate_email` error code
- [x] Email case-insensitive deduplication (`Alice@Example.COM` = `alice@example.com`)
- [x] Invalid referral code silently discarded (registration proceeds)
- [x] Valid referral code stored with registration
- [x] Synthetic records excluded from real registration count
- [x] Consent flag stored correctly
- [x] All required fields stored (name, email, college, branch, year, channel)

### Database
- [x] All four tables created on `init_db()`
- [x] Default referral codes seeded (CAMPUS01, WHATSAPP01, TELEGRAM01, LINKEDIN01)
- [x] Second call to `init_db()` preserves existing data
- [x] Parameterized queries used throughout (no string interpolation)

### Analytics
- [x] Zero-registration state returns correct defaults
- [x] Completion % formula: (total / 500) × 100
- [x] Remaining formula: max(500 − total, 0) — never negative
- [x] Cost per registration returns "N/A" when denominator is zero
- [x] Synthetic records excluded from real metrics

### Referrals
- [x] Default codes present after DB init
- [x] Referral count increments when code is used in registration
- [x] Message generation includes code and URL
- [x] URL param extraction (`?ref=CODE`) with uppercase normalisation
- [x] Invalid or empty ref param returns None

### CSV Exports
- [x] All 6 export types return valid CSV on empty database
- [x] Full export includes student name and email
- [x] Analytical export excludes student name and email
- [x] Channel export shows all channels used
- [x] Referral export shows codes used
- [x] Daily export includes running total column
- [x] Metrics export shows total registration count
- [x] BOM (utf-8-sig) encoding applied for Excel compatibility

---

## How to Run Tests

```powershell
# From the project root directory:
python -m pytest tests/ -v

# Run a single test file:
python -m pytest tests/test_database.py -v

# Run with coverage (if pytest-cov is installed):
python -m pytest tests/ -v --cov=. --cov-report=term-missing
```

---

## Limitations and Notes

1. **Streamlit UI is not tested.** The Streamlit interface requires a running browser and cannot be easily unit-tested without Playwright or Selenium. All business logic has been separated into testable modules (`database.py`, `analytics.py`, `referrals.py`, `exports.py`) so that the core behaviour is verified independently of the UI.

2. **All tests use temporary SQLite databases.** Each test class creates a fresh database in a temporary file and deletes it after the test. Production data is never touched.

3. **No integration tests against the live app.** Full end-to-end testing (e.g., simulating a browser form submission and verifying the database update) would require a browser automation tool. This is documented as a known limitation and a next step.

4. **The `asyncio_default_fixture_loop_scope` warning** from `pytest-asyncio` is cosmetic — it does not indicate a test failure and does not affect CareerConnect (which does not use async fixtures).

---

*Test results above were obtained by running `python -m pytest tests/ -v` in the project root on Windows 11 with Python 3.11.9.*

