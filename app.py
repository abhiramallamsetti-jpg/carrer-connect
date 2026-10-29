"""
CareerConnect — Main Application
Student Opportunities & AI Workshop Growth Platform
NxtWave Growth Intern Challenge
"""

import re
import streamlit as st
from datetime import datetime
from pathlib import Path

# ── Project modules ──────────────────────────────────────────────────────────
import config
from config import (
    APP_NAME, APP_TAGLINE, WORKSHOP_TITLE, WORKSHOP_DESCRIPTION,
    WORKSHOP_AUDIENCE, REGISTRATION_TARGET, ACQUISITION_CHANNELS,
    ENGINEERING_BRANCHES, VALID_GRADUATION_YEARS, SAMPLE_OPPORTUNITIES,
    COLORS, get_admin_password,
)
from database import (
    init_db, register_student, email_already_registered,
    get_all_registrations, seed_opportunities, get_opportunities,
    get_all_referral_codes, add_referral_code, referral_code_exists,
    get_recent_registrations,
)
from analytics import (
    compute_campaign_metrics, PROPOSED_EXPERIMENTS,
    get_channel_target_allocation,
)
from referrals import (
    extract_referral_from_params, generate_referral_message,
    generate_linkedin_message, get_referral_summary,
)
from exports import (
    export_registrations_csv, export_channel_performance_csv,
    export_referral_performance_csv, export_daily_summary_csv,
    export_campaign_metrics_csv,
)

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CareerConnect",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Database Init ─────────────────────────────────────────────────────────────
@st.cache_resource
def startup():
    init_db()
    seed_opportunities(SAMPLE_OPPORTUNITIES)
    return True

startup()

# ── Global CSS ────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(f"""
<style>
/* ── Base ── */
body, [data-testid="stAppViewContainer"] {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text_primary']};
}}
[data-testid="stSidebar"] {{
    background-color: #13151a;
    border-right: 1px solid {COLORS['border']};
}}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label {{
    color: {COLORS['text_secondary']} !important;
}}

/* ── Typography ── */
h1, h2, h3, h4 {{ color: {COLORS['text_primary']}; }}
p, li {{ color: {COLORS['text_secondary']}; }}

