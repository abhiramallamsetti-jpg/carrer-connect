# Three-Minute Demo Script
## CareerConnect — NxtWave Growth Intern Challenge

---

> **How to use this script:**
> Read it out loud in your own words — don't memorise it word for word.
> Speak at a natural, conversational pace.
> Each timestamp is a guide, not a strict cutoff.
> On-screen actions are shown in *[square brackets]*.
>
> **Recording checklist:** See the end of this document.

---

## 0:00 – 0:25 | Introduction

*(Speak to the camera or microphone)*

"Hi, my name is [YOUR NAME], and I'm a final-year Computer Science Engineering student.

For the NxtWave Growth Intern Challenge, I built **CareerConnect** — a web application designed around a real problem: how do you get 500 engineering students to register for a free AI workshop in just seven days, with a budget of only ₹2,000?

The workshop is called *Build Your First AI Project in 60 Minutes*, and the goal of this challenge was to plan and demonstrate a practical growth strategy for promoting it."

---

## 0:25 – 1:00 | Strategy Overview

*(Keep the app visible but talk to the camera)*

"Let me quickly walk you through the strategy.

The target audience is **final-year engineering students** — people actively looking for skills and opportunities before placement season.

I identified four main channels:
- **WhatsApp** college communities — estimated 180 registrations
- **LinkedIn** posts — estimated 100 registrations
- **Telegram** tech groups — estimated 100 registrations
- **College clubs and student referrals** — estimated 120 registrations

That adds up to 500.

Each channel gets a unique **referral code** — so when a student registers using a shared link, I know exactly which channel brought them in.

For the budget: organic channels cost zero. I've reserved ₹1,000 for optional paid promotion only *after* testing which channels perform best, and ₹1,000 as a contingency. Total: ₹2,000 maximum.

These are *proposed* targets — this is a plan, not a completed campaign."

---

## 1:00 – 2:00 | Website Demo

*[Open the CareerConnect app in the browser — `http://localhost:8501`]*

"Let me show you the working website I built.

*[Point to the sidebar]*
The app has seven sections: Home, Opportunities, AI Workshop, Registration, Referrals, Dashboard, and Export.

### Home Page
*[Click on 'Home' in the sidebar]*

This is the home page — CareerConnect branding, tagline, and a workshop banner. There are two main call-to-action buttons: Register for the workshop, and Explore Opportunities.

### Registration Form
*[Click '📝 Register' in the sidebar]*

Here's the registration form. It collects the student's name, email, college, branch, graduation year, how they heard about the workshop, and an optional referral code.

*[Fill in the form with test data: e.g., Name: 'Demo Student', Email: 'demo@college.edu', etc.]*

Watch what happens with validation — I'll leave the email blank...

*[Submit with empty email]*

You get a clear error message. Now let me fill it in properly and submit.

*[Fill in correctly and submit]*

Registration saved — confirmed with a success message and confetti. This is stored in a local SQLite database, so it survives restarts.

### Referral System
*[Click '🔗 Referrals' in the sidebar]*

Here are the referral codes. Each code has a ready-to-copy WhatsApp message and a LinkedIn post draft. A coordinator can share their link — for example `http://localhost:8501/?ref=CAMPUS01` — and the referral code is automatically pre-filled when someone opens the link.

### Admin Dashboard
*[Click '📊 Dashboard' in the sidebar — enter password 'admin123']*

This is the admin dashboard. It's password-protected. It shows the total registrations, how many remain to reach 500, and the completion percentage. All metrics are calculated from the live database — nothing is hardcoded.

*[Point to charts]*

Charts show registrations by channel, by referral code, by date, by branch, and by graduation year.

### CSV Export
*[Click '📁 Export Data' in the sidebar]*

From here, an admin can download six types of CSV reports — registrations, channel performance, referral performance, daily summaries, and campaign metrics. Exports with personal information are clearly flagged."

---

## 2:00 – 2:35 | AI Suggestion Rejected

*(Back to camera)*

"During development, AI suggested adding an ML-based job recommender — where the app would use embeddings and nearest-neighbour matching to suggest relevant jobs to each student.

I deliberately rejected this.

Here's why:

First, the challenge is about a *growth strategy for a workshop* — not about building an ML system. Adding it would have wasted time on something outside the core deliverable.

Second, the job listings are clearly labelled sample data. A 'smart' recommender built on fake listings would produce meaningless results and could mislead users.

Third, ML libraries like `scikit-learn` or `sentence-transformers` add hundreds of megabytes of dependencies — which goes against the challenge requirement to keep the project lightweight and beginner-friendly.

Instead, I used a simple keyword search and dropdown filter. It achieves the same goal — finding relevant listings — without any ML complexity.

The lesson: **don't add impressive-sounding features that don't serve the actual objective.**"

---

## 2:35 – 3:00 | What I Learned and Next Steps

*(Camera)*

"To summarise what I built: a working registration and referral platform, a live analytics dashboard, six CSV exports, 65 passing automated tests, a five-slide growth plan, and a complete documentation set — all running locally with Python, Streamlit, and SQLite.

What would I improve with another 24 hours?

Three things:
- **Test with real users** — have five actual students register and note where they get confused.
- **Run a small pilot outreach** — send to one community (with admin permission) to get real attribution data.
- **Add rate limiting** before any public deployment to prevent fake registrations.

The strategy is planned. The platform is ready. The next step is for a real campaign to begin.

Thank you."

---

## 📋 Video Recording Checklist

Use this before and during recording. You do **not** need paid video editing software.

### Free Recording Tools
- **Windows built-in:** Press `Win + G` to open the Xbox Game Bar, then record your screen.
- **OBS Studio** (free, open-source): Download from obsproject.com for higher quality.
- **Google Meet / Zoom:** Start a meeting alone and record your screen.

### Before You Record
- [ ] Run `python -m streamlit run app.py` and confirm the app loads at `http://localhost:8501`
- [ ] Register a test student in advance so the dashboard shows at least one registration
- [ ] Have the admin password ready (`admin123` or your custom env variable)
- [ ] Close unnecessary browser tabs and desktop notifications
- [ ] Set screen resolution to 1920×1080 if possible
- [ ] Test your microphone audio before the full recording
- [ ] Read through this script at least twice out loud

### During Recording
- [ ] Show the sidebar navigation clearly
- [ ] Zoom in on form fields and charts if recording at high resolution
- [ ] Speak slowly — aim for about 130 words per minute
- [ ] If you make a mistake, pause, breathe, and continue — you can trim in editing

### After Recording
- [ ] Trim the start and end if there's dead time
- [ ] Verify the audio is clear throughout
- [ ] Export as MP4 (most submission forms accept this)
- [ ] Keep the file under the submission size limit

### Submission
Submit your video and all deliverables via the NxtWave Growth Challenge form:
**https://forms.gle/xEtJSgJfeqvnxv8q6**

*(Do not claim the form has been submitted — you must do this yourself.)*

---

*This script was written as a guide. Speak naturally in your own voice rather than reading word-for-word.*

