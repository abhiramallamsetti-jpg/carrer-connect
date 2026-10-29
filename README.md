# CareerConnect 🚀
### Student Opportunities & AI Workshop Growth Platform
### NxtWave Growth Intern Challenge

> **"Discover Opportunities. Build Skills. Grow Your Career."**

---

## What Is CareerConnect?

CareerConnect is a student-focused web application built for the **NxtWave Growth Intern Challenge**. It demonstrates a practical growth strategy for promoting a free online AI workshop targeted at final-year engineering students.

The application provides:
- A workshop registration and referral tracking system
- An admin analytics dashboard
- CSV data exports
- A sample job and internship opportunity explorer
- Complete growth campaign documentation

---

## Why Was It Built?

The NxtWave Growth Intern Challenge requires designing and demonstrating a plan to achieve **500 unique workshop registrations in 7 days with a maximum budget of ₹2,000** for the free online workshop:

> **"Build Your First AI Project in 60 Minutes"**

CareerConnect is the working platform that supports this strategy — tracking registrations, attributing them to channels, and reporting on campaign progress.

> **Important:** The campaign is *proposed*, not executed. No real registrations exist in the initial build. The application demonstrates how the strategy would work if implemented.

---

## Features

| Feature | Description |
|---------|-------------|
| 🏠 Home Page | Branding, workshop banner, featured opportunities, CTA buttons |
| 💼 Opportunities | Sample job/internship listings with search and filter |
| 🤖 AI Workshop | Workshop details, FAQ, proposed topics, registration CTA |
| 📝 Registration | Validated 7-field form, SQLite persistence, duplicate prevention |
| 🔗 Referral Tracking | 4 default codes, URL auto-fill, shareable message generator |
| 📊 Admin Dashboard | Live charts (Plotly), password-protected, target progress |
| 📁 CSV Export | 6 export types including analytical (no PII) versions |

---

## Technology Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.11+ | Core language |
| Streamlit 1.35+ | Web interface |
| SQLite (built-in) | Persistent database |
| Pandas | Data processing |
| Plotly | Interactive charts |
| python-pptx | Growth Plan presentation |
| pytest | Automated testing |

---

## Project Structure

```
carrerconnect/
│
├── app.py                      ← Main Streamlit application
├── database.py                 ← SQLite operations (all DB logic)
├── analytics.py                ← Campaign metrics and KPIs
├── referrals.py                ← Referral codes and message generation
├── exports.py                  ← CSV download functions
├── config.py                   ← Central configuration
├── generate_pptx.py            ← Growth Plan PPTX generator
│
├── requirements.txt            ← Python dependencies
├── README.md                   ← This file
├── .gitignore                  ← Git exclusions
├── promotional_materials.md    ← Draft campaign messages
│
├── data/
│   ├── .gitkeep                ← Keeps directory in Git
│   └── careerconnect.db        ← SQLite database (auto-created, NOT committed)
│
├── assets/                     ← Static assets directory
│
├── tests/
│   ├── __init__.py
│   ├── test_database.py        ← DB init, registrations, referrals, opportunities
│   ├── test_analytics.py       ← Metrics calculations
│   ├── test_referrals.py       ← Referral messages and URL extraction
│   └── test_exports.py         ← CSV export correctness
│
└── deliverables/
    ├── CareerConnect_Growth_Plan.pptx  ← 5-slide growth plan
    ├── AI_Learning_Notes.md            ← AI usage documentation
    ├── Three_Minute_Demo_Script.md     ← Video presentation script
    ├── Campaign_Plan.md                ← 7-day campaign strategy
    ├── Campaign_Metrics_Definitions.md ← Metric formulas and definitions
    ├── Project_Test_Report.md          ← Test results
    └── Submission_Checklist.md         ← Pre-submission checklist
```

---

## Installation on Windows 11

### Prerequisites