/* ── Brand Header ── */
.brand-header {{
    background: linear-gradient(135deg, {COLORS['primary']} 0%, #8B5CF6 50%, {COLORS['secondary']} 100%);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(108,99,255,0.3);
}}
.brand-header h1 {{
    font-size: 2.8rem;
    font-weight: 800;
    color: #fff !important;
    margin: 0;
    letter-spacing: -0.5px;
}}
.brand-header p {{
    font-size: 1.15rem;
    color: rgba(255,255,255,0.85) !important;
    margin: 0.5rem 0 0;
}}

/* ── Workshop Banner ── */
.workshop-banner {{
    background: linear-gradient(135deg, #1a1d23 0%, #252830 100%);
    border: 1px solid {COLORS['primary']};
    border-left: 5px solid {COLORS['primary']};
    border-radius: 12px;
    padding: 1.8rem 2rem;
    margin: 1.5rem 0;
}}
.workshop-banner h2 {{ color: {COLORS['primary']} !important; margin: 0 0 0.5rem; }}
.workshop-banner p {{ color: {COLORS['text_secondary']} !important; margin: 0; }}

/* ── Metric Cards ── */
.metric-card {{
    background: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.4);
}}
.metric-card .value {{
    font-size: 2.2rem;
    font-weight: 700;
    color: {COLORS['primary']};
    line-height: 1;
}}
.metric-card .label {{
    font-size: 0.82rem;
    color: {COLORS['text_secondary']};
    margin-top: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* ── Opportunity Card ── */
.opp-card {{
    background: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}}
.opp-card:hover {{ border-color: {COLORS['primary']}; }}
.opp-card .opp-title {{ font-size: 1.1rem; font-weight: 600; color: {COLORS['text_primary']}; }}
.opp-card .opp-company {{ font-size: 0.9rem; color: {COLORS['secondary']}; }}
.opp-card .opp-badge {{
    display: inline-block;
    background: rgba(108,99,255,0.15);
    color: {COLORS['primary']};
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 6px;
}}
.opp-card .opp-meta {{ font-size: 0.82rem; color: {COLORS['text_secondary']}; margin-top: 0.5rem; }}

/* ── Alert Boxes ── */
.alert-success {{
    background: rgba(0,201,167,0.12);
    border: 1px solid {COLORS['success']};
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: {COLORS['success']};
}}
.alert-error {{
    background: rgba(255,107,107,0.12);
    border: 1px solid {COLORS['error']};
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: {COLORS['error']};
}}
.alert-info {{
    background: rgba(108,99,255,0.10);
    border: 1px solid {COLORS['primary']};
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: {COLORS['text_secondary']};
}}
.alert-warning {{
    background: rgba(255,179,71,0.10);
    border: 1px solid {COLORS['warning']};
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: {COLORS['warning']};
}}

/* ── Section Headers ── */
.section-header {{
    border-bottom: 2px solid {COLORS['primary']};
    padding-bottom: 0.5rem;
    margin: 2rem 0 1.2rem;
    color: {COLORS['text_primary']};
    font-size: 1.4rem;
    font-weight: 700;
}}

/* ── Referral Box ── */
.referral-box {{
    background: #1a1d23;
    border: 1px dashed {COLORS['secondary']};
    border-radius: 10px;
    padding: 1.2rem;
    font-family: monospace;
    font-size: 0.88rem;
    color: {COLORS['text_secondary']};
    white-space: pre-wrap;
    word-break: break-word;
}}

/* ── Progress Bar ── */
.progress-wrap {{
    background: {COLORS['border']};
    border-radius: 8px;
    height: 12px;
    overflow: hidden;
    margin: 0.5rem 0;
}}
.progress-fill {{
    background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['secondary']});
    height: 100%;
    border-radius: 8px;
    transition: width 0.5s ease;
}}

/* ── Synthetic Data Badge ── */
.synthetic-badge {{
    background: rgba(255,179,71,0.15);
    border: 1px solid {COLORS['warning']};
    border-radius: 6px;
    padding: 0.4rem 0.8rem;
    font-size: 0.78rem;
    color: {COLORS['warning']};
    display: inline-block;
    margin-bottom: 0.8rem;
}}

/* ── Sidebar nav ── */
.sidebar-logo {{
    font-size: 1.4rem;
    font-weight: 800;
    color: {COLORS['primary']};
    padding: 0.5rem 0 1rem;
    display: block;
}}
</style>
""", unsafe_allow_html=True)

inject_css()


# ── Helpers ──────────────────────────────────────────────────────────────────

def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))

def metric_card(value, label):
    st.markdown(
        f'<div class="metric-card"><div class="value">{value}</div>'
        f'<div class="label">{label}</div></div>',
        unsafe_allow_html=True,
    )

def section_header(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

def progress_bar(pct):
    pct_clamped = min(max(pct, 0), 100)
    st.markdown(
        f'<div class="progress-wrap">'
        f'<div class="progress-fill" style="width:{pct_clamped}%"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<span class="sidebar-logo">🚀 CareerConnect</span>', unsafe_allow_html=True)
    st.caption(APP_TAGLINE)
    st.markdown("---")
    page = st.radio(
        "Navigate",
        [
            "🏠 Home",
            "💼 Opportunities",
            "🤖 AI Workshop",
            "📝 Register",
            "🔗 Referrals",
            "📊 Dashboard",
            "📁 Export Data",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("**NxtWave Growth Intern Challenge**")
    st.caption("Local Demonstration Build")
    st.caption(f"Version {config.APP_VERSION}")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE A — HOME
# ═════════════════════════════════════════════════════════════════════════════

if page == "🏠 Home":
    # Hero
    st.markdown(f"""
<div class="brand-header">
    <h1>🚀 {APP_NAME}</h1>
    <p>{APP_TAGLINE}</p>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
<div class="metric-card">
    <div class="value">🎓</div>
    <div class="label">Student-First Platform</div>
</div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
<div class="metric-card">
    <div class="value">🤖</div>
    <div class="label">Free AI Workshop</div>
</div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
<div class="metric-card">
    <div class="value">💼</div>
    <div class="label">Career Opportunities</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Workshop Banner
    st.markdown(f"""
<div class="workshop-banner">
    <h2>🤖 {WORKSHOP_TITLE}</h2>
    <p>{WORKSHOP_DESCRIPTION}</p>
    <p style="margin-top:0.8rem; font-size:0.85rem; color:#888;">
        ⚠️ Workshop date, time, speaker, and meeting link will be confirmed by the organiser.
        Please verify all details before registering.
    </p>
</div>
""", unsafe_allow_html=True)

    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])
    with btn_col1:
        if st.button("📝 Register for Free Workshop", type="primary", use_container_width=True):
            st.session_state["_nav"] = "📝 Register"
            st.rerun()
    with btn_col2:
        if st.button("💼 Explore Opportunities", use_container_width=True):
            st.session_state["_nav"] = "💼 Opportunities"
            st.rerun()

    st.markdown("---")

    # How Students Benefit
    section_header("How CareerConnect Helps You")
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown("""
**🎯 Discover Workshops**
Access curated free workshops designed for engineering students — no prior experience required.
""")
    with b2:
        st.markdown("""
**🔗 Refer & Earn Recognition**
Share your referral code with friends. Track how many people you helped get registered.
""")
    with b3:
        st.markdown("""
**💼 Explore Career Paths**
Browse sample internship and job listings to understand what skills employers are looking for.
""")

    st.markdown("---")

    # Featured Opportunities (top 3)
    section_header("Featured Opportunities")
    st.markdown(
        '<div class="alert-warning">⚠️ Sample opportunities are provided for demonstration. '
        'Verify each listing with the original organisation before applying.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    featured = SAMPLE_OPPORTUNITIES[:3]
    for opp in featured:
        with st.container():
            st.markdown(f"""
<div class="opp-card">
    <div class="opp-title">{opp['title']}</div>
    <div class="opp-company">🏢 {opp['company']}</div>
    <div style="margin-top:0.6rem;">
        <span class="opp-badge">{opp['type']}</span>
        <span class="opp-badge">📍 {opp['location']}</span>
    </div>
    <div class="opp-meta">🛠 {opp['skills']}</div>
</div>
""", unsafe_allow_html=True)

    if st.button("View All Opportunities →"):
        st.session_state["_nav"] = "💼 Opportunities"
        st.rerun()


# Handle nav redirect from buttons
if "_nav" in st.session_state:
    # Clear and redirect
    nav_target = st.session_state.pop("_nav")
    # Can't directly change radio; notify user
    st.info(f"👉 Please select **{nav_target}** from the sidebar to navigate.")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE B — OPPORTUNITIES
# ═════════════════════════════════════════════════════════════════════════════

elif page == "💼 Opportunities":
    st.markdown(f'<div class="brand-header"><h1>💼 Career Opportunities</h1><p>Sample internships and jobs for engineering students</p></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="alert-warning">⚠️ <strong>Important:</strong> All listings below are sample/demonstration opportunities. '
        'They are NOT real job postings. Verify every listing with the original organisation before applying.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Filters
    fcol1, fcol2 = st.columns([3, 1])
    with fcol1:
        search = st.text_input("🔍 Search by title, company, or skill", placeholder="e.g. Python, Data, Remote…")
    with fcol2:
        opp_types = ["All", "Internship", "Full-time", "Part-time", "Freelance"]
        opp_type_filter = st.selectbox("Filter by type", opp_types)

    opps = get_opportunities(search=search, opp_type=opp_type_filter if opp_type_filter != "All" else "")

    if not opps:
        st.markdown('<div class="alert-info">No opportunities match your filters. Try a different search term.</div>', unsafe_allow_html=True)
    else:
        st.caption(f"Showing {len(opps)} {'sample ' if True else ''}opportunit{'y' if len(opps)==1 else 'ies'}")
        for opp in opps:
            with st.expander(f"**{opp['title']}** — {opp['company']} ({opp['opp_type']})", expanded=False):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**🏢 Organisation:** {opp['company']}")
                    st.markdown(f"**📌 Type:** {opp['opp_type']}")
                    st.markdown(f"**📍 Location:** {opp['location']}")
                    st.markdown(f"**🗓 Deadline:** {opp['deadline'] or 'To be confirmed'}")
                with c2:
                    st.markdown(f"**🛠 Skills Required:** {opp['skills']}")
                    st.markdown(f"**🎓 Eligibility:** {opp['eligibility']}")
                st.markdown(f"**📄 Description:** {opp['description']}")
                if opp.get("is_sample"):
                    st.markdown('<span class="synthetic-badge">📋 SAMPLE LISTING — For demonstration only</span>', unsafe_allow_html=True)
                if opp.get("apply_link"):
                    st.link_button("Apply Now →", opp["apply_link"])
                else:
                    st.caption("Application link not yet available — check the organisation's official website.")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE C — AI WORKSHOP
# ═════════════════════════════════════════════════════════════════════════════

elif page == "🤖 AI Workshop":
    st.markdown(f'<div class="brand-header"><h1>🤖 AI Workshop</h1><p>Build Your First AI Project in 60 Minutes</p></div>', unsafe_allow_html=True)

    st.markdown(f"""
<div class="workshop-banner">
    <h2>{WORKSHOP_TITLE}</h2>
    <p>{WORKSHOP_DESCRIPTION}</p>
</div>
""", unsafe_allow_html=True)

    st.markdown(
        '<div class="alert-info">ℹ️ The information below describes the proposed workshop scope. '
        'Exact date, time, speaker, and meeting link will be confirmed by the organiser. '
        'Please verify before registering.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    section_header("Workshop Overview")
    wc1, wc2 = st.columns(2)
    with wc1:
        st.markdown(f"**🎯 Objective:** {WORKSHOP_DESCRIPTION}")
        st.markdown(f"**👥 Audience:** {WORKSHOP_AUDIENCE}")
        st.markdown("**⏱ Duration:** Approximately 60 minutes (online)")
        st.markdown("**💰 Cost:** Free of charge")
    with wc2:
        st.markdown("**📅 Date & Time:** *To be confirmed by the organiser*")
        st.markdown("**🔗 Meeting Link:** *To be confirmed by the organiser*")
        st.markdown("**🏅 Certificate:** *To be confirmed by the organiser*")
        st.markdown("**🎤 Speaker:** *To be confirmed by the organiser*")

    section_header("Proposed Learning Topics")
    st.markdown("""
> **Note:** These are proposed topics. The actual curriculum will be confirmed by the workshop organiser.

1. **Introduction to AI** — What is AI and why does it matter for engineering students?
2. **Choosing a Project Idea** — How to select a beginner-friendly AI project
3. **Data Collection Basics** — Finding and preparing a small dataset
4. **Building Your First Model** — Hands-on demonstration with Python
5. **Testing and Evaluating** — How to know if your model is working
6. **Next Steps** — Resources to continue learning AI independently
""")

    section_header("Who Should Attend?")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
✅ Final-year engineering students (any branch)
✅ Students exploring AI/ML for projects or placements
✅ Beginners with no prior AI experience required
""")
    with col2:
        st.markdown("""
✅ Students working on final-year projects
✅ Anyone curious about practical AI applications
✅ Students preparing for AI-related interviews
""")

    section_header("How to Register")
    st.markdown("""
1. Click the **Register Now** button below
2. Fill in your name, email, college, branch, and graduation year
3. Select how you heard about the workshop
4. Enter a referral code if you received one
5. Tick the consent checkbox and submit
6. Keep an eye on the email address you provide for workshop details from the organiser
""")

    if st.button("📝 Register Now — It's Free!", type="primary"):
        st.info("👉 Please select **📝 Register** from the sidebar to open the registration form.")

    section_header("Frequently Asked Questions")
    faqs = [
        ("Is this workshop really free?", "Yes, registration is free. Please verify payment details (if any) directly with the organiser."),
        ("Do I need to know Python already?", "The workshop is designed for beginners. Basic familiarity with programming concepts will be helpful but is not mandatory."),
        ("Will I receive a certificate?", "Certificate availability has not been confirmed. Please check with the organiser after registration."),
        ("Can students from any engineering branch attend?", "Yes. The workshop is open to all engineering branches."),
        ("How will I receive the workshop link?", "The organiser will send workshop details to your registered email. Ensure your email address is correct."),
        ("What if I miss the live session?", "Recording availability has not been confirmed. Please contact the organiser for their policy."),
    ]
    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(a)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE D — REGISTRATION
# ═════════════════════════════════════════════════════════════════════════════

elif page == "📝 Register":
    st.markdown(f'<div class="brand-header"><h1>📝 Workshop Registration</h1><p>Register for the free AI workshop below</p></div>', unsafe_allow_html=True)

    # Read referral from query params
    query_params = st.query_params
    url_ref = extract_referral_from_params(dict(query_params))
    if url_ref and referral_code_exists(url_ref):
        st.markdown(
            f'<div class="alert-success">✅ Referral code <strong>{url_ref}</strong> detected and pre-filled!</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="alert-info">ℹ️ All fields marked with * are required. '
        'Your information will be used only to manage your workshop registration.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("registration_form", clear_on_submit=False):
        st.markdown("### 👤 Personal Information")
        rc1, rc2 = st.columns(2)
        with rc1:
            student_name = st.text_input("Full Name *", placeholder="Your full name")
        with rc2:
            email = st.text_input("Email Address *", placeholder="you@example.com")

        st.markdown("### 🎓 Academic Information")
        ac1, ac2 = st.columns(2)
        with ac1:
            college = st.text_input("College / University *", placeholder="Your college name")
        with ac2:
            branch = st.selectbox("Engineering Branch *", ["— Select —"] + ENGINEERING_BRANCHES)

        gc1, gc2 = st.columns(2)
        with gc1:
            grad_year = st.selectbox(
                "Expected Graduation Year *",
                ["— Select —"] + [str(y) for y in VALID_GRADUATION_YEARS],
            )
        with gc2:
            channel = st.selectbox(
                "How did you hear about this workshop? *",
                ["— Select —"] + ACQUISITION_CHANNELS,
            )

        st.markdown("### 🔗 Referral Code (Optional)")
        referral_input = st.text_input(
            "Referral Code",
            value=url_ref or "",
            placeholder="e.g. CAMPUS01",
            help="Enter the referral code shared by a friend or coordinator. Leave blank if you don't have one.",
        )

        st.markdown("### ✅ Consent")
        consent = st.checkbox(
            "I acknowledge that the information I provide will be used to manage my workshop registration. *",
        )

        submitted = st.form_submit_button("🚀 Register Now", type="primary", use_container_width=True)

    if submitted:
        errors = []

        # Validate required fields
        if not student_name.strip():
            errors.append("Full name is required.")
        elif len(student_name.strip()) < 2:
            errors.append("Please enter your full name (at least 2 characters).")

        if not email.strip():
            errors.append("Email address is required.")
        elif not is_valid_email(email):
            errors.append("Please enter a valid email address (e.g. name@domain.com).")

        if not college.strip():
            errors.append("College / University name is required.")

        if branch == "— Select —":
            errors.append("Please select your engineering branch.")

        if grad_year == "— Select —":
            errors.append("Please select your expected graduation year.")
        else:
            try:
                int(grad_year)
            except ValueError:
                errors.append("Invalid graduation year.")

        if channel == "— Select —":
            errors.append("Please tell us how you heard about the workshop.")

        if not consent:
            errors.append("You must acknowledge the consent statement to register.")

        if errors:
            for err in errors:
                st.markdown(f'<div class="alert-error">❌ {err}</div>', unsafe_allow_html=True)
        else:
            # Attempt registration
            result = register_student(
                student_name=student_name,
                email=email,
                college_name=college,
                branch=branch,
                graduation_year=int(grad_year),
                acquisition_channel=channel,
                referral_code=referral_input.strip() if referral_input.strip() else None,
                consent_acknowledged=consent,
                is_synthetic=False,
            )

            if result["success"]:
                st.markdown(f"""
<div class="alert-success">
🎉 <strong>Registration Successful!</strong><br>
Thank you, <strong>{student_name.strip()}</strong>! Your registration has been saved.<br>
Watch the email address you provided for workshop details from the organiser.
</div>
""", unsafe_allow_html=True)
                st.balloons()
            elif result.get("error") == "duplicate_email":
                st.markdown(
                    f'<div class="alert-error">⚠️ This email address is already registered. '
                    f'Each student may register only once. If you think this is an error, '
                    f'please contact the organiser.</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="alert-error">❌ Registration failed: {result.get("error", "Unknown error")}. '
                    f'Please try again or contact the organiser.</div>',
                    unsafe_allow_html=True,
                )

    # Privacy notice
    st.markdown("---")
    st.markdown("""
**🔒 Privacy Notice**

- Your information is stored locally in a SQLite database on this server and is not shared with third parties.
- Email addresses are normalised and used solely to prevent duplicate registrations and to send workshop details from the organiser.
- Phone numbers are not collected.
- This is a local prototype. Review the privacy and security documentation before any public deployment.
""")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE E — REFERRALS
# ═════════════════════════════════════════════════════════════════════════════

elif page == "🔗 Referrals":
    st.markdown(f'<div class="brand-header"><h1>🔗 Referral Tracking</h1><p>Share your code and track who registers through you</p></div>', unsafe_allow_html=True)

    summary = get_referral_summary()

    section_header("How Referrals Work")
    st.markdown("""
1. Each campus ambassador or campaign source receives a unique referral code.
2. Students share the registration link with their code: `https://your-app-url/?ref=CODE`
3. When someone registers using a referral code, the registration is attributed to that code.
4. The dashboard tracks referral performance in real time.

> **Referral codes are for demonstration.** CAMPUS01, WHATSAPP01, etc., are example codes — not evidence of real participating colleges or active campaigns.
""")

    section_header("Active Referral Codes")
    if not summary["codes"]:
        st.markdown('<div class="alert-info">No referral codes found. Database may not be initialised.</div>', unsafe_allow_html=True)
    else:
        for entry in summary["codes"]:
            with st.expander(f"**{entry['code']}** — {entry['description']} ({entry['registrations']} registrations)"):
                st.markdown(f"**Channel:** {entry['channel']}")
                st.markdown(f"**Registrations attributed:** {entry['registrations']}")

                st.markdown("**📱 WhatsApp / Telegram Message Draft:**")
                st.markdown(f'<div class="referral-box">{entry["message"]}</div>', unsafe_allow_html=True)
                st.markdown("**🔗 LinkedIn Post Draft:**")
                st.markdown(f'<div class="referral-box">{entry["linkedin_message"]}</div>', unsafe_allow_html=True)

    st.markdown("---")
    section_header("Add a New Referral Code")
    st.markdown(
        '<div class="alert-warning">⚠️ This is an admin function for managing campaign codes. '
        'In a production deployment, this should be protected behind authentication.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("add_referral_form"):
        nc1, nc2, nc3 = st.columns(3)
        with nc1:
            new_code = st.text_input("Referral Code *", placeholder="e.g. MYCLUB01").upper().strip()
        with nc2:
            new_desc = st.text_input("Description", placeholder="e.g. Engineering Club")
        with nc3:
            new_channel = st.selectbox("Channel", [""] + ACQUISITION_CHANNELS)
        add_submitted = st.form_submit_button("Add Code", type="primary")

    if add_submitted:
        if not new_code:
            st.markdown('<div class="alert-error">❌ Referral code cannot be empty.</div>', unsafe_allow_html=True)
        elif len(new_code) < 3:
            st.markdown('<div class="alert-error">❌ Code must be at least 3 characters.</div>', unsafe_allow_html=True)
        else:
            ok = add_referral_code(new_code, new_desc, new_channel)
            if ok:
                st.markdown(f'<div class="alert-success">✅ Referral code <strong>{new_code}</strong> added successfully.</div>', unsafe_allow_html=True)
                st.rerun()
            else:
                st.markdown(f'<div class="alert-error">⚠️ Code <strong>{new_code}</strong> already exists.</div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE F — ADMIN DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════

elif page == "📊 Dashboard":
    st.markdown(f'<div class="brand-header"><h1>📊 Admin Dashboard</h1><p>Live campaign analytics from the database</p></div>', unsafe_allow_html=True)

    # Simple local auth
    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False

    if not st.session_state["admin_authenticated"]:
        st.markdown(
            '<div class="alert-info">🔒 This dashboard contains registration data. '
            'Please enter the admin password to continue.<br>'
            '<small>Default local dev password: <code>admin123</code> — '
            'Change via the <code>CAREERCONNECT_ADMIN_PASSWORD</code> environment variable.</small></div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        pw = st.text_input("Admin Password", type="password")
        if st.button("Login", type="primary"):
            if pw == get_admin_password():
                st.session_state["admin_authenticated"] = True
                st.rerun()
            else:
                st.markdown('<div class="alert-error">❌ Incorrect password.</div>', unsafe_allow_html=True)
        st.stop()

    # Authenticated
    if st.button("🚪 Logout", help="Log out of the admin dashboard"):
        st.session_state["admin_authenticated"] = False
        st.rerun()

    import plotly.express as px
    import pandas as pd

    metrics = compute_campaign_metrics(only_real=True)

    # Top KPI cards
    section_header("Campaign Overview")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        metric_card(metrics["total_registrations"], "Total Registrations")
    with k2:
        metric_card(metrics["target"], "Target")
    with k3:
        metric_card(metrics["remaining"], "Remaining")
    with k4:
        metric_card(f"{metrics['completion_pct']}%", "Target Completion")

    st.markdown("<br>", unsafe_allow_html=True)
    progress_bar(metrics["completion_pct"])
    st.caption(f"Progress toward {metrics['target']} registrations: {metrics['completion_pct']}%")
    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    if metrics["total_registrations"] == 0:
        st.markdown(
            '<div class="alert-info">📭 No registrations yet. '
            'Register some students to see analytics here.</div>',
            unsafe_allow_html=True,
        )
    else:
        ch_col, ref_col = st.columns(2)

        with ch_col:
            section_header("By Acquisition Channel")
            if metrics["channel_data"]:
                df_ch = pd.DataFrame(metrics["channel_data"])
                fig_ch = px.bar(
                    df_ch, x="channel", y="count",
                    color="count",
                    color_continuous_scale=["#6C63FF", "#00C9A7"],
                    labels={"channel": "Channel", "count": "Registrations"},
                    template="plotly_dark",
                )
                fig_ch.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    coloraxis_showscale=False,
                )
                st.plotly_chart(fig_ch, use_container_width=True)
            else:
                st.caption("No channel data available.")

        with ref_col:
            section_header("By Referral Code")
            if metrics["referral_data"]:
                df_ref = pd.DataFrame(metrics["referral_data"])
                fig_ref = px.pie(
                    df_ref, names="code", values="count",
                    template="plotly_dark",
                    color_discrete_sequence=px.colors.sequential.Purples_r,
                )
                fig_ref.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig_ref, use_container_width=True)
            else:
                st.caption("No referral registrations yet.")

        # Daily trend
        if metrics["daily_data"]:
            section_header("Daily Registration Trend")
            df_daily = pd.DataFrame(metrics["daily_data"])
            fig_daily = px.area(
                df_daily, x="date", y="count",
                labels={"date": "Date", "count": "Registrations"},
                template="plotly_dark",
                color_discrete_sequence=["#6C63FF"],
            )
            fig_daily.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_daily, use_container_width=True)

        br_col, yr_col = st.columns(2)
        with br_col:
            section_header("Engineering Branch Distribution")
            if metrics["branch_data"]:
                df_br = pd.DataFrame(metrics["branch_data"])
                fig_br = px.bar(
                    df_br, x="count", y="branch", orientation="h",
                    template="plotly_dark",
                    color_discrete_sequence=["#00C9A7"],
                    labels={"branch": "Branch", "count": "Registrations"},
                )
                fig_br.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig_br, use_container_width=True)

        with yr_col:
            section_header("Graduation Year Distribution")
            if metrics["year_data"]:
                df_yr = pd.DataFrame(metrics["year_data"])
                df_yr["year"] = df_yr["year"].astype(str)
                fig_yr = px.bar(
                    df_yr, x="year", y="count",
                    template="plotly_dark",
                    color_discrete_sequence=["#FF6B6B"],
                    labels={"year": "Grad Year", "count": "Registrations"},
                )
                fig_yr.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig_yr, use_container_width=True)

    # Recent Registrations
    section_header("Recent Registrations")
    recent = metrics["recent_registrations"]
    if not recent:
        st.caption("No registrations yet.")
    else:
        import pandas as pd
        df_recent = pd.DataFrame(recent)
        df_recent = df_recent.rename(columns={
            "student_name": "Name",
            "college_name": "College",
            "branch": "Branch",
            "graduation_year": "Grad Year",
            "acquisition_channel": "Channel",
            "referral_code": "Ref Code",
            "registered_at": "Registered At (UTC)",
            "is_synthetic": "Synthetic",
        })
        df_recent["Synthetic"] = df_recent["Synthetic"].apply(lambda x: "✅ Yes" if x else "No")
        st.dataframe(df_recent, use_container_width=True)

    # Channel Target vs Actual
    section_header("Proposed vs Actual Channel Targets")
    st.markdown(
        '<div class="alert-info">ℹ️ Targets below are <em>proposed</em> allocations for the campaign plan — '
        'not observed results.</div>',
        unsafe_allow_html=True,
    )
    allocation = get_channel_target_allocation()
    actual_by_channel = {r["channel"]: r["count"] for r in metrics["channel_data"]}
    df_alloc = pd.DataFrame([
        {
            "Channel": a["channel"],
            "Proposed Target": a["proposed_target"],
            "Actual": actual_by_channel.get(
                # Try to match by partial name
                next((ch for ch in actual_by_channel if a["channel"].split()[0].lower() in ch.lower()), ""),
                0,
            ),
        }
        for a in allocation
    ])
    st.dataframe(df_alloc, use_container_width=True)

    # Proposed experiments
    section_header("Proposed Growth Experiments")
    st.markdown(
        '<div class="alert-info">ℹ️ These experiments are proposed only — not yet executed.</div>',
        unsafe_allow_html=True,
    )
    for exp in PROPOSED_EXPERIMENTS:
        with st.expander(f"**{exp['id']}** — {exp['name']} ({exp['status']})"):
            st.markdown(f"**Hypothesis:** {exp['hypothesis']}")
            st.markdown(f"**Variable:** {exp['variable']}")
            st.markdown("**Variants:**")
            for v in exp["variants"]:
                st.markdown(f"  - {v}")
            st.markdown(f"**Success Metric:** {exp['success_metric']}")
            st.markdown(f"**Minimum Data Needed:** {exp['minimum_data']}")
            st.markdown(f"**If Positive:** {exp['action_if_positive']}")
            st.markdown(f"**If Negative:** {exp['action_if_negative']}")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE G — DATA EXPORT
# ═════════════════════════════════════════════════════════════════════════════

elif page == "📁 Export Data":
    st.markdown(f'<div class="brand-header"><h1>📁 Export Data</h1><p>Download CSV reports from live database records</p></div>', unsafe_allow_html=True)

    # Auth gate
    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False

    if not st.session_state["admin_authenticated"]:
        st.markdown(
            '<div class="alert-info">🔒 Data exports require admin access. '
            'Please log in from the Dashboard page first.</div>',
            unsafe_allow_html=True,
        )
        pw2 = st.text_input("Admin Password", type="password", key="export_pw")
        if st.button("Login", type="primary", key="export_login"):
            if pw2 == get_admin_password():
                st.session_state["admin_authenticated"] = True
                st.rerun()
            else:
                st.markdown('<div class="alert-error">❌ Incorrect password.</div>', unsafe_allow_html=True)
        st.stop()

    section_header("Available Exports")

    now_str = datetime.utcnow().strftime("%Y%m%d_%H%M")

    # 1. Full registrations (with PII — admin only)
    with st.container():
        st.markdown("#### 1. Workshop Registrations (Full — includes PII)")
        st.markdown("Contains student names, emails, and all registration details. Admin use only.")
        cols = st.columns([2, 1])
        with cols[0]:
            st.markdown('<div class="alert-warning">⚠️ Contains personal information. Do not share publicly.</div>', unsafe_allow_html=True)
        with cols[1]:
            csv_data = export_registrations_csv(include_personal=True, only_real=True)
            st.download_button(
                "⬇️ Download Registrations (Full)",
                data=csv_data,
                file_name=f"careerconnect_registrations_{now_str}.csv",
                mime="text/csv",
            )

    st.markdown("---")

    # 2. Analytical registrations (no PII)
    with st.container():
        st.markdown("#### 2. Registrations — Analytical (No PII)")
        st.markdown("Branch, college, year, and channel data only. Safe for sharing.")
        csv_data2 = export_registrations_csv(include_personal=False, only_real=True)
        st.download_button(
            "⬇️ Download Analytical Export",
            data=csv_data2,
            file_name=f"careerconnect_registrations_analytical_{now_str}.csv",
            mime="text/csv",
        )

    st.markdown("---")

    # 3. Channel performance
    with st.container():
        st.markdown("#### 3. Channel Performance")
        csv_data3 = export_channel_performance_csv(only_real=True)
        st.download_button(
            "⬇️ Download Channel Performance",
            data=csv_data3,
            file_name=f"careerconnect_channels_{now_str}.csv",
            mime="text/csv",
        )

    st.markdown("---")

    # 4. Referral performance
    with st.container():
        st.markdown("#### 4. Referral Code Performance")
        csv_data4 = export_referral_performance_csv(only_real=True)
        st.download_button(
            "⬇️ Download Referral Performance",
            data=csv_data4,
            file_name=f"careerconnect_referrals_{now_str}.csv",
            mime="text/csv",
        )

    st.markdown("---")

    # 5. Daily summary
    with st.container():
        st.markdown("#### 5. Daily Registration Summary")
        csv_data5 = export_daily_summary_csv(only_real=True)
        st.download_button(
            "⬇️ Download Daily Summary",
            data=csv_data5,
            file_name=f"careerconnect_daily_{now_str}.csv",
            mime="text/csv",
        )

    st.markdown("---")

    # 6. Campaign metrics
    with st.container():
        st.markdown("#### 6. Campaign Metrics Summary")
        csv_data6 = export_campaign_metrics_csv(expenditure_inr=0.0, only_real=True)
        st.download_button(
            "⬇️ Download Campaign Metrics",
            data=csv_data6,
            file_name=f"careerconnect_metrics_{now_str}.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.caption("All exports are generated from the live SQLite database. Empty exports indicate no matching records.")
    st.caption("Date/time: UTC. Exports include a BOM character for Microsoft Excel compatibility.")

