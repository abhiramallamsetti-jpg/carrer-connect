"""
CareerConnect — Growth Plan PPTX Generator
Creates the five-slide NxtWave Growth Challenge presentation using python-pptx.
Run this script directly: python generate_pptx.py
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pathlib import Path


# ── Colours ──────────────────────────────────────────────────────────────────
PRIMARY   = RGBColor(0x6C, 0x63, 0xFF)   # #6C63FF  brand purple
SECONDARY = RGBColor(0x00, 0xC9, 0xA7)   # #00C9A7  brand teal
ACCENT    = RGBColor(0xFF, 0x6B, 0x6B)   # #FF6B6B  warm red
BG_DARK   = RGBColor(0x0E, 0x11, 0x17)   # #0E1117  dark bg
BG_CARD   = RGBColor(0x1A, 0x1D, 0x23)   # #1A1D23  card bg
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREY= RGBColor(0xB0, 0xB8, 0xC1)


def set_slide_bg(slide, color: RGBColor):
    """Fill slide background with a solid colour."""
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(
    slide, left, top, width, height,
    text, font_size=18, bold=False, color=WHITE,
    align=PP_ALIGN.LEFT, italic=False,
):
    """Add a simple textbox to a slide."""
    txb = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb


def add_rect(slide, left, top, width, height, fill_color: RGBColor, line_color=None):
    """Add a filled rectangle."""
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(left), Inches(top), Inches(width), Inches(height),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
    else:
        shape.line.fill.background()
    return shape


def add_bullet_textbox(
    slide, left, top, width, height,
    bullets: list, title: str = "",
    title_size=16, bullet_size=13,
    title_color=SECONDARY, bullet_color=LIGHT_GREY,
):
    """Add a textbox with an optional title and a list of bullet points."""
    txb = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txb.text_frame
    tf.word_wrap = True

    if title:
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = title
        run.font.size = Pt(title_size)
        run.font.bold = True
        run.font.color.rgb = title_color

    for i, bullet in enumerate(bullets):
        if title or i > 0:
            p = tf.add_paragraph()
        else:
            p = tf.paragraphs[0]
        run = p.add_run()
        run.text = f"• {bullet}"
        run.font.size = Pt(bullet_size)
        run.font.color.rgb = bullet_color
        p.space_before = Pt(2)

    return txb


# ── Slides ───────────────────────────────────────────────────────────────────

def build_slide_1(prs):
    """SLIDE 1 — Objective and Audience."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    set_slide_bg(slide, BG_DARK)

    # Purple header bar
    add_rect(slide, 0, 0, 10, 1.4, PRIMARY)

    # Slide number
    add_textbox(slide, 9.2, 0.05, 0.7, 0.3, "1 / 5",
                font_size=10, color=WHITE, align=PP_ALIGN.RIGHT)

    # Title
    add_textbox(slide, 0.3, 0.15, 9.0, 1.1,
                "CareerConnect — Growth Plan",
                font_size=30, bold=True, color=WHITE)

    add_textbox(slide, 0.3, 1.05, 5.0, 0.4,
                "NxtWave Growth Intern Challenge",
                font_size=13, color=SECONDARY, italic=True)

    # Objective block
    add_rect(slide, 0.3, 1.6, 4.4, 5.0, BG_CARD)
    add_bullet_textbox(
        slide, 0.5, 1.7, 4.1, 4.8,
        title="🎯  Objective",
        bullets=[
            "Plan 500 unique workshop registrations",
            "in 7 days with ≤ ₹2,000 budget",
            "",
            "Workshop:",
            "\"Build Your First AI Project",
            "  in 60 Minutes\"",
            "",
            "Organiser: NxtWave (details TBC)",
        ],
        title_size=15, bullet_size=12,
    )

    # Audience block
    add_rect(slide, 5.0, 1.6, 4.7, 5.0, BG_CARD)
    add_bullet_textbox(
        slide, 5.2, 1.7, 4.4, 4.8,
        title="👥  Target Audience",
        bullets=[
            "Final-year engineering students",
            "All branches welcome",
            "2025–2027 graduation cohort",
            "",
            "📌  Key Assumptions",
            "• Online workshop (free)",
            "• Date/speaker TBC by organiser",
            "• Organic channels tested first",
            "• No guarantee of real execution",
        ],
        title_size=15, bullet_size=12,
    )

    # Footer
    add_textbox(slide, 0.3, 6.9, 9.4, 0.3,
                "⚠️  All targets are proposed — not observed results.",
                font_size=9, color=ACCENT, italic=True)