- Python 3.10 or later ([python.org](https://www.python.org/downloads/))
- Verify Python is installed:

```powershell
python --version
```

If you see `Python 3.x.x`, you're ready. If not:
- Try `py --version` (the Python Launcher)
- Or reinstall Python and tick "Add Python to PATH" during setup

### Step 1 — Navigate to the project directory

```powershell
cd "C:\Users\abhir\Desktop\carrerconnect"
```

### Step 2 — Create a virtual environment (recommended)

```powershell
python -m venv .venv
```

### Step 3 — Activate the virtual environment

**PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Command Prompt (alternative):**
```cmd
.venv\Scripts\activate.bat
```

> **If PowerShell shows a security error:**
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Then try activating again.

You should see `(.venv)` at the start of your prompt when active.

### Step 4 — Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 5 — Run the application

```powershell
python -m streamlit run app.py
```

The app opens automatically in your browser at `http://localhost:8501`.

---

## How to Run Without a Virtual Environment

If you prefer to install globally (not recommended for production):

```powershell
pip install -r requirements.txt
python -m streamlit run app.py
```

---

## How to Run the Tests

```powershell
python -m pytest tests/ -v
```

Expected output: **65 tests passed**.

To run a single test file:
```powershell
python -m pytest tests/test_database.py -v
```

---

## How the SQLite Database Works

The database is stored at `data/careerconnect.db` and is created automatically when the app starts. You do not need to create it manually.

- **Schema:** Four tables — `registrations`, `referral_codes`, `opportunities`, `campaign_events`
- **Persistence:** Data survives application restarts
- **Safety:** Parameterized SQL queries prevent SQL injection
- **Duplicates:** Email addresses are normalised and must be unique
- **Synthetic data:** Records marked `is_synthetic = 1` are excluded from dashboard metrics

---

## How to Register a Student

1. Open the app and click **📝 Register** in the sidebar
2. Fill in all required fields (name, email, college, branch, year, channel)
3. Optionally enter a referral code (e.g. `CAMPUS01`)
4. Tick the consent checkbox
5. Click **Register Now**

The registration is saved to SQLite. The dashboard immediately reflects the new record.

---

## How Referral Tracking Works

1. Each campaign channel has a referral code: `CAMPUS01`, `WHATSAPP01`, `TELEGRAM01`, `LINKEDIN01`
2. A coordinator shares a link like: `http://localhost:8501/?ref=CAMPUS01`
3. The referral code is automatically pre-filled in the registration form
4. On successful registration, the code is stored alongside the student record
5. The dashboard shows how many registrations each code has driven

To add a new code:
- Go to **🔗 Referrals** → scroll down to **Add a New Referral Code**

---

## How to Use the Admin Dashboard

1. Click **📊 Dashboard** in the sidebar
2. Enter the admin password: `admin123` (for local development only)
3. The dashboard shows:
   - Total registrations, target, remaining, completion %
   - Charts by channel, referral code, date, branch, year
   - Recent registrations table
   - Proposed vs actual target comparison

### Changing the Admin Password

Set an environment variable before running the app:

**PowerShell:**
```powershell
$env:CAREERCONNECT_ADMIN_PASSWORD = "your-new-password"
python -m streamlit run app.py
```

The default `admin123` password is for local demo only. **Never use it in a public deployment.**

---

## How to Export CSV Files

1. Log in to the **📊 Dashboard** first
2. Navigate to **📁 Export Data**
3. Click the relevant download button:
   - Full registrations (includes names and emails — admin only)
   - Analytical registrations (no PII — safe for sharing)
   - Channel performance
   - Referral code performance
   - Daily registration summary
   - Campaign metrics

---

## How to Reset Demonstration Data

To start fresh (clear all registrations):

**Option 1:** Delete the database file and restart
```powershell
Remove-Item "data\careerconnect.db"
python -m streamlit run app.py
```

The database is recreated automatically with default referral codes.

**Option 2:** Use SQLite directly
```powershell
python -c "import sqlite3; conn = sqlite3.connect('data/careerconnect.db'); conn.execute('DELETE FROM registrations WHERE is_synthetic = 0'); conn.commit(); conn.close(); print('Done')"
```

---

## Generating the Growth Plan Presentation

```powershell
python generate_pptx.py
```

This creates `deliverables/CareerConnect_Growth_Plan.pptx`.

---

## Privacy and Security Considerations

| Practice | Implementation |
|----------|---------------|
| Parameterized SQL | All queries use `?` placeholders |
| Email normalisation | Lowercase + strip before storage |
| Duplicate prevention | UNIQUE constraint on `normalized_email` |
| No phone numbers | Not collected |
| Admin auth | Password via environment variable |
| PII in exports | Full export is admin-only; analytical export strips PII |
| No external APIs | All processing is local |
| No hardcoded secrets | Password from env variable or local demo default |
| Synthetic data labelled | `is_synthetic` column, visible in dashboard |

> **This is a prototype.** Before any public deployment:
> - Replace the password system with proper session authentication
> - Add rate limiting and CAPTCHA to the registration form
> - Review all student data handling against applicable privacy regulations
> - Do not publish the SQLite database publicly

---

## Known Limitations

1. **No deployed URL.** The app runs locally. To share publicly, deploy to Streamlit Community Cloud, Render, or a similar platform (document the steps, do not assume a URL).
2. **Basic admin authentication.** The single-password system is suitable for local demonstration only.
3. **No email delivery.** The app saves registrations but cannot send confirmation emails (would require an email service and API key).
4. **Streamlit UI not unit-tested.** The UI layer requires browser automation for end-to-end tests. All business logic is tested independently.
5. **Sample opportunities only.** No real job listings are connected. Verify all listings with the original organisation.
6. **Single-touch attribution.** Multi-touch attribution (first-touch + last-touch) is not yet implemented.

---

## Troubleshooting

### `python` not found
Try `py` instead of `python`. If neither works, reinstall Python and tick "Add to PATH".

### Dependency installation fails
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Port 8501 already in use
```powershell
python -m streamlit run app.py --server.port 8502
```

### PowerShell script execution blocked
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Database not initialising
Delete `data/careerconnect.db` and restart the app. It is created fresh automatically.

### Registration form shows validation errors
- Ensure all required fields are filled
- Email must be in `name@domain.com` format
- Graduation year must be selected from the dropdown
- Consent checkbox must be ticked

### Duplicate registration error
Each email address can only register once. Check if the email was already used. The system is case-insensitive.

### Invalid referral code ignored
If you enter a referral code that is not in the database, the registration proceeds and the code is stored as empty. The referral is not attributed. Verify the code exists in the **🔗 Referrals** page.

---

## Preparing for Submission

1. Complete the [Submission Checklist](deliverables/Submission_Checklist.md)
2. Record the three-minute video using the [Demo Script](deliverables/Three_Minute_Demo_Script.md)
3. (Optional) Push to GitHub: `git init && git add . && git commit -m "CareerConnect"`
4. Submit at: **https://forms.gle/xEtJSgJfeqvnxv8q6**

---

## Suggested Git Commands

```powershell
git init
git add .
git commit -m "CareerConnect: NxtWave Growth Intern Challenge — complete build"
git remote add origin https://github.com/YOUR_USERNAME/careerconnect.git
git push -u origin main
```

> The SQLite database (`data/careerconnect.db`) is excluded by `.gitignore`.
> Never commit real student registration data to a public repository.

---

## License

This project was built for the NxtWave Growth Intern Challenge. All code is original. Sample opportunity listings and referral codes are for demonstration purposes only.

