# AI + Learning Notes
## CareerConnect — NxtWave Growth Intern Challenge

---

## A. What I Asked → What AI Suggested → What I Changed

### Example 1 — Database Email Deduplication

**What I asked:**
How should I prevent the same student from registering twice for the workshop?

**What AI suggested:**
Use a `UNIQUE` constraint on the email column in SQLite. Additionally, the AI recommended normalising the email (lowercasing and stripping whitespace) *before* storing it, so that `Alice@Example.COM` and `alice@example.com` are treated as the same address. The AI also suggested using `COLLATE NOCASE` on the column for extra safety.

**What I changed / adopted:**
I implemented both recommendations:
- Added `normalized_email TEXT NOT NULL UNIQUE COLLATE NOCASE` in the `registrations` table schema.
- Added a `normalize_email()` function in `database.py` that lowercases and strips whitespace before every insert and lookup.
- Applied the same normalisation in the duplicate-check function `email_already_registered()`.

This means a student attempting to register again with a differently-cased version of their email receives a clear "already registered" message rather than a confusing database error.

---

### Example 2 — Referral Code URL Auto-Fill

**What I asked:**
Is there a way to automatically pre-fill the referral code field when someone clicks a shared link containing the referral code?

**What AI suggested:**
Use URL query parameters — specifically `?ref=CODE` — and read them from Streamlit's `st.query_params` at page load. The AI recommended stripping and uppercasing the code before validation, and displaying a confirmation banner so the user knows the code was detected.

**What I changed / adopted:**
I implemented this as described in `referrals.py` (`extract_referral_from_params()`) and used it in `app.py` on the registration page. When `?ref=CAMPUS01` is present in the URL, the referral field is pre-filled and a teal success banner confirms the detection.

I also validated the extracted code against the database before pre-filling, so invalid or fabricated codes in the URL are silently discarded rather than pre-filling an invalid value.

---

### Example 3 — CSV BOM Encoding for Excel Compatibility

**What I asked:**
My CSV downloads open correctly in a text editor but columns appear jumbled when opened in Microsoft Excel on Windows. How do I fix this?

**What AI suggested:**
Use `utf-8-sig` encoding (UTF-8 with a Byte Order Mark, BOM) when writing CSV files. The BOM tells Excel that the file is UTF-8, preventing it from misinterpreting special characters and misaligning columns.

**What I changed / adopted:**
Updated `exports.py` to encode all CSV output with `utf-8-sig`:
```python
return buf.getvalue().encode("utf-8-sig")
```
This is a small but practically important change for any Indian student or evaluator opening the exports in Excel. The fix also correctly handles special characters such as the ₹ symbol in the campaign metrics export.

---

## B. One AI Suggestion I Deliberately Rejected

### Suggestion: Add an ML-Based Job Recommender

**What was suggested:**
During planning, the AI suggested adding a machine-learning job recommendation feature — specifically, embedding student profile data (branch, skills, graduation year) and job listings into a vector space, then finding the nearest-neighbour matches using a library like `scikit-learn` or `sentence-transformers`.

**Why I did not follow it:**

1. **Out of scope for the challenge.** The NxtWave Growth Intern Challenge is about planning and demonstrating a *growth strategy for a free workshop*, not building an ML-powered job portal. Adding this feature would have distracted from the primary deliverable.

2. **Introduces unnecessary dependencies.** Installing `scikit-learn`, `torch`, or `sentence-transformers` on a Windows 11 laptop for a beginner-facing prototype adds significant download size (often 500 MB+), potential installation failures, and hardware-specific issues (GPU vs CPU). This contradicts the challenge requirement to keep the project *lightweight and easy for a beginner to run*.

3. **Sample listings are explicitly labelled as demonstrations.** Since the job listings are marked as sample data anyway, a "smart" recommendation against fake listings would produce meaningless results and could mislead users about the quality of the matches.

4. **Prototype risk.** A recommender built on synthetic data and untested embeddings could recommend irrelevant or random listings — creating a worse experience than simple keyword search.

**What alternative I chose:**
A simple text-search filter (title, company, skills) and a type dropdown. This achieves the same goal — helping a student find relevant listings — without any ML infrastructure, in a way that is transparent, fast, and reliable on any hardware.

**What I learned:**
AI suggestions often optimise for technical sophistication. In a growth challenge context, it is more valuable to ship a working, honest prototype quickly than to add impressive-sounding features that obscure the core deliverable. The right question is always: *does this feature serve the challenge objective?* In this case, it did not.

---

## C. What I Would Improve With Another 24 Hours

### 1. Test the Registration Experience with Real Users
I would recruit 5–10 engineering students (with their consent) to complete the registration form on the actual running app and note any points of confusion — unclear field labels, unexpected error messages, or friction in finding the referral code field. Usability testing with real users almost always reveals issues that automated tests and self-review miss.

### 2. Improve Channel Attribution Accuracy
Currently, attribution is single-touch (last referral code used). A student who sees the LinkedIn post, then registers via a WhatsApp group link, would be attributed entirely to WhatsApp. With more time I would implement a first-touch and last-touch attribution model, storing both in the database, so the dashboard can show a more complete picture of the acquisition journey.

### 3. A/B Test Promotional Messages on a Pilot Group
Before sending messages to all communities, I would run a small pilot — two message variations sent to two groups of similar size (with admin permission) — and compare registration rates over 24 hours. This data-driven approach prevents wasting the full outreach effort on a less effective message.

### 4. Add Basic Rate Limiting and CAPTCHA Before Public Deployment
The current form has no protection against automated form submissions. Before making the registration page publicly accessible (e.g., on Streamlit Cloud), I would add rate limiting by IP and a simple CAPTCHA to prevent fake registrations inflating the count.

### 5. Improve Accessibility
I would audit the colour contrast ratios in the custom CSS, add `aria-label` attributes where Streamlit permits, and test keyboard navigation through the registration form to ensure the application is accessible to students using screen readers or keyboard-only navigation.

### 6. Replace the Prototype Admin Password with a Proper Auth Flow
The current local authentication uses a single password from an environment variable. Before any production deployment, I would replace this with a proper authentication mechanism — at minimum, hashed passwords stored in an environment-managed secret store, ideally a session-based auth library.

### 7. Use Actual Campaign Data to Refine the Strategy
The entire growth strategy is currently *proposed* — no real campaign has been run. With another 24 hours, I would begin a small pilot outreach to one or two communities (with permission), collect real registration data, and use that to validate or revise the channel allocation before the full seven-day campaign.

---

*All descriptions above reflect actual development decisions made during this project build. No verbatim AI conversation transcripts are reproduced. Where AI suggestions were adopted, the implementation can be verified in the corresponding source files.*