def build_slide_2(prs):
    """SLIDE 2 — Growth Channels."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)

    add_rect(slide, 0, 0, 10, 0.9, PRIMARY)
    add_textbox(slide, 0.3, 0.12, 8.0, 0.7,
                "Growth Channels & Tracking Strategy",
                font_size=24, bold=True, color=WHITE)
    add_textbox(slide, 9.0, 0.05, 0.8, 0.3, "2 / 5",
                font_size=10, color=WHITE, align=PP_ALIGN.RIGHT)

    channels = [
        ("📱  WhatsApp", "180 reg.", "WHATSAPP01",
         ["College engineering groups", "High reach, trusted source",
          "Requires admin permission"]),
        ("💼  LinkedIn", "100 reg.", "LINKEDIN01",
         ["Professional student profiles", "Good for final-year students",
          "Post + engage with comments"]),
        ("✈️  Telegram", "100 reg.", "TELEGRAM01",
         ["Active tech communities", "Fast information sharing",
          "Free to post with permission"]),
        ("🏫  Clubs & Referrals", "120 reg.", "CAMPUS01",
         ["Student coordinators", "High-trust personal referrals",
          "Volunteer ambassador model"]),
    ]

    col_w = 2.3
    for i, (ch, target, code, points) in enumerate(channels):
        x = 0.15 + i * col_w
        add_rect(slide, x, 1.0, col_w - 0.15, 5.8, BG_CARD)
        add_textbox(slide, x + 0.1, 1.1, col_w - 0.3, 0.6,
                    ch, font_size=13, bold=True, color=SECONDARY)
        add_textbox(slide, x + 0.1, 1.65, col_w - 0.3, 0.35,
                    f"Target: {target}", font_size=11, color=WHITE, bold=True)
        add_textbox(slide, x + 0.1, 2.0, col_w - 0.3, 0.3,
                    f"Code: {code}", font_size=10, color=PRIMARY, italic=True)
        for j, pt in enumerate(points):
            add_textbox(slide, x + 0.1, 2.4 + j * 0.4, col_w - 0.25, 0.38,
                        f"• {pt}", font_size=10, color=LIGHT_GREY)

        add_textbox(slide, x + 0.1, 5.9, col_w - 0.25, 0.5,
                    "Tracked via referral code in registration DB",
                    font_size=9, color=ACCENT, italic=True)

    add_textbox(slide, 0.3, 6.85, 9.4, 0.3,
                "Total proposed: 500 | Overlap buffer: track duplicates via email normalisation",
                font_size=9, color=LIGHT_GREY, italic=True)


def build_slide_3(prs):
    """SLIDE 3 — Seven-Day Plan and Budget."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)

    add_rect(slide, 0, 0, 10, 0.9, PRIMARY)
    add_textbox(slide, 0.3, 0.12, 8.5, 0.7,
                "7-Day Plan & ₹2,000 Budget",
                font_size=24, bold=True, color=WHITE)
    add_textbox(slide, 9.0, 0.05, 0.8, 0.3, "3 / 5",
                font_size=10, color=WHITE, align=PP_ALIGN.RIGHT)

    # Timeline column
    days = [
        ("Day 1", "Build website, DB, referral system, promotional assets"),
        ("Day 2", "Identify communities, prepare messages, seek admin permission"),
        ("Day 3", "Begin outreach — permitted WhatsApp & Telegram groups"),
        ("Day 4", "Review performance, A/B test messages, optimise channel focus"),
        ("Day 5", "Expand to college clubs and student coordinators"),
        ("Day 6", "Activate referral sharing, send permitted reminders"),
        ("Day 7", "Final push, analyse registrations, prepare report"),
    ]

    add_rect(slide, 0.2, 1.0, 5.8, 5.8, BG_CARD)
    add_textbox(slide, 0.4, 1.05, 5.5, 0.4,
                "📅  Proposed Schedule (not yet executed)",
                font_size=13, bold=True, color=SECONDARY)
    for i, (day, desc) in enumerate(days):
        y = 1.5 + i * 0.72
        add_textbox(slide, 0.4, y, 1.0, 0.38,
                    day, font_size=11, bold=True, color=PRIMARY)
        add_textbox(slide, 1.4, y, 4.4, 0.38,
                    desc, font_size=10, color=LIGHT_GREY)

    # Budget column
    add_rect(slide, 6.2, 1.0, 3.6, 5.8, BG_CARD)
    add_textbox(slide, 6.4, 1.05, 3.3, 0.4,
                "💰  Budget Allocation",
                font_size=13, bold=True, color=SECONDARY)
    budget_rows = [
        ("Website & Tools", "₹0", "Open-source / local"),
        ("Organic Outreach", "₹0", "Permission-based"),
        ("Paid Promotion*", "₹1,000", "Only after organic test"),
        ("Contingency", "₹1,000", "Buffer for changes"),
        ("TOTAL", "₹2,000", "Maximum available"),
    ]
    for i, (item, amt, note) in enumerate(budget_rows):
        y = 1.6 + i * 0.85
        bold = item == "TOTAL"
        color = SECONDARY if bold else WHITE
        add_textbox(slide, 6.4, y, 1.8, 0.35, item,
                    font_size=11, bold=bold, color=color)
        add_textbox(slide, 8.2, y, 1.0, 0.35, amt,
                    font_size=11, bold=bold, color=color, align=PP_ALIGN.RIGHT)
        add_textbox(slide, 6.4, y + 0.3, 2.8, 0.3, note,
                    font_size=9, color=LIGHT_GREY, italic=True)

    add_textbox(slide, 0.3, 6.85, 9.4, 0.3,
                "*Paid spend only if organic underperforms — test first, spend later.",
                font_size=9, color=ACCENT, italic=True)


