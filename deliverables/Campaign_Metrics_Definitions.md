# Campaign Metrics Definitions
## CareerConnect — NxtWave Growth Intern Challenge

This document defines all metrics used in the CareerConnect dashboard and exports.

---

## Core Registration Metrics

### Total Unique Registrations
**Formula:** `COUNT(*) FROM registrations WHERE is_synthetic = 0`

**Meaning:** The number of distinct students who have completed the workshop registration form with a valid email address and given consent. Duplicate email addresses are rejected at insert time, so this count is always unique.

**Source:** Live SQLite database

---

### Registration Target
**Value:** 500

**Meaning:** The challenge objective — 500 unique final-year engineering student registrations within 7 days.

---

### Target Completion Percentage
**Formula:**
```
completion_pct = (total_unique_registrations / 500) × 100
```

**Example:** 250 registrations → 50.0%

**Note:** Capped conceptually at 100% if registrations exceed the target (though the formula is not clamped — exceeding 500 would show > 100%).

---

### Remaining Registrations
**Formula:**
```
remaining = max(500 − total_unique_registrations, 0)
```

**Note:** The `max(..., 0)` ensures this metric is never negative, even if registrations exceed the target.

---

## Channel Metrics

### Registrations by Acquisition Channel
**Formula:** `COUNT(*) GROUP BY acquisition_channel WHERE is_synthetic = 0`

**Channels tracked:** WhatsApp, LinkedIn, Telegram, College Clubs, Student Referral, Other

**Attribution rule:** The channel is whatever the student selected in the registration form. If a referral code is also present, both the channel (form field) and the code are recorded independently.

---

### Channel Conversion Rate
**Formula:**
```
channel_conversion_rate = registrations_from_channel / reach_via_channel × 100
```

**⚠️ Limitation:** `reach_via_channel` (how many people actually saw the message on each channel) is not automatically tracked. This metric can only be calculated if manual reach data is recorded separately. When reach data is unavailable, display "N/A" rather than inventing a number.

---

## Referral Metrics

### Registrations by Referral Code
**Formula:** `COUNT(*) GROUP BY referral_code WHERE referral_code IS NOT NULL AND is_synthetic = 0`

**Attribution rule:** The referral code stored is the *validated* code — if a student submitted an invalid code, it is stored as NULL.

### Total Referral Registrations
**Formula:** `SUM(count) for all referral_code groups`

### Organic Registrations (no referral code)
**Formula:** `total_registrations − referral_registrations`

---

## Cost Metrics

### Cost per Registration
**Formula:**
```
cost_per_registration = campaign_expenditure_INR / total_unique_registrations
```

**Edge cases:**
- If `total_unique_registrations = 0`: display "N/A" (avoid division by zero)
- If `campaign_expenditure_INR = 0`: display "N/A" (no spend has occurred)

**Note:** This metric is only meaningful when real campaign expenditure data is available and recorded.

---

## Daily Metrics

### New Registrations per Day
**Formula:** `COUNT(*) GROUP BY DATE(registered_at) WHERE is_synthetic = 0`

### Running Total
**Formula:** Cumulative sum of `new_registrations` ordered by date

### Remaining on Each Day
**Formula:** `max(500 − running_total, 0)` per day

---

## Data Quality Metrics

### Duplicate Rejection Rate
**Formula:**
```
duplicate_rate = rejected_duplicate_attempts / total_registration_attempts × 100
```

**⚠️ Limitation:** Rejected duplicates are not currently stored in a separate table. The rejection is enforced by the SQLite `UNIQUE` constraint. To track this metric, rejected attempts would need to be logged in `campaign_events`.

---

## Synthetic Data Label

Any record where `is_synthetic = 1` in the `registrations` table was inserted programmatically for demonstration purposes. All live dashboard metrics and CSV exports default to `WHERE is_synthetic = 0` (real records only). The dashboard clearly labels which records are synthetic.

---

## Definitions Summary Table

| Metric | Formula | Data Source | Zero-Safe? |
|--------|---------|------------|-----------|
| Total registrations | COUNT(*) WHERE is_synthetic=0 | DB | Yes (returns 0) |
| Completion % | total / 500 × 100 | DB | Yes (returns 0.0%) |
| Remaining | max(500 − total, 0) | DB | Yes (returns 500) |
| Referral total | SUM of referral counts | DB | Yes (returns 0) |
| Organic total | total − referral_total | DB | Yes (returns 0) |
| Cost per registration | spend / total | Manual + DB | Displays "N/A" |
| Channel conversion rate | channel_regs / reach × 100 | DB + Manual | Displays "N/A" |

---

*Last updated: 2026-10-29. All formulas are implemented in `analytics.py` and `exports.py`.*

