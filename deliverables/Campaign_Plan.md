# CareerConnect — Campaign Plan
## NxtWave Growth Intern Challenge

> **Status:** This is a *proposed* campaign plan.
> No outreach has been conducted. No real registrations exist at the time of writing.
> All channel targets are planning estimates, not observed results.

---

## 1. Objective

Plan for **500 unique final-year engineering student registrations** for the free online workshop:

> **"Build Your First AI Project in 60 Minutes"**

- **Timeframe:** 7 days
- **Budget:** ≤ ₹2,000
- **Constraint:** Organic channels must be tested before any paid spend
- **Ethics:** No spam, no unauthorised posting, no purchasing of student data

---

## 2. Target Audience

| Dimension | Details |
|-----------|---------|
| **Who** | Final-year engineering students (all branches) |
| **When** | 2025–2027 graduation cohort |
| **Where** | India — primarily WhatsApp, LinkedIn, Telegram, college clubs |
| **Motivation** | Placement prep, practical AI skills, free learning |
| **Pain point** | Struggling to find beginner-friendly, free AI resources |

---

## 3. Acquisition Channels

### Channel A — WhatsApp College Communities
**Proposed target:** 180 registrations

- **Audience:** Engineering students in year-specific or branch-specific WhatsApp groups
- **Activity:** Post the promotional message with referral code WHATSAPP01
- **Distribution:** Request admin permission before posting; one post per group
- **Tracking:** Referral code WHATSAPP01 in registration form
- **Expected:** Highest reach per message; moderate conversion rate
- **Risks:** Groups may restrict promotional posts; admin may decline
- **Mitigation:** Prepare a concise, genuinely useful message; offer to answer student questions

**Sample WhatsApp Message:**
```
Hi everyone! Sharing a free AI workshop for engineering students —
"Build Your First AI Project in 60 Minutes"

✅ Free | ✅ Online | ✅ Beginner-friendly

Register here: [REGISTRATION_URL]?ref=WHATSAPP01

Workshop details (date, time, speaker) will be confirmed by the organiser.
Please verify before registering.
```

---

### Channel B — LinkedIn
**Proposed target:** 100 registrations

- **Audience:** Final-year students with LinkedIn profiles; engineering student networks
- **Activity:** Publish a personal post explaining the workshop; use relevant hashtags
- **Distribution:** Organic post + engagement in comments; connect with student communities
- **Tracking:** Referral code LINKEDIN01 in registration URL
- **Expected:** Slower but high-quality registrations from motivated students
- **Risks:** Algorithm reach limited without engagement; requires genuine post, not spam
- **Mitigation:** Write a personal story about AI learning; include a clear, honest description

**Sample LinkedIn Post:**
```
Calling all final-year engineering students!

Found a free online workshop — "Build Your First AI Project in 60 Minutes"
— designed specifically for students new to AI.

If you've been curious about building something with AI but don't know where to start,
this workshop is worth checking out.

Register (free): [REGISTRATION_URL]?ref=LINKEDIN01

Workshop details to be confirmed by the organiser.

#AI #Engineering #FreeWorkshop #StudentLife #CareerGrowth
```

---

### Channel C — Telegram Communities
**Proposed target:** 100 registrations

- **Audience:** Tech-focused engineering student Telegram channels and groups
- **Activity:** Post the promotional message with referral code TELEGRAM01
- **Distribution:** Request admin permission; post once per channel
- **Tracking:** Referral code TELEGRAM01
- **Expected:** High-engagement audience; tech students respond well to AI workshops
- **Risks:** Some channels have strict no-promotion rules
- **Mitigation:** Join relevant channels early; contribute value before posting

---

### Channel D — College Clubs and Student Referrals
**Proposed target:** 120 registrations