def build_slide_4(prs):
    """SLIDE 4 — CareerConnect Working Asset."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)

    add_rect(slide, 0, 0, 10, 0.9, PRIMARY)
    add_textbox(slide, 0.3, 0.12, 8.5, 0.7,
                "CareerConnect — Working Asset",
                font_size=24, bold=True, color=WHITE)
    add_textbox(slide, 9.0, 0.05, 0.8, 0.3, "4 / 5",
                font_size=10, color=WHITE, align=PP_ALIGN.RIGHT)

    features = [
        ("🏠 Home Page",
         ["CareerConnect brand & tagline", "Workshop banner",
          "Featured opportunities", "CTA buttons"]),
        ("📝 Registration",
         ["7-field validated form", "Email normalisation & dedup",
          "Referral code auto-fill", "SQLite persistence"]),
        ("🔗 Referral Tracking",
         ["4 default codes (CAMPUS01…)", "URL param auto-prefill",
          "Per-code reg counts", "Shareable message generator"]),
        ("📊 Dashboard",
         ["Live metrics from DB", "Plotly charts (channel, trend…)",
          "Password-protected", "Proposed vs actual view"]),
        ("📁 CSV Export",
         ["6 export types", "Full + analytical (no PII)",
          "Channel & referral perf.", "Campaign metrics summary"]),
        ("🤖 Workshop Page",
         ["Honest unconfirmed details", "FAQ section",
          "Proposed topics", "Register CTA"]),
    ]

    col_w, col_h = 3.0, 2.6
    for i, (title, pts) in enumerate(features):
        col = i % 3
        row = i // 3
        x = 0.2 + col * col_w + col * 0.1
        y = 1.05 + row * (col_h + 0.15)
        add_rect(slide, x, y, col_w, col_h, BG_CARD)
        add_textbox(slide, x + 0.15, y + 0.1, col_w - 0.3, 0.45,
                    title, font_size=12, bold=True, color=SECONDARY)
        for j, pt in enumerate(pts):
            add_textbox(slide, x + 0.15, y + 0.55 + j * 0.42,
                        col_w - 0.3, 0.38,
                        f"• {pt}", font_size=10, color=LIGHT_GREY)

    add_textbox(slide, 0.3, 6.85, 9.4, 0.3,
                "Run locally: python -m streamlit run app.py | All 65 automated tests passing",
                font_size=9, color=SECONDARY, italic=True)


def build_slide_5(prs):
    """SLIDE 5 — AI Usage and Learning."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, BG_DARK)

    add_rect(slide, 0, 0, 10, 0.9, PRIMARY)
    add_textbox(slide, 0.3, 0.12, 8.5, 0.7,
                "AI Usage & What I Learned",
                font_size=24, bold=True, color=WHITE)
    add_textbox(slide, 9.0, 0.05, 0.8, 0.3, "5 / 5",
                font_size=10, color=WHITE, align=PP_ALIGN.RIGHT)

    # AI-assisted decisions (left column)
    add_rect(slide, 0.2, 1.0, 5.8, 3.8, BG_CARD)
    add_textbox(slide, 0.4, 1.05, 5.5, 0.4,
                "🤖  AI-Assisted Decisions",
                font_size=13, bold=True, color=SECONDARY)

    ai_items = [
        ("1. Database schema design",
         "AI suggested using UNIQUE COLLATE NOCASE on email → adopted for "
         "case-insensitive duplicate prevention."),
        ("2. Referral code URL param",
         "AI suggested extracting ?ref=CODE from URL and pre-filling the form "
         "→ implemented; improves user experience."),
        ("3. Export BOM encoding",
         "AI flagged that CSV exports need utf-8-sig BOM for Excel compatibility "
         "→ adopted in all export functions."),
    ]
    for i, (title, desc) in enumerate(ai_items):
        y = 1.55 + i * 0.95
        add_textbox(slide, 0.4, y, 5.5, 0.35,
                    title, font_size=11, bold=True, color=WHITE)
        add_textbox(slide, 0.4, y + 0.32, 5.5, 0.55,
                    desc, font_size=10, color=LIGHT_GREY)

    # Rejected suggestion (right column)
    add_rect(slide, 6.2, 1.0, 3.6, 3.8, BG_CARD)
    add_textbox(slide, 6.4, 1.05, 3.3, 0.4,
                "❌  AI Suggestion Rejected",
                font_size=13, bold=True, color=ACCENT)
    add_textbox(slide, 6.4, 1.5, 3.3, 0.35,
                "What was suggested:", font_size=11, bold=True, color=WHITE)
    add_textbox(slide, 6.4, 1.85, 3.3, 0.75,
                "Add an ML-based job recommender that matches student profiles "
                "to opportunities using embeddings.",
                font_size=10, color=LIGHT_GREY)
    add_textbox(slide, 6.4, 2.65, 3.3, 0.35,
                "Why rejected:", font_size=11, bold=True, color=WHITE)
    add_textbox(slide, 6.4, 3.0, 3.3, 1.0,
                "Adds external ML dependencies, outside challenge scope, risks "
                "over-engineering a prototype. Simple search/filter achieves the "
                "same goal without complexity.",
                font_size=10, color=LIGHT_GREY)

    # What I'd improve
    add_rect(slide, 0.2, 5.0, 9.6, 1.75, BG_CARD)
    add_textbox(slide, 0.4, 5.05, 9.3, 0.4,
                "🔮  With 24 More Hours I Would…",
                font_size=13, bold=True, color=SECONDARY)
    improvements = [
        "Test registration with 5–10 real students to find UX friction",
        "Improve channel attribution (multi-touch) for overlapping audiences",
        "Add rate limiting and CAPTCHA before any public deployment",
        "Test A/B message variations on a small WhatsApp pilot group",
    ]
    for i, pt in enumerate(improvements):
        col = i % 2
        row = i // 2
        x = 0.4 + col * 4.9
        y = 5.55 + row * 0.5
        add_textbox(slide, x, y, 4.7, 0.42,
                    f"• {pt}", font_size=10, color=LIGHT_GREY)

    add_textbox(slide, 0.3, 6.85, 9.4, 0.3,
                "All AI decisions documented in deliverables/AI_Learning_Notes.md",
                font_size=9, color=LIGHT_GREY, italic=True)


# ── Main ─────────────────────────────────────────────────────────────────────

def generate_pptx(output_path: Path) -> Path:
    prs = Presentation()
    prs.slide_width  = Inches(10)
    prs.slide_height = Inches(7.5)

    build_slide_1(prs)
    build_slide_2(prs)
    build_slide_3(prs)
    build_slide_4(prs)
    build_slide_5(prs)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))
    print(f"[OK] Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "deliverables" / "CareerConnect_Growth_Plan.pptx"
    generate_pptx(out)