- **Audience:** Engineering club members; student coordinator networks
- **Activity:** Reach out to coding clubs, tech fests, placement cells; appoint volunteer campus ambassadors
- **Distribution:** Email or message to club leads; ask them to share with members
- **Tracking:** Referral code CAMPUS01 (or custom codes per coordinator)
- **Expected:** Highest trust channel; personal recommendations convert well
- **Risks:** Slower to activate; depends on volunteer effort
- **Mitigation:** Make participation easy; provide ready-to-use messages; show coordinator contribution on dashboard

---

## 4. Seven-Day Schedule

| Day | Activity |
|-----|----------|
| **Day 1** | Build landing page, registration form, referral system, tracking dashboard, promotional assets |
| **Day 2** | Identify communities; prepare messages; seek admin permission where required |
| **Day 3** | Begin outreach — post to permitted WhatsApp and Telegram groups |
| **Day 4** | Review channel performance; test message variations; identify best-performing channel |
| **Day 5** | Expand to college clubs and student coordinators |
| **Day 6** | Activate referral sharing; send permitted follow-up messages |
| **Day 7** | Final outreach push; analyse results; prepare campaign report |

---

## 5. Budget

| Item | Amount (INR) | Notes |
|------|-------------|-------|
| Website & analytics tools | ₹0 | Open-source local stack |
| Organic outreach | ₹0 | Permission-based, no cost |
| Optional paid promotion | ₹1,000 | Only after organic test confirms viability |
| Contingency | ₹1,000 | Flexible buffer |
| **Total** | **₹2,000** | **Maximum available** |

**Decision rule for paid spend:**
If organic channels reach less than 200 registrations by Day 4, consider allocating ₹500–₹1,000 to targeted LinkedIn ads or WhatsApp Business campaigns. Paid spend should only happen once the message and targeting are validated by organic results.

---

## 6. Measurement Framework

### Key Metrics

| Metric | Formula | Source |
|--------|---------|--------|
| Total unique registrations | COUNT of registrations WHERE is_synthetic = 0 | DB |
| Target completion (%) | (total / 500) × 100 | Computed |
| Remaining registrations | max(500 − total, 0) | Computed |
| Registrations by channel | GROUP BY acquisition_channel | DB |
| Referral registrations | COUNT WHERE referral_code IS NOT NULL | DB |
| Cost per registration | Expenditure ÷ total registrations | Manual + DB |
| Duplicate rate | Rejected duplicates ÷ total attempts | DB |

### Proposed Experiments

**EXP-01: Message Variation Test**
- Hypothesis: An action-focused message ("60-minute hands-on project") outperforms an outcome-focused message ("boost your career with AI").
- Variable: WhatsApp message wording
- Success metric: Registration rate per variant
- Status: Proposed — not executed

**EXP-02: Channel Attribution Comparison**
- Hypothesis: WhatsApp delivers more registrations per message than LinkedIn in the first 3 days.
- Variable: Channel (WhatsApp vs LinkedIn), tracked by referral code
- Success metric: Registrations per channel by Day 4
- Status: Proposed — not executed

---

## 7. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| WhatsApp group admins refuse posting | Medium | High | Prepare a concise, respectful request; have alternatives ready |
| Duplicate registrations inflate count | Low | Medium | Email normalisation + UNIQUE constraint prevent this |
| Low LinkedIn organic reach | Medium | Medium | Engage with comments; ask network to share |
| Workshop details not confirmed by organiser | High | High | Always label TBC details honestly; never invent dates |
| Budget insufficient for paid ads | Low | Low | Organic is free; paid is optional contingency |

---

## 8. Attribution Rules

1. If a student registers with a referral code that matches a database record → attributed to that code's channel.
2. If a student registers via a URL with `?ref=CODE` → code is pre-filled and attributed.
3. If a student selects an acquisition channel but has no referral code → attributed to the selected channel only.
4. Duplicate registrations (same email) are rejected — only the first registration is counted.
5. Email normalisation ensures `Alice@Example.COM` and `alice@example.com` are treated as one student.

---

*This document describes a proposed plan. All activities labelled as "Day N" have not yet been executed. Results will be updated as real data becomes available.*

