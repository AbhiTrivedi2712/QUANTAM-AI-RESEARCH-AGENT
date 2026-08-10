#!/usr/bin/env python3
"""
QUANTUM Financial Intelligence Agent
PREMIUM Redesign — Black + Gold Single Palette
Capgemini AgentifAI Deep Dive Round 2025
Team: Logic Legends

Run: python -X utf8 create_ppt.py
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ═══════════════════════════════════════════════════════════════════
#  SINGLE COLOR PALETTE — Premium Black + Gold/Amber only
#  Matches the actual QUANTUM dashboard UI colour language
# ═══════════════════════════════════════════════════════════════════
BG      = RGBColor(0x05, 0x05, 0x05)   # #050505  pure-black background
CARD    = RGBColor(0x11, 0x11, 0x11)   # #111111  primary card
CARD2   = RGBColor(0x1b, 0x1b, 0x1b)   # #1b1b1b  elevated card
AMBER   = RGBColor(0xFF, 0x8C, 0x42)   # #FF8C42  orange accent (matches rest of deck)
AMBER_S = RGBColor(0x8f, 0x3e, 0x00)   # #8f3e00  subtle orange fill
WHITE   = RGBColor(0xff, 0xff, 0xff)
LGRAY   = RGBColor(0x9c, 0xa3, 0xaf)   # #9ca3af  body text
MGRAY   = RGBColor(0x52, 0x52, 0x52)   # #525252  muted / deemphasized
BORDER  = RGBColor(0x28, 0x28, 0x28)   # #282828  subtle card border
BORDER2 = RGBColor(0x3c, 0x3c, 0x3c)   # #3c3c3c  stronger border

FONT = "Calibri"
SW   = Inches(13.33)
SH   = Inches(7.50)

# ═══════════════════════════════════════════════════════════════════
#  IMAGE PATHS  — auto-discovered from brain artifacts directory
# ═══════════════════════════════════════════════════════════════════
BRAIN = r"C:\Users\singh\.gemini\antigravity-ide\brain\61595afa-300c-4366-9516-2a9d23928c1a"

def _find(pattern):
    if not os.path.isdir(BRAIN):
        return ""
    for f in sorted(os.listdir(BRAIN), reverse=True):
        if all(p in f for p in pattern.split("|")) and f.endswith(".png"):
            return os.path.join(BRAIN, f)
    return ""

ARCH_IMG      = _find("arch_v2")
PIPELINE_IMG  = _find("pipeline_v2")
DASH_SCREEN1  = _find("dashboard_screen1")
DASH_SCREEN2  = _find("dashboard_screen2")


# ═══════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════

def new_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, SW, SH)
    bg.fill.solid();  bg.fill.fore_color.rgb = BG;  bg.line.fill.background()
    return s


def box(s, l, t, w, h, fill, lc=None, lw=Pt(0.5)):
    shp = s.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shp.fill.solid();  shp.fill.fore_color.rgb = fill
    if lc:   shp.line.color.rgb = lc;  shp.line.width = lw
    else:    shp.line.fill.background()
    return shp


def tb(s, text, l, t, w, h, size=14, bold=False, color=WHITE,
       align=PP_ALIGN.LEFT, italic=False, font=FONT):
    txb = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf  = txb.text_frame;  tf.word_wrap = True
    p   = tf.paragraphs[0];  p.alignment = align
    r   = p.add_run();  r.text = text
    r.font.size = Pt(size);  r.font.bold = bold;  r.font.italic = italic
    r.font.color.rgb = color;  r.font.name = font
    return txb


def ml_tb(s, lines, l, t, w, h, size=12, color=LGRAY,
          bold=False, align=PP_ALIGN.LEFT, font=FONT):
    txb = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf  = txb.text_frame;  tf.word_wrap = True
    first = True
    for line in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        r = p.add_run();  r.text = line
        r.font.size = Pt(size);  r.font.bold = bold
        r.font.color.rgb = color;  r.font.name = font
    return txb


def img(s, path, l, t, w, h, label="[ Image ]"):
    if path and os.path.exists(path):
        s.shapes.add_picture(path, Inches(l), Inches(t), Inches(w), Inches(h))
    else:
        box(s, l, t, w, h, CARD, BORDER2)
        tb(s, label, l+0.1, t+h/2-0.18, w-0.2, 0.36,
           size=10, color=MGRAY, align=PP_ALIGN.CENTER)


def slide_header(s, title, subtitle=None, top=0.30):
    """Premium slide header: large white title + thin amber underline."""
    tb(s, title, 0.55, top, 12.4, 0.9, size=40, bold=True, color=WHITE)
    uy = top + (1.15 if subtitle else 0.95)
    if subtitle:
        tb(s, subtitle, 0.55, top+0.88, 12.4, 0.38, size=13, color=LGRAY, italic=True)
    box(s, 0.55, uy, 1.6, 0.038, AMBER)          # amber underline


def amber_tag(s, text, l, t, w=2.8, h=0.28):
    """Small amber-bordered label pill."""
    box(s, l, t, w, h, BG, AMBER, Pt(0.75))
    tb(s, text, l+0.08, t+0.04, w-0.12, h-0.06,
       size=8, bold=True, color=AMBER)


def numbered_item(s, num, title, body, l, t, w, h,
                  num_size=32, title_size=14, body_size=11):
    """Premium numbered item: big amber number + white title + gray body."""
    box(s, l, t, w, h, CARD, BORDER)
    # Number badge
    tb(s, str(num).zfill(2), l+0.14, t+0.08, 0.7, 0.55,
       size=num_size, bold=True, color=AMBER)
    # Thin amber separator line
    box(s, l+0.14, t+0.62, 0.5, 0.032, AMBER)
    # Title
    tb(s, title, l+0.14, t+0.72, w-0.28, 0.38, size=title_size, bold=True, color=WHITE)
    # Body
    if isinstance(body, list):
        ml_tb(s, body, l+0.14, t+1.12, w-0.28, h-1.22, size=body_size, color=LGRAY)
    else:
        tb(s, body, l+0.14, t+1.12, w-0.28, h-1.22, size=body_size, color=LGRAY)


def clean_card(s, l, t, w, h, title, body, title_size=13.5, body_size=11,
               accent=True):
    """Minimal card: subtle border, amber left bar, clean typography."""
    box(s, l, t, w, h, CARD, BORDER)
    if accent:
        box(s, l, t, 0.045, h, AMBER)
    tb(s, title, l+0.12, t+0.1, w-0.2, 0.38,
       size=title_size, bold=True, color=WHITE)
    if isinstance(body, list):
        ml_tb(s, body, l+0.12, t+0.52, w-0.2, h-0.62, size=body_size, color=LGRAY)
    else:
        tb(s, body, l+0.12, t+0.52, w-0.2, h-0.62, size=body_size, color=LGRAY)


def divider(s, l, t, w=12.2):
    box(s, l, t, w, 0.012, BORDER2)


def slide_number(s, num):
    tb(s, str(num), 12.7, 7.1, 0.5, 0.32, size=11, color=MGRAY,
       align=PP_ALIGN.RIGHT)


# ═══════════════════════════════════════════════════════════════════
#  SLIDE 01 — COVER  (APPLE KEYNOTE × BLOOMBERG TERMINAL)
# ═══════════════════════════════════════════════════════════════════
def slide_01(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, SW, SH)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x05, 0x05, 0x05)
    bg.line.fill.background()

    ORANGE  = RGBColor(0xFF, 0x8C, 0x42)
    C_BG    = RGBColor(0x11, 0x11, 0x11)
    DIM     = RGBColor(0x28, 0x28, 0x28)
    LG      = RGBColor(0x9c, 0xa3, 0xaf)
    MG      = RGBColor(0x52, 0x52, 0x52)
    BLACK   = RGBColor(0x05, 0x05, 0x05)

    # ── Thin top orange stripe ─────────────────────────────────────
    box(s, 0, 0, 13.33, 0.06, ORANGE)

    # ── Vertical separator line (60/40 divider) ────────────────────
    box(s, 7.90, 0.06, 0.016, 7.44, RGBColor(0x22, 0x22, 0x22))

    # ══════════════════════════════════════════════════════════════
    #  LEFT SIDE  —  Product Story  (x=0.50 → 7.75, w=7.25)
    # ══════════════════════════════════════════════════════════════
    LX = 0.50   # left content x
    LW = 7.25   # left content width

    # ── Badge ─────────────────────────────────────────────────────
    badge = s.shapes.add_textbox(Inches(LX), Inches(0.16),
                                 Inches(LW), Inches(0.24))
    tf_b = badge.text_frame; tf_b.word_wrap = False
    tf_b.margin_top = Inches(0); tf_b.margin_bottom = Inches(0)
    tf_b.margin_left = Inches(0); tf_b.margin_right = Inches(0)
    p_b = tf_b.paragraphs[0]
    r_b1 = p_b.add_run()
    r_b1.text = "\u25c9  "
    r_b1.font.size = Pt(9.5); r_b1.font.color.rgb = ORANGE; r_b1.font.name = FONT
    r_b2 = p_b.add_run()
    r_b2.text = "Capgemini Exceller AgentifAI Buildathon 2026"
    r_b2.font.size = Pt(9.5); r_b2.font.bold = True
    r_b2.font.color.rgb = ORANGE; r_b2.font.name = FONT
    r_b3 = p_b.add_run()
    r_b3.text = "   \u2014   Deep Dive Round Submission"
    r_b3.font.size = Pt(9.5); r_b3.font.color.rgb = LG; r_b3.font.name = FONT

    # ── QUANTUM  (hero, 78pt — guaranteed single line in LW=7.25") ─
    tb(s, "QUANTUM", LX - 0.02, 0.50, 7.50, 1.20,
       size=78, bold=True, color=WHITE)

    # ── "Financial Intelligence Agent" ────────────────────────────
    tb(s, "Financial Intelligence Agent", LX, 1.72, LW, 0.56,
       size=30, bold=True, color=ORANGE)

    # ── Tagline (2-line, mixed colour) ────────────────────────────
    tg = s.shapes.add_textbox(Inches(LX), Inches(2.36),
                              Inches(LW), Inches(0.58))
    tf_tg = tg.text_frame; tf_tg.word_wrap = True
    tf_tg.margin_top = Inches(0); tf_tg.margin_bottom = Inches(0)
    tf_tg.margin_left = Inches(0); tf_tg.margin_right = Inches(0)
    p_tg1 = tf_tg.paragraphs[0]
    r_tg1 = p_tg1.add_run()
    r_tg1.text = "Transforming Market Noise Into"
    r_tg1.font.size = Pt(15); r_tg1.font.italic = True
    r_tg1.font.color.rgb = LG; r_tg1.font.name = FONT
    p_tg2 = tf_tg.add_paragraph()
    r_tg2 = p_tg2.add_run()
    r_tg2.text = "Institutional Investment Conviction"
    r_tg2.font.size = Pt(15); r_tg2.font.bold = True; r_tg2.font.italic = True
    r_tg2.font.color.rgb = ORANGE; r_tg2.font.name = FONT

    # ── Thin orange micro-divider ─────────────────────────────────
    box(s, LX, 3.02, 4.50, 0.025, ORANGE)

    # ── Value Proposition ─────────────────────────────────────────
    vp = s.shapes.add_textbox(Inches(LX), Inches(3.10),
                              Inches(LW), Inches(0.52))
    tf_vp = vp.text_frame; tf_vp.word_wrap = True
    tf_vp.margin_top = Inches(0); tf_vp.margin_bottom = Inches(0)
    tf_vp.margin_left = Inches(0); tf_vp.margin_right = Inches(0)
    p_vp = tf_vp.paragraphs[0]
    r_vp = p_vp.add_run()
    r_vp.text = ("A Multi-Agent AI platform combining Technical Analysis, "
                 "Fundamental Research, and News Intelligence to generate "
                 "institutional-grade investment intelligence for retail investors.")
    r_vp.font.size = Pt(11); r_vp.font.color.rgb = LG; r_vp.font.name = FONT

    # ── 4 KEY METRIC CARDS  (y=3.74, h=1.06) ─────────────────────
    metrics = [
        ("4",            "Specialized\nAI Agents"),
        ("100+",         "Financial\nIndicators"),
        ("Real-Time",    "News\nIntelligence"),
        ("Institutional","Research\nReports"),
    ]
    mc_h  = 1.06
    mc_y  = 3.74
    mc_gap = 0.12
    mc_w  = (LW - 3 * mc_gap) / 4   # 1.7325

    for m_i, (num, lbl) in enumerate(metrics):
        mx = LX + m_i * (mc_w + mc_gap)

        # Card shell
        box(s, mx, mc_y, mc_w, mc_h, C_BG, DIM, Pt(0.75))
        # Orange top accent
        box(s, mx, mc_y, mc_w, 0.04, ORANGE)

        # Big number / keyword
        tb(s, num, mx + 0.08, mc_y + 0.10, mc_w - 0.14, 0.46,
           size=20, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

        # Label (2-line possible)
        tb(s, lbl, mx + 0.06, mc_y + 0.60, mc_w - 0.10, 0.42,
           size=8.5, color=LG, align=PP_ALIGN.CENTER)

    # ── TEAM ROW  (compact, y=4.94) ───────────────────────────────
    tb(s, "TEAM", LX, 4.90, 0.72, 0.20,
       size=8, bold=True, color=ORANGE)
    box(s, LX + 0.80, 4.97, LW - 0.80, 0.014, DIM)

    team = [
        ("Vedant Saubhri",       "Architecture & Deploy"),
        ("Abhinav Trivedi",      "AI & Consensus"),
        ("Priyansh Sharma",      "Data & APIs"),
        ("Suhani Rai",           "News & Sentiment"),
        ("Ummehani Burhanuddin", "Frontend & UX"),
    ]
    tc_h  = 0.88
    tc_y  = 5.12
    tc_gap = 0.09
    tc_w  = (LW - 4 * tc_gap) / 5   # ~1.39"

    for t_i, (name, role) in enumerate(team):
        tx = LX + t_i * (tc_w + tc_gap)
        # Card: no heavy border — just a very subtle bg + left accent
        box(s, tx, tc_y, tc_w, tc_h, C_BG, DIM, Pt(0.5))
        box(s, tx, tc_y, 0.04, tc_h, ORANGE)
        tb(s, name, tx + 0.10, tc_y + 0.06, tc_w - 0.14, 0.32,
           size=9, bold=True, color=WHITE)
        tb(s, role, tx + 0.10, tc_y + 0.40, tc_w - 0.14, 0.40,
           size=7.5, color=LG)

    # ── B.Tech / Team info micro-line ─────────────────────────────
    tb(s, "B.Tech 3rd Year   \u2014   All-India Buildathon   \u2014   Logic Legends",
       LX, 6.10, LW, 0.22, size=8, color=MG)

    # ══════════════════════════════════════════════════════════════
    #  RIGHT SIDE  —  Dashboard Screenshot  (x=7.92 → 13.25)
    # ══════════════════════════════════════════════════════════════
    RX = 7.92    # right image x
    RW = 5.24    # right image width
    RY = 0.06    # top y
    RH = 7.38    # height

    # Outer orange glow frame (slightly larger than image)
    box(s, RX - 0.06, RY - 0.02, RW + 0.12, RH + 0.04,
        RGBColor(0x12, 0x06, 0x00), ORANGE, Pt(1.8))

    # Dashboard image
    if DASH_SCREEN1 and __import__("os").path.exists(DASH_SCREEN1):
        s.shapes.add_picture(DASH_SCREEN1,
                             Inches(RX), Inches(RY),
                             Inches(RW), Inches(RH))
    else:
        box(s, RX, RY, RW, RH, RGBColor(0x11, 0x11, 0x11), DIM)
        tb(s, "[ Dashboard Screenshot ]",
           RX + 0.20, RY + RH / 2 - 0.22, RW - 0.40, 0.44,
           size=11, color=LG, align=PP_ALIGN.CENTER)

    # "LIVE DEMO READY" badge  (bottom-right of image)
    box(s, RX + RW - 1.80, RY + RH - 0.48, 1.74, 0.38, ORANGE)
    tb(s, "\u25cf  LIVE DEMO READY",
       RX + RW - 1.80, RY + RH - 0.44, 1.74, 0.30,
       size=9, bold=True, color=BLACK, align=PP_ALIGN.CENTER)

    slide_number(s, 1)
    return s


# ═══════════════════════════════════════════════════════════════════
#  SLIDE 02 — THE PROBLEM
# ═══════════════════════════════════════════════════════════════════
def slide_02(prs):
    # Set background color to #050505 (Bloomberg Terminal style pitch black)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, SW, SH)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x05, 0x05, 0x05)
    bg.line.fill.background()

    # Top border highlight - premium orange (#FF8C42)
    ORANGE = RGBColor(0xFF, 0x8C, 0x42)
    box(s, 0, 0, 13.33, 0.06, ORANGE)

    # Category Tracker
    tb_track = s.shapes.add_textbox(Inches(0.55), Inches(0.18), Inches(5.0), Inches(0.22))
    tf_track = tb_track.text_frame
    tf_track.word_wrap = True
    tf_track.margin_top = Inches(0)
    tf_track.margin_bottom = Inches(0)
    tf_track.margin_left = Inches(0)
    tf_track.margin_right = Inches(0)
    p_track = tf_track.paragraphs[0]
    r_track = p_track.add_run()
    r_track.text = "STRATEGIC ANALYSIS"
    r_track.font.size = Pt(11)
    r_track.font.bold = True
    r_track.font.color.rgb = ORANGE
    r_track.font.name = FONT

    # Title (46 pt)
    tb(s, "THE PROBLEM WE ARE SOLVING", 0.55, 0.45, 12.2, 0.7, size=46, bold=True, color=WHITE)

    # Subtitle (20 pt) with orange highlights
    tb_sub = s.shapes.add_textbox(Inches(0.55), Inches(1.15), Inches(12.2), Inches(0.40))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_top = Inches(0)
    tf_sub.margin_bottom = Inches(0)
    tf_sub.margin_left = Inches(0)
    tf_sub.margin_right = Inches(0)
    p_sub = tf_sub.paragraphs[0]
    
    r_sub1 = p_sub.add_run()
    r_sub1.text = "Retail investors are surrounded by financial information but lack "
    r_sub1.font.size = Pt(20)
    r_sub1.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_sub1.font.name = FONT
    r_sub1.font.italic = True
    
    r_sub2 = p_sub.add_run()
    r_sub2.text = "institutional-grade decision intelligence."
    r_sub2.font.size = Pt(20)
    r_sub2.font.bold = True
    r_sub2.font.color.rgb = ORANGE
    r_sub2.font.name = FONT
    r_sub2.font.italic = True

    # Left Column: Infographic Visual
    visual_img = _find("premium_overload_infographic")
    img(s, visual_img, 0.55, 1.65, 5.35, 3.8, "[ INFORMATION OVERLOAD ]")

    # Right Column: Problem Cards
    cards_data = [
        ("INFORMATION OVERLOAD", "Investors manually analyze charts, earnings reports, market news and financial statements across multiple platforms."),
        ("FRAGMENTED RESEARCH", "Critical market signals exist across disconnected tools, making research slow and inefficient."),
        ("DECISION PARALYSIS", "Conflicting technical, fundamental and news signals often result in delayed or emotional investment decisions.")
    ]

    card_y = 1.65
    for title, text in cards_data:
        # Subtle card box: #111111 background, very thin muted orange border
        box(s, 6.28, card_y, 6.5, 1.15, RGBColor(0x11, 0x11, 0x11), RGBColor(0x3c, 0x24, 0x12), Pt(0.75))
        
        # Title text box (with orange dot prefix)
        tb_title = s.shapes.add_textbox(Inches(6.43), Inches(card_y + 0.10), Inches(6.2), Inches(0.38))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        tf_title.margin_top = Inches(0)
        tf_title.margin_bottom = Inches(0)
        tf_title.margin_left = Inches(0)
        tf_title.margin_right = Inches(0)
        p_title = tf_title.paragraphs[0]
        
        # Orange square dot run
        r_dot = p_title.add_run()
        r_dot.text = "■  "
        r_dot.font.size = Pt(18)
        r_dot.font.bold = True
        r_dot.font.color.rgb = ORANGE
        r_dot.font.name = FONT
        
        # Title text run
        r_title = p_title.add_run()
        r_title.text = title
        r_title.font.size = Pt(24)
        r_title.font.bold = True
        r_title.font.color.rgb = ORANGE
        r_title.font.name = FONT

        # Body text box
        tb_body = s.shapes.add_textbox(Inches(6.43), Inches(card_y + 0.52), Inches(6.2), Inches(0.55))
        tf_body = tb_body.text_frame
        tf_body.word_wrap = True
        tf_body.margin_top = Inches(0)
        tf_body.margin_bottom = Inches(0)
        tf_body.margin_left = Inches(0)
        tf_body.margin_right = Inches(0)
        p_body = tf_body.paragraphs[0]
        r_body = p_body.add_run()
        r_body.text = text
        r_body.font.size = Pt(16)
        r_body.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
        r_body.font.name = FONT
        
        card_y += 1.30

    # Bottom Insight Bar: Full-width orange-highlighted card.
    # X = 0.55, Y = 5.60, Width = 12.23, Height = 1.35
    insight_bg = box(s, 0.55, 5.60, 12.23, 1.35, RGBColor(0x11, 0x11, 0x11), ORANGE, Pt(1))
    
    # Overlapping tab on top-left: KEY INSIGHT (solid orange, black text)
    box(s, 0.75, 5.46, 1.50, 0.28, ORANGE)
    tb_key = s.shapes.add_textbox(Inches(0.75), Inches(5.50), Inches(1.50), Inches(0.24))
    tf_key = tb_key.text_frame
    tf_key.word_wrap = True
    tf_key.margin_top = Inches(0)
    tf_key.margin_bottom = Inches(0)
    tf_key.margin_left = Inches(0)
    tf_key.margin_right = Inches(0)
    p_key = tf_key.paragraphs[0]
    p_key.alignment = PP_ALIGN.CENTER
    r_key = p_key.add_run()
    r_key.text = "KEY INSIGHT"
    r_key.font.size = Pt(10)
    r_key.font.bold = True
    r_key.font.color.rgb = RGBColor(0x05, 0x05, 0x05)
    r_key.font.name = FONT

    # Overlapping tab on top-right: OPPORTUNITY IDENTIFIED (outlined orange, orange text)
    box(s, 9.80, 5.46, 2.70, 0.28, RGBColor(0x11, 0x11, 0x11), ORANGE, Pt(0.75))
    tb_opp = s.shapes.add_textbox(Inches(9.80), Inches(5.50), Inches(2.70), Inches(0.24))
    tf_opp = tb_opp.text_frame
    tf_opp.word_wrap = True
    tf_opp.margin_top = Inches(0)
    tf_opp.margin_bottom = Inches(0)
    tf_opp.margin_left = Inches(0)
    tf_opp.margin_right = Inches(0)
    p_opp = tf_opp.paragraphs[0]
    p_opp.alignment = PP_ALIGN.CENTER
    r_opp = p_opp.add_run()
    r_opp.text = "OPPORTUNITY IDENTIFIED"
    r_opp.font.size = Pt(10)
    r_opp.font.bold = True
    r_opp.font.color.rgb = ORANGE
    r_opp.font.name = FONT

    # Bottom Bar Centered Text (17 pt italic orange)
    tb_ins_text = s.shapes.add_textbox(Inches(0.75), Inches(5.85), Inches(11.83), Inches(0.95))
    tf_ins_text = tb_ins_text.text_frame
    tf_ins_text.word_wrap = True
    tf_ins_text.margin_top = Inches(0)
    tf_ins_text.margin_bottom = Inches(0)
    tf_ins_text.margin_left = Inches(0)
    tf_ins_text.margin_right = Inches(0)
    p_ins_text = tf_ins_text.paragraphs[0]
    p_ins_text.alignment = PP_ALIGN.CENTER
    r_ins_text = p_ins_text.add_run()
    r_ins_text.text = ("\"Investors spend hours collecting information but only minutes making decisions. "
                      "The challenge is no longer access to data. The challenge is transforming data into actionable investment intelligence.\"")
    r_ins_text.font.size = Pt(17)
    r_ins_text.font.color.rgb = ORANGE
    r_ins_text.font.name = FONT
    r_ins_text.font.italic = True

    slide_number(s, 2)
    return s


# ═══════════════════════════════════════════════════════════════════
#  SLIDE 03 — OUR SOLUTION
# ═══════════════════════════════════════════════════════════════════
def slide_03(prs):
    # Set background color to #050505 (Bloomberg Terminal style pitch black)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, SW, SH)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x05, 0x05, 0x05)
    bg.line.fill.background()

    # Top border highlight - premium orange (#FF8C42)
    ORANGE = RGBColor(0xFF, 0x8C, 0x42)
    box(s, 0, 0, 13.33, 0.06, ORANGE)

    # Title (52 px = 39 pt)
    tb(s, "OUR SOLUTION", 0.55, 0.35, 12.2, 0.65, size=39, bold=True, color=WHITE)

    # Subtitle (20 pt) with orange highlights
    tb_sub = s.shapes.add_textbox(Inches(0.55), Inches(1.05), Inches(12.2), Inches(0.50))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_top = Inches(0)
    tf_sub.margin_bottom = Inches(0)
    tf_sub.margin_left = Inches(0)
    tf_sub.margin_right = Inches(0)
    p_sub = tf_sub.paragraphs[0]
    
    r_sub1 = p_sub.add_run()
    r_sub1.text = "Quantum automatically analyzes "
    r_sub1.font.size = Pt(20)
    r_sub1.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_sub1.font.name = FONT
    r_sub1.font.italic = True
    
    r_sub2 = p_sub.add_run()
    r_sub2.text = "technical signals, company fundamentals, and market sentiment"
    r_sub2.font.size = Pt(20)
    r_sub2.font.bold = True
    r_sub2.font.color.rgb = ORANGE
    r_sub2.font.name = FONT
    r_sub2.font.italic = True

    r_sub3 = p_sub.add_run()
    r_sub3.text = " to generate "
    r_sub3.font.size = Pt(20)
    r_sub3.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_sub3.font.name = FONT
    r_sub3.font.italic = True

    r_sub4 = p_sub.add_run()
    r_sub4.text = "explainable investment intelligence."
    r_sub4.font.size = Pt(20)
    r_sub4.font.bold = True
    r_sub4.font.color.rgb = ORANGE
    r_sub4.font.name = FONT
    r_sub4.font.italic = True

    # 4 columns for transformation flow
    col_w  = 2.60
    col_h  = 3.80
    col_y  = 1.65
    card_bg = RGBColor(0x11, 0x11, 0x11)
    muted_border = RGBColor(0x3c, 0x24, 0x12)
    inner_bg = RGBColor(0x16, 0x16, 0x16)

    # COLUMN 1: MARKET DATA SOURCES
    x1 = 0.55
    box(s, x1, col_y, col_w, col_h, card_bg, ORANGE, Pt(1))
    tb(s, "MARKET DATA\nSOURCES", x1 + 0.15, col_y + 0.15, col_w - 0.3, 0.60, size=19, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    
    inputs = [
        "📈  Yahoo Finance", 
        "📰  Google News RSS", 
        "📊  Technical Indicators", 
        "📄  Financial Statements"
    ]
    for idx, inp in enumerate(inputs):
        iy = col_y + 0.85 + idx * 0.68
        box(s, x1 + 0.15, iy, 2.30, 0.48, inner_bg, muted_border, Pt(0.5))
        tb_inp = s.shapes.add_textbox(Inches(x1 + 0.20), Inches(iy + 0.08), Inches(2.20), Inches(0.35))
        tf_inp = tb_inp.text_frame
        tf_inp.word_wrap = True
        tf_inp.margin_top = Inches(0)
        tf_inp.margin_bottom = Inches(0)
        tf_inp.margin_left = Inches(0)
        tf_inp.margin_right = Inches(0)
        p_inp = tf_inp.paragraphs[0]
        p_inp.alignment = PP_ALIGN.CENTER
        r_inp = p_inp.add_run()
        r_inp.text = inp
        r_inp.font.size = Pt(14)
        r_inp.font.color.rgb = WHITE
        r_inp.font.name = FONT

    # COLUMN 2: SPECIALIZED AI RESEARCH AGENTS (glowing central block)
    x2 = 3.76
    box(s, x2, col_y, col_w, col_h, card_bg, ORANGE, Pt(1.5))
    tb(s, "SPECIALIZED AI\nRESEARCH AGENTS", x2 + 0.10, col_y + 0.15, col_w - 0.2, 0.60, size=19, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    
    agents = [
        "📉  Technical Agent", 
        "🏢  Fundamental Agent", 
        "🧠  Sentiment Agent"
    ]
    for idx, ag in enumerate(agents):
        iy = col_y + 0.85 + idx * 0.68
        box(s, x2 + 0.15, iy, 2.30, 0.48, inner_bg, muted_border, Pt(0.5))
        tb_ag = s.shapes.add_textbox(Inches(x2 + 0.20), Inches(iy + 0.08), Inches(2.20), Inches(0.35))
        tf_ag = tb_ag.text_frame
        tf_ag.word_wrap = True
        tf_ag.margin_top = Inches(0)
        tf_ag.margin_bottom = Inches(0)
        tf_ag.margin_left = Inches(0)
        tf_ag.margin_right = Inches(0)
        p_ag = tf_ag.paragraphs[0]
        p_ag.alignment = PP_ALIGN.CENTER
        r_ag = p_ag.add_run()
        r_ag.text = ag
        r_ag.font.size = Pt(14)
        r_ag.font.bold = True
        r_ag.font.color.rgb = ORANGE
        r_ag.font.name = FONT
    # Underlying LLM Layer
    iy_llm = col_y + 2.95
    box(s, x2 + 0.15, iy_llm, 2.30, 0.48, ORANGE, muted_border, Pt(0.5))
    tb_llm = s.shapes.add_textbox(Inches(x2 + 0.20), Inches(iy_llm + 0.08), Inches(2.20), Inches(0.35))
    tf_llm = tb_llm.text_frame
    tf_llm.word_wrap = True
    tf_llm.margin_top = Inches(0)
    tf_llm.margin_bottom = Inches(0)
    tf_llm.margin_left = Inches(0)
    tf_llm.margin_right = Inches(0)
    p_llm = tf_llm.paragraphs[0]
    p_llm.alignment = PP_ALIGN.CENTER
    r_llm = p_llm.add_run()
    r_llm.text = "Groq LLM (Llama 3.3)"
    r_llm.font.size = Pt(14)
    r_llm.font.bold = True
    r_llm.font.color.rgb = RGBColor(0x05, 0x05, 0x05)
    r_llm.font.name = FONT

    # COLUMN 3: CONSENSUS ENGINE
    x3 = 6.97
    box(s, x3, col_y, col_w, col_h, card_bg, ORANGE, Pt(1))
    tb(s, "⚖  CONSENSUS\nENGINE", x3 + 0.15, col_y + 0.15, col_w - 0.3, 0.60, size=19, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    
    fusions = [
        "Weighted Aggregation", 
        "Confidence Scoring", 
        "Risk Assessment", 
        "Verdict Generation"
    ]
    for idx, fus in enumerate(fusions):
        iy = col_y + 0.85 + idx * 0.68
        box(s, x3 + 0.15, iy, 2.30, 0.48, inner_bg, muted_border, Pt(0.5))
        tb_fus = s.shapes.add_textbox(Inches(x3 + 0.20), Inches(iy + 0.08), Inches(2.20), Inches(0.35))
        tf_fus = tb_fus.text_frame
        tf_fus.word_wrap = True
        tf_fus.margin_top = Inches(0)
        tf_fus.margin_bottom = Inches(0)
        tf_fus.margin_left = Inches(0)
        tf_fus.margin_right = Inches(0)
        p_fus = tf_fus.paragraphs[0]
        p_fus.alignment = PP_ALIGN.CENTER
        r_fus = p_fus.add_run()
        r_fus.text = fus
        r_fus.font.size = Pt(14)
        r_fus.font.color.rgb = WHITE
        r_fus.font.name = FONT

    # COLUMN 4: INSTITUTIONAL RESEARCH OUTPUT (vertical cards, larger)
    x4 = 10.18
    box(s, x4, col_y, col_w, col_h, card_bg, ORANGE, Pt(1))
    tb(s, "📑  INSTITUTIONAL\nRESEARCH OUTPUT", x4 + 0.10, col_y + 0.15, col_w - 0.2, 0.60, size=19, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    
    outputs = [
        "Executive Investment Thesis", 
        "Bull vs Bear Analysis",
        "Risk Register", 
        "Catalyst Calendar",
        "Investment Decision Box", 
        "PDF Export"
    ]
    for idx, out_lbl in enumerate(outputs):
        iy = col_y + 0.85 + idx * 0.48
        box(s, x4 + 0.15, iy, 2.30, 0.40, inner_bg, muted_border, Pt(0.5))
        tb_out = s.shapes.add_textbox(Inches(x4 + 0.20), Inches(iy + 0.05), Inches(2.20), Inches(0.30))
        tf_out = tb_out.text_frame
        tf_out.word_wrap = True
        tf_out.margin_top = Inches(0)
        tf_out.margin_bottom = Inches(0)
        tf_out.margin_left = Inches(0)
        tf_out.margin_right = Inches(0)
        p_out = tf_out.paragraphs[0]
        p_out.alignment = PP_ALIGN.CENTER
        r_out = p_out.add_run()
        r_out.text = out_lbl
        r_out.font.size = Pt(12)
        r_out.font.color.rgb = WHITE
        r_out.font.name = FONT

    # Add large arrows between stages (+40% width: 0.45 x 0.50, MSO_SHAPE.RIGHT_ARROW is 33)
    for ax in [3.23, 6.44, 9.65]:
        ashp = s.shapes.add_shape(33, Inches(ax), Inches(col_y + 1.60), Inches(0.45), Inches(0.50))
        ashp.fill.solid()
        ashp.fill.fore_color.rgb = ORANGE
        ashp.line.fill.background()

    # BOTTOM HIGHLIGHT: KEY DIFFERENTIATOR
    insight_bg = box(s, 0.55, 5.60, 12.23, 1.35, RGBColor(0x11, 0x11, 0x11), ORANGE, Pt(1))
    
    # Overlapping tab on top-left: KEY DIFFERENTIATOR (solid orange, black text)
    box(s, 0.75, 5.46, 2.00, 0.28, ORANGE)
    tb_key = s.shapes.add_textbox(Inches(0.75), Inches(5.50), Inches(2.00), Inches(0.24))
    tf_key = tb_key.text_frame
    tf_key.word_wrap = True
    tf_key.margin_top = Inches(0)
    tf_key.margin_bottom = Inches(0)
    tf_key.margin_left = Inches(0)
    tf_key.margin_right = Inches(0)
    p_key = tf_key.paragraphs[0]
    p_key.alignment = PP_ALIGN.CENTER
    r_key = p_key.add_run()
    r_key.text = "KEY DIFFERENTIATOR"
    r_key.font.size = Pt(10)
    r_key.font.bold = True
    r_key.font.color.rgb = RGBColor(0x05, 0x05, 0x05)
    r_key.font.name = FONT

    # Bottom Bar Centered Text (18 pt italic white with orange highlight)
    tb_ins_text = s.shapes.add_textbox(Inches(0.75), Inches(5.85), Inches(11.83), Inches(0.95))
    tf_ins_text = tb_ins_text.text_frame
    tf_ins_text.word_wrap = True
    tf_ins_text.margin_top = Inches(0)
    tf_ins_text.margin_bottom = Inches(0)
    tf_ins_text.margin_left = Inches(0)
    tf_ins_text.margin_right = Inches(0)
    p_ins_text = tf_ins_text.paragraphs[0]
    p_ins_text.alignment = PP_ALIGN.CENTER
    
    r_ins1 = p_ins_text.add_run()
    r_ins1.text = "\"Instead of forcing investors to manually interpret fragmented market data, Quantum "
    r_ins1.font.size = Pt(18)
    r_ins1.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_ins1.font.name = FONT
    r_ins1.font.italic = True
    
    r_ins2 = p_ins_text.add_run()
    r_ins2.text = "performs the research automatically and delivers explainable investment intelligence."
    r_ins2.font.size = Pt(18)
    r_ins2.font.bold = True
    r_ins2.font.color.rgb = ORANGE
    r_ins2.font.name = FONT
    r_ins2.font.italic = True
    
    r_ins3 = p_ins_text.add_run()
    r_ins3.text = "\""
    r_ins3.font.size = Pt(18)
    r_ins3.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_ins3.font.name = FONT
    r_ins3.font.italic = True

    slide_number(s, 3)
    return s


# ═══════════════════════════════════════════════════════════════════
#  SLIDE 04 — HOW IT WORKS  (Pipeline + Tech Stack)
# ═══════════════════════════════════════════════════════════════════
def slide_04(prs):
    # Set background color to #050505 (Bloomberg Terminal style pitch black)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, SW, SH)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x05, 0x05, 0x05)
    bg.line.fill.background()

    # Top border highlight - premium orange (#FF8C42)
    ORANGE = RGBColor(0xFF, 0x8C, 0x42)
    box(s, 0, 0, 13.33, 0.06, ORANGE)

    # Title (40 pt)
    tb(s, "HOW QUANTUM WORKS", 0.55, 0.35, 12.2, 0.65, size=40, bold=True, color=WHITE)

    # Subtitle (20 pt) with orange highlights
    tb_sub = s.shapes.add_textbox(Inches(0.55), Inches(1.05), Inches(12.2), Inches(0.50))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_top = Inches(0)
    tf_sub.margin_bottom = Inches(0)
    tf_sub.margin_left = Inches(0)
    tf_sub.margin_right = Inches(0)
    p_sub = tf_sub.paragraphs[0]
    
    r_sub1 = p_sub.add_run()
    r_sub1.text = "From stock search to "
    r_sub1.font.size = Pt(20)
    r_sub1.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_sub1.font.name = FONT
    r_sub1.font.italic = True
    
    r_sub2 = p_sub.add_run()
    r_sub2.text = "institutional-grade investment intelligence"
    r_sub2.font.size = Pt(20)
    r_sub2.font.bold = True
    r_sub2.font.color.rgb = ORANGE
    r_sub2.font.name = FONT
    r_sub2.font.italic = True

    r_sub3 = p_sub.add_run()
    r_sub3.text = " in under 30 seconds."
    r_sub3.font.size = Pt(20)
    r_sub3.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_sub3.font.name = FONT
    r_sub3.font.italic = True

    # 6 columns layout
    col_w  = 1.65
    col_h  = 3.40
    col_y  = 1.65
    card_bg = RGBColor(0x11, 0x11, 0x11)

    # Helper to draw premium card
    def draw_premium_card(col_x, icon, title, keywords):
        # Card base
        box(s, col_x, col_y, col_w, col_h, card_bg, ORANGE, Pt(0.75))
        
        # Icon (36 pt orange, centered)
        tb_icon = s.shapes.add_textbox(Inches(col_x), Inches(col_y + 0.30), Inches(col_w), Inches(0.60))
        tf_icon = tb_icon.text_frame
        tf_icon.word_wrap = True
        tf_icon.margin_top = Inches(0)
        tf_icon.margin_bottom = Inches(0)
        tf_icon.margin_left = Inches(0)
        tf_icon.margin_right = Inches(0)
        p_icon = tf_icon.paragraphs[0]
        p_icon.alignment = PP_ALIGN.CENTER
        r_icon = p_icon.add_run()
        r_icon.text = icon
        r_icon.font.size = Pt(36)
        r_icon.font.color.rgb = ORANGE
        r_icon.font.name = FONT
        
        # Title (14 pt bold white, centered)
        tb_title = s.shapes.add_textbox(Inches(col_x + 0.05), Inches(col_y + 1.05), Inches(col_w - 0.10), Inches(0.50))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        tf_title.margin_top = Inches(0)
        tf_title.margin_bottom = Inches(0)
        tf_title.margin_left = Inches(0)
        tf_title.margin_right = Inches(0)
        p_title = tf_title.paragraphs[0]
        p_title.alignment = PP_ALIGN.CENTER
        r_title = p_title.add_run()
        r_title.text = title
        r_title.font.size = Pt(14)
        r_title.font.bold = True
        r_title.font.color.rgb = WHITE
        r_title.font.name = FONT

        # Muted divider line
        box(s, col_x + 0.20, col_y + 1.70, col_w - 0.40, 0.012, RGBColor(0x3c, 0x24, 0x12))

        # Keywords (11.5 pt light gray, left-aligned)
        tb_keys = s.shapes.add_textbox(Inches(col_x + 0.12), Inches(col_y + 1.85), Inches(col_w - 0.24), Inches(1.30))
        tf_keys = tb_keys.text_frame
        tf_keys.word_wrap = True
        tf_keys.margin_top = Inches(0)
        tf_keys.margin_bottom = Inches(0)
        tf_keys.margin_left = Inches(0)
        tf_keys.margin_right = Inches(0)
        
        for idx, key in enumerate(keywords):
            p_key = tf_keys.paragraphs[0] if idx == 0 else tf_keys.add_paragraph()
            r_key = p_key.add_run()
            r_key.text = f"•  {key}"
            r_key.font.size = Pt(11.5)
            r_key.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
            r_key.font.name = FONT
    # Left comparison text
    tb_left = s.shapes.add_textbox(Inches(0.85), Inches(5.75), Inches(5.40), Inches(1.10))
    tf_left = tb_left.text_frame
    tf_left.word_wrap = True
    tf_left.margin_top = Inches(0)
    tf_left.margin_bottom = Inches(0)
    tf_left.margin_left = Inches(0)
    tf_left.margin_right = Inches(0)
    
    p_left_hdr = tf_left.paragraphs[0]
    r_left_hdr = p_left_hdr.add_run()
    r_left_hdr.text = "Traditional Research"
    r_left_hdr.font.size = Pt(14)
    r_left_hdr.font.bold = True
    r_left_hdr.font.color.rgb = LGRAY
    r_left_hdr.font.name = FONT
    
    left_points = [
        "✗  Multiple Platforms",
        "✗  Manual Analysis",
        "✗  Information Overload"
    ]
    for pt in left_points:
        p_pt = tf_left.add_paragraph()
        r_pt = p_pt.add_run()
        r_pt.text = pt
        r_pt.font.size = Pt(11.5)
        r_pt.font.color.rgb = LGRAY
        r_pt.font.name = FONT

    # Center separator line
    box(s, 6.66, 5.65, 0.012, 1.20, BORDER2)

    # Right comparison text
    tb_right = s.shapes.add_textbox(Inches(6.85), Inches(5.75), Inches(5.40), Inches(1.10))
    tf_right = tb_right.text_frame
    tf_right.word_wrap = True
    tf_right.margin_top = Inches(0)
    tf_right.margin_bottom = Inches(0)
    tf_right.margin_left = Inches(0)
    tf_right.margin_right = Inches(0)
    
    p_right_hdr = tf_right.paragraphs[0]
    r_right_hdr = p_right_hdr.add_run()
    r_right_hdr.text = "Quantum Intelligence"
    r_right_hdr.font.size = Pt(14)
    r_right_hdr.font.bold = True
    r_right_hdr.font.color.rgb = ORANGE
    r_right_hdr.font.name = FONT
    
    right_points = [
        "✓  Unified Research",
        "✓  Automated Intelligence",
        "✓  Explainable Recommendations"
    ]
    for pt in right_points:
        p_pt = tf_right.add_paragraph()
        r_pt = p_pt.add_run()
        r_pt.text = pt
        r_pt.font.size = Pt(11.5)
        r_pt.font.bold = True
        r_pt.font.color.rgb = WHITE
        r_pt.font.name = FONT

    slide_number(s, 4)
    return s


# ═══════════════════════════════════════════════════════════════════
#  SLIDE 05 — Technical Architecture & Intelligence Flow
# ═══════════════════════════════════════════════════════════════════
def slide_05(prs):
    # Set background color to #050505 (Bloomberg Terminal style pitch black)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, SW, SH)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x05, 0x05, 0x05)
    bg.line.fill.background()

    # Top border highlight - premium orange (#FF8C42)
    ORANGE = RGBColor(0xFF, 0x8C, 0x42)
    box(s, 0, 0, 13.33, 0.06, ORANGE)

    # Title (reduced size by 15% to 34 pt)
    tb(s, "TECHNICAL ARCHITECTURE & INTELLIGENCE FLOW", 0.55, 0.35, 12.2, 0.65, size=34, bold=True, color=WHITE)

    # Subtitle (20 pt) with orange highlights
    tb_sub = s.shapes.add_textbox(Inches(0.55), Inches(1.05), Inches(12.2), Inches(0.50))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_top = Inches(0)
    tf_sub.margin_bottom = Inches(0)
    tf_sub.margin_left = Inches(0)
    tf_sub.margin_right = Inches(0)
    p_sub = tf_sub.paragraphs[0]
    
    r_sub1 = p_sub.add_run()
    r_sub1.text = "Institutional-grade "
    r_sub1.font.size = Pt(20)
    r_sub1.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_sub1.font.name = FONT
    r_sub1.font.italic = True
    
    r_sub2 = p_sub.add_run()
    r_sub2.text = "multi-agent research architecture"
    r_sub2.font.size = Pt(20)
    r_sub2.font.bold = True
    r_sub2.font.color.rgb = ORANGE
    r_sub2.font.name = FONT
    r_sub2.font.italic = True

    r_sub3 = p_sub.add_run()
    r_sub3.text = " powering Quantum Financial Intelligence Agent."
    r_sub3.font.size = Pt(20)
    r_sub3.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_sub3.font.name = FONT
    r_sub3.font.italic = True

    # Main content zone
    col_y = 1.67
    card_bg = RGBColor(0x11, 0x11, 0x11)

    # LEFT Title: QUANTUM MULTI-AGENT INTELLIGENCE ARCHITECTURE
    tb(s, "QUANTUM MULTI-AGENT INTELLIGENCE ARCHITECTURE", 0.55, 1.40, 8.00, 0.22, size=11.5, bold=True, color=ORANGE)

    # LEFT: Full Architecture Diagram (Dominant Visual, 70% width, dark-themed)
    # Framed in a premium container
    box(s, 0.55, col_y, 8.00, 2.85, card_bg, ORANGE, Pt(1.5))
    
    # Use the dark-themed image generated by our Pillow script
    arch_dark_path = os.path.join(BRAIN, "quantum_arch_dark.png")
    img(s, arch_dark_path, 0.65, 1.75, 7.80, 2.69, "[ Technical Architecture Diagram ]")

    # KEY DIFFERENTIATOR CALLOUT (Below architecture diagram - height increased by 30-40% to 1.20)
    box(s, 0.55, 4.62, 8.00, 1.20, card_bg, ORANGE, Pt(1.5))
    box(s, 0.55, 4.62, 0.05, 1.20, ORANGE)
    
    tb(s, "KEY DIFFERENTIATOR", 0.70, 4.67, 7.70, 0.24, size=13, bold=True, color=ORANGE)
    
    tb_diff = s.shapes.add_textbox(Inches(0.70), Inches(4.97), Inches(7.70), Inches(0.75))
    tf_diff = tb_diff.text_frame
    tf_diff.word_wrap = True
    tf_diff.margin_top = Inches(0)
    tf_diff.margin_bottom = Inches(0)
    tf_diff.margin_left = Inches(0)
    tf_diff.margin_right = Inches(0)
    p_diff = tf_diff.paragraphs[0]
    
    runs_data = [
        ("Unlike traditional AI assistants, Quantum combines ", False),
        ("Technical, Fundamental and Sentiment Agents", True),
        (" through a ", False),
        ("Consensus Engine", True),
        (" before generating investment recommendations.", False)
    ]
    for text, highlight in runs_data:
        r = p_diff.add_run()
        r.text = text
        r.font.size = Pt(11.5)
        r.font.name = FONT
        if highlight:
            r.font.bold = True
            r.font.color.rgb = ORANGE
        else:
            r.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)

    # RIGHT: Five Architecture Pillars (30% width, stacked with wide spacing, larger titles, reduced density)
    pillars = [
        ("🗄️", "DATA LAYER", "Yahoo Finance  •  Google News RSS"),
        ("🔄", "RESEARCH PIPELINE", "Technical Indicators  •  Market Context  •  Validation"),
        ("🧠", "AI INTELLIGENCE", "Technical Agent  •  Fundamental Agent  •  Sentiment Agent"),
        ("⚖️", "CONSENSUS ENGINE", "Direction  •  Confidence  •  Risk"),
        ("📑", "RESEARCH DELIVERY", "Institutional Dashboard  •  Investment Dossier  •  Exportable Reports")
    ]

    for idx, (icon, title, details) in enumerate(pillars):
        py = col_y + idx * 0.83  # Spacing increased from 0.77 to 0.83
        box(s, 8.85, py, 3.93, 0.72, card_bg, RGBColor(0x28, 0x28, 0x28), Pt(0.75))
        box(s, 8.85, py, 0.05, 0.72, ORANGE)
        
        # Pillar Title with Icon (slightly larger title: 13 pt)
        tb_p_title = s.shapes.add_textbox(Inches(9.02), Inches(py + 0.10), Inches(3.65), Inches(0.26))
        tf_p_title = tb_p_title.text_frame
        tf_p_title.word_wrap = True
        tf_p_title.margin_top = Inches(0)
        tf_p_title.margin_bottom = Inches(0)
        tf_p_title.margin_left = Inches(0)
        tf_p_title.margin_right = Inches(0)
        p_p_title = tf_p_title.paragraphs[0]
        
        r_icon = p_p_title.add_run()
        r_icon.text = f"{icon}  "
        r_icon.font.size = Pt(14)
        r_icon.font.bold = True
        r_icon.font.color.rgb = ORANGE
        r_icon.font.name = FONT
        
        r_title = p_p_title.add_run()
        r_title.text = title
        r_title.font.size = Pt(13)
        r_title.font.bold = True
        r_title.font.color.rgb = WHITE
        r_title.font.name = FONT

        # Pillar Details (size 9.5 pt, single line dot lists)
        tb_p_det = s.shapes.add_textbox(Inches(9.02), Inches(py + 0.38), Inches(3.65), Inches(0.24))
        tf_p_det = tb_p_det.text_frame
        tf_p_det.word_wrap = True
        tf_p_det.margin_top = Inches(0)
        tf_p_det.margin_bottom = Inches(0)
        tf_p_det.margin_left = Inches(0)
        tf_p_det.margin_right = Inches(0)
        p_p_det = tf_p_det.paragraphs[0]
        r_p_det = p_p_det.add_run()
        r_p_det.text = details
        r_p_det.font.size = Pt(9.5)
        r_p_det.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
        r_p_det.font.name = FONT

    # BOTTOM: Three Architecture Benefits Cards (Scan-friendly bullet checkmarks)
    benefits = [
        ("EXPLAINABLE INTELLIGENCE", ["✓  Agent Outputs", "✓  Confidence Scores", "✓  Traceable Decisions"]),
        ("MULTI-AGENT VALIDATION", ["✓  Technical Agent", "✓  Fundamental Agent", "✓  Sentiment Agent"]),
        ("PRODUCTION-READY ARCHITECTURE", ["✓  Validation Layer", "✓  Cache Layer", "✓  Fallback Logic"])
    ]
    card_w = 3.85
    card_h = 1.10
    card_y = 5.95
    for idx, (title, bullets) in enumerate(benefits):
        cx = 0.55 + idx * 4.19
        box(s, cx, card_y, card_w, card_h, card_bg, RGBColor(0x28, 0x28, 0x28), Pt(0.75))
        box(s, cx, card_y, 0.05, card_h, ORANGE)
        
        # Benefit Content inside a single text box
        tb_b = s.shapes.add_textbox(Inches(cx + 0.15), Inches(card_y + 0.08), Inches(card_w - 0.25), Inches(0.95))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_top = Inches(0)
        tf_b.margin_bottom = Inches(0)
        tf_b.margin_left = Inches(0)
        tf_b.margin_right = Inches(0)
        
        # Title paragraph
        p_b_title = tf_b.paragraphs[0]
        r_b_title = p_b_title.add_run()
        r_b_title.text = title
        r_b_title.font.size = Pt(13)
        r_b_title.font.bold = True
        r_b_title.font.color.rgb = ORANGE
        r_b_title.font.name = FONT
        
        # Bullet list paragraphs
        for b_text in bullets:
            p_bullet = tf_b.add_paragraph()
            r_bullet = p_bullet.add_run()
            r_bullet.text = b_text
            r_bullet.font.size = Pt(11)
            r_bullet.font.bold = True
            r_bullet.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
            r_bullet.font.name = FONT

    slide_number(s, 5)
    return s


# ═══════════════════════════════════════════════════════════════════
#  SLIDE 06 — APPROACH & METHODOLOGY  (NEW)
# ═══════════════════════════════════════════════════════════════════
def slide_06(prs):
    # Set background color to #050505 (Bloomberg Terminal style pitch black)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, SW, SH)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x05, 0x05, 0x05)
    bg.line.fill.background()

    # Top border highlight - premium orange (#FF8C42)
    ORANGE = RGBColor(0xFF, 0x8C, 0x42)
    box(s, 0, 0, 13.33, 0.06, ORANGE)

    # Title (34 pt)
    tb(s, "APPROACH & METHODOLOGY", 0.55, 0.35, 12.2, 0.65, size=34, bold=True, color=WHITE)

    # Subtitle (20 pt) with orange highlights
    tb_sub = s.shapes.add_textbox(Inches(0.55), Inches(1.05), Inches(12.2), Inches(0.50))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_top = Inches(0)
    tf_sub.margin_bottom = Inches(0)
    tf_sub.margin_left = Inches(0)
    tf_sub.margin_right = Inches(0)
    p_sub = tf_sub.paragraphs[0]
    
    r_sub1 = p_sub.add_run()
    r_sub1.text = "From Market Noise to "
    r_sub1.font.size = Pt(20)
    r_sub1.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_sub1.font.name = FONT
    r_sub1.font.italic = True
    
    r_sub2 = p_sub.add_run()
    r_sub2.text = "Actionable Intelligence"
    r_sub2.font.size = Pt(20)
    r_sub2.font.bold = True
    r_sub2.font.color.rgb = ORANGE
    r_sub2.font.name = FONT
    r_sub2.font.italic = True

    # SECTION 1 — METHODOLOGY JOURNEY
    # 4 horizontal cards
    cards = [
        ("DISCOVER", 
         ["Retail investors use multiple platforms", "Research signals are fragmented", "No explainable decision support"],
         "IDENTIFY"),
        ("DESIGN", 
         ["Evaluated multiple AI architectures", "Selected specialized agents", "Defined consensus mechanism"],
         "DESIGN"),
        ("DEVELOP", 
         ["Built FastAPI orchestration layer", "Integrated financial data sources", "Implemented multi-agent workflow"],
         "BUILD"),
        ("DELIVER", 
         ["Research Dashboard", "PDF Dossier", "Investment Recommendation Engine"],
         "DELIVER")
    ]

    card_w = 2.85
    card_h = 2.10
    card_y = 1.35
    card_bg = RGBColor(0x11, 0x11, 0x11)
    
    # Process stage connection arrows
    for ax in [3.44, 6.56, 9.68]:
        ashp = s.shapes.add_shape(33, Inches(ax), Inches(2.10), Inches(0.20), Inches(0.20))
        ashp.fill.solid()
        ashp.fill.fore_color.rgb = ORANGE
        ashp.line.fill.background()

    for idx, (title, bullets, badge) in enumerate(cards):
        cx = 0.55 + idx * 3.12  # 2.85 width + 0.27 gap
        # Card base box (#111111 background, #282828 border)
        box(s, cx, card_y, card_w, card_h, card_bg, RGBColor(0x28, 0x28, 0x28), Pt(0.75))
        # Orange top accent line
        box(s, cx, card_y, card_w, 0.05, ORANGE)
        
        # Title
        tb(s, title, cx + 0.12, card_y + 0.12, card_w - 0.24, 0.30, size=12.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        # Accent line under title
        box(s, cx + 0.50, card_y + 0.42, card_w - 1.00, 0.012, ORANGE)
        
        # Bullet list text box
        tb_b = s.shapes.add_textbox(Inches(cx + 0.12), Inches(card_y + 0.48), Inches(card_w - 0.24), Inches(1.10))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_top = Inches(0)
        tf_b.margin_bottom = Inches(0)
        tf_b.margin_left = Inches(0)
        tf_b.margin_right = Inches(0)
        
        first = True
        for bullet in bullets:
            p = tf_b.paragraphs[0] if first else tf_b.add_paragraph()
            first = False
            r = p.add_run()
            r.text = f"•  {bullet}"
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
            r.font.name = FONT
            
        # Outcome badge at the bottom (Solid orange badge centered)
        box(s, cx + 0.625, card_y + 1.68, 1.60, 0.32, ORANGE)
        tb(s, badge, cx + 0.625, card_y + 1.74, 1.60, 0.26, size=9.5, bold=True, color=RGBColor(0x05, 0x05, 0x05), align=PP_ALIGN.CENTER)

    # SECTION 2 — WHY MULTI-AGENT AI
    # Left Card (Traditional Single LLM)
    box(s, 0.55, 3.65, 5.70, 1.85, card_bg, RGBColor(0x28, 0x28, 0x28), Pt(0.75))
    box(s, 0.55, 3.65, 0.05, 1.85, RGBColor(0x9c, 0xa3, 0xaf))
    tb(s, "Traditional Single LLM", 0.75, 3.75, 5.30, 0.30, size=13, bold=True, color=RGBColor(0x9c, 0xa3, 0xaf))
    
    # Left Card - Column 1
    tb_l_col1 = s.shapes.add_textbox(Inches(0.75), Inches(4.15), Inches(2.45), Inches(1.10))
    tf_l_col1 = tb_l_col1.text_frame
    tf_l_col1.word_wrap = True
    tf_l_col1.margin_top = Inches(0)
    tf_l_col1.margin_bottom = Inches(0)
    tf_l_col1.margin_left = Inches(0)
    tf_l_col1.margin_right = Inches(0)
    
    l_bullets_1 = [
        "❌  One reasoning source",
        "❌  Mixed signal interpretation"
    ]
    for idx, b_text in enumerate(l_bullets_1):
        p = tf_l_col1.paragraphs[0] if idx == 0 else tf_l_col1.add_paragraph()
        r = p.add_run()
        r.text = b_text
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(0x9c, 0xa3, 0xaf)
        r.font.name = FONT

    # Left Card - Column 2
    tb_l_col2 = s.shapes.add_textbox(Inches(3.40), Inches(4.15), Inches(2.45), Inches(1.10))
    tf_l_col2 = tb_l_col2.text_frame
    tf_l_col2.word_wrap = True
    tf_l_col2.margin_top = Inches(0)
    tf_l_col2.margin_bottom = Inches(0)
    tf_l_col2.margin_left = Inches(0)
    tf_l_col2.margin_right = Inches(0)
    
    l_bullets_2 = [
        "❌  Limited transparency",
        "❌  Single-point decision output"
    ]
    for idx, b_text in enumerate(l_bullets_2):
        p = tf_l_col2.paragraphs[0] if idx == 0 else tf_l_col2.add_paragraph()
        r = p.add_run()
        r.text = b_text
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(0x9c, 0xa3, 0xaf)
        r.font.name = FONT

    # Center VS badge
    box(s, 6.40, 4.35, 0.45, 0.45, card_bg, ORANGE, Pt(1.2))
    tb(s, "VS", 6.40, 4.43, 0.45, 0.30, size=11, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

    # Right Card (Quantum Multi-Agent Architecture)
    box(s, 6.95, 3.65, 5.83, 1.85, card_bg, ORANGE, Pt(1.5))
    box(s, 6.95, 3.65, 0.05, 1.85, ORANGE)
    tb(s, "Quantum Multi-Agent Architecture", 7.15, 3.75, 5.40, 0.30, size=13, bold=True, color=ORANGE)
    
    # Right Card - Column 1
    tb_r_col1 = s.shapes.add_textbox(Inches(7.15), Inches(4.15), Inches(2.60), Inches(1.10))
    tf_r_col1 = tb_r_col1.text_frame
    tf_r_col1.word_wrap = True
    tf_r_col1.margin_top = Inches(0)
    tf_r_col1.margin_bottom = Inches(0)
    tf_r_col1.margin_left = Inches(0)
    tf_r_col1.margin_right = Inches(0)
    
    r_bullets_1 = [
        "✅  Technical Agent",
        "✅  Fundamental Agent",
        "✅  Sentiment Agent"
    ]
    for idx, b_text in enumerate(r_bullets_1):
        p = tf_r_col1.paragraphs[0] if idx == 0 else tf_r_col1.add_paragraph()
        r = p.add_run()
        r.text = b_text
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = WHITE
        r.font.name = FONT

    # Right Card - Column 2
    tb_r_col2 = s.shapes.add_textbox(Inches(9.95), Inches(4.15), Inches(2.60), Inches(1.10))
    tf_r_col2 = tb_r_col2.text_frame
    tf_r_col2.word_wrap = True
    tf_r_col2.margin_top = Inches(0)
    tf_r_col2.margin_bottom = Inches(0)
    tf_r_col2.margin_left = Inches(0)
    tf_r_col2.margin_right = Inches(0)
    
    r_bullets_2 = [
        "✅  Consensus Engine",
        "✅  Traceable Decisions"
    ]
    for idx, b_text in enumerate(r_bullets_2):
        p = tf_r_col2.paragraphs[0] if idx == 0 else tf_r_col2.add_paragraph()
        r = p.add_run()
        r.text = b_text
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = WHITE
        r.font.name = FONT

    # SECTION 3 — KEY DECISION CALLOUT
    box(s, 0.55, 5.68, 12.23, 1.25, card_bg, ORANGE, Pt(1.2))
    box(s, 0.55, 5.68, 0.05, 1.25, ORANGE)
    
    # Overlapping orange tab on top-left of the callout
    box(s, 0.75, 5.53, 2.50, 0.28, ORANGE)
    tb(s, "WHY WE CHOSE MULTI-AGENT AI", 0.75, 5.59, 2.50, 0.22, size=9, bold=True, color=RGBColor(0x05, 0x05, 0x05), align=PP_ALIGN.CENTER)
    
    # Summary body text
    tb_ins = s.shapes.add_textbox(Inches(0.75), Inches(5.92), Inches(11.83), Inches(0.85))
    tf_ins = tb_ins.text_frame
    tf_ins.word_wrap = True
    tf_ins.margin_top = Inches(0)
    tf_ins.margin_bottom = Inches(0)
    tf_ins.margin_left = Inches(0)
    tf_ins.margin_right = Inches(0)
    p_ins = tf_ins.paragraphs[0]
    
    r_ins = p_ins.add_run()
    r_ins.text = (
        "Instead of relying on one general-purpose model, Quantum distributes financial reasoning "
        "across specialized agents and combines their outputs through a consensus engine, resulting "
        "in more reliable, explainable, and institution-grade investment intelligence."
    )
    r_ins.font.size = Pt(11.5)
    r_ins.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_ins.font.name = FONT

    slide_number(s, 6)
    return s


# ═══════════════════════════════════════════════════════════════════
#  SLIDE 07 — SOLUTION DEMONSTRATION  (NEW)
# ═══════════════════════════════════════════════════════════════════
def slide_07(prs):
    # Set background color to #050505 (Bloomberg Terminal style pitch black)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, SW, SH)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x05, 0x05, 0x05)
    bg.line.fill.background()

    # Top border highlight - premium orange (#FF8C42)
    ORANGE = RGBColor(0xFF, 0x8C, 0x42)
    box(s, 0, 0, 13.33, 0.06, ORANGE)

    # Title (34 pt)
    tb(s, "SOLUTION DEMONSTRATION", 0.55, 0.35, 12.2, 0.65, size=34, bold=True, color=WHITE)

    # Subtitle (20 pt) with orange highlights
    tb_sub = s.shapes.add_textbox(Inches(0.55), Inches(1.05), Inches(12.2), Inches(0.50))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_top = Inches(0)
    tf_sub.margin_bottom = Inches(0)
    tf_sub.margin_left = Inches(0)
    tf_sub.margin_right = Inches(0)
    p_sub = tf_sub.paragraphs[0]
    
    r_sub1 = p_sub.add_run()
    r_sub1.text = "From Stock Search to "
    r_sub1.font.size = Pt(20)
    r_sub1.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_sub1.font.name = FONT
    r_sub1.font.italic = True
    
    r_sub2 = p_sub.add_run()
    r_sub2.text = "Institutional-Grade Investment Intelligence"
    r_sub2.font.size = Pt(20)
    r_sub2.font.bold = True
    r_sub2.font.color.rgb = ORANGE
    r_sub2.font.name = FONT
    r_sub2.font.italic = True

    r_sub3 = p_sub.add_run()
    r_sub3.text = " in Seconds"
    r_sub3.font.size = Pt(20)
    r_sub3.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_sub3.font.name = FONT
    r_sub3.font.italic = True

    # Main content zone coordinates
    card_bg = RGBColor(0x11, 0x11, 0x11)
    card_w = 2.80
    card_h = 3.60
    card_y = 1.95

    # Process step labels and titles
    labels = ["INPUT", "ANALYSIS", "CONSENSUS", "REPORT"]
    titles = ["Stock Discovery", "Multi-Agent Analysis", "Consensus Intelligence", "Research Delivery"]
    
    # Screenshot file paths from frontend images directory
    img_paths = [
        r"C:\Users\singh\QUANTAM-AI-RESEARCH-AGENT\frontend\images\Search page.jpeg",
        r"C:\Users\singh\QUANTAM-AI-RESEARCH-AGENT\frontend\images\landing page.jpeg",
        r"C:\Users\singh\QUANTAM-AI-RESEARCH-AGENT\frontend\images\research page.jpeg",
        r"C:\Users\singh\QUANTAM-AI-RESEARCH-AGENT\frontend\images\research page.jpeg"
    ]

    # Process connection arrows
    for ax in [3.42, 6.56, 9.70]:
        ashp = s.shapes.add_shape(33, Inches(ax), Inches(2.70), Inches(0.20), Inches(0.20))
        ashp.fill.solid()
        ashp.fill.fore_color.rgb = ORANGE
        ashp.line.fill.background()

    # Steps Loop
    for idx in range(4):
        cx = 0.55 + idx * 3.14  # 2.80 width + 0.34 gap
        
        # Subtle label above step
        tb(s, labels[idx], cx, 1.35, card_w, 0.22, size=9.5, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
        
        # Step title above card
        tb(s, titles[idx], cx, 1.60, card_w, 0.30, size=12.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        
        # Step card container box (#111111 background, #282828 border)
        box(s, cx, card_y, card_w, card_h, card_bg, RGBColor(0x28, 0x28, 0x28), Pt(0.75))
        
        # Screenshot placeholder with orange border accent
        box(s, cx + 0.05, card_y + 0.05, 2.70, 1.65, card_bg, ORANGE, Pt(0.5))
        img(s, img_paths[idx], cx + 0.05, card_y + 0.05, 2.70, 1.65, f"[ Screenshot {idx+1} ]")

        # Details section inside card under screenshot
        if idx == 0:
            # Step 1 details
            tb(s, "Investor enters stock symbol\n(AAPL, NVDA, INFY, TSLA)", cx + 0.10, card_y + 1.85, card_w - 0.20, 0.60, size=9.5, color=LGRAY, align=PP_ALIGN.CENTER)
            
            # Bottom badge
            box(s, cx + 0.50, card_y + 3.00, 1.80, 0.32, ORANGE)
            tb(s, "INPUT", cx + 0.50, card_y + 3.06, 1.80, 0.26, size=9.5, bold=True, color=RGBColor(0x05, 0x05, 0x05), align=PP_ALIGN.CENTER)
            
        elif idx == 1:
            # Step 2 details: 3 agent tags
            agents = ["📉  Technical Agent", "🏢  Fundamental Agent", "🧠  Sentiment Agent"]
            for a_idx, agent in enumerate(agents):
                ay = card_y + 1.80 + a_idx * 0.38
                box(s, cx + 0.15, ay, 2.50, 0.28, RGBColor(0x16, 0x16, 0x16), RGBColor(0x28, 0x28, 0x28), Pt(0.5))
                tb(s, agent, cx + 0.20, ay + 0.04, 2.40, 0.22, size=8.5, bold=True, color=WHITE)
                
            # Bottom badge
            box(s, cx + 0.50, card_y + 3.00, 1.80, 0.32, ORANGE)
            tb(s, "AI PROCESSING", cx + 0.50, card_y + 3.06, 1.80, 0.26, size=9.5, bold=True, color=RGBColor(0x05, 0x05, 0x05), align=PP_ALIGN.CENTER)
            
        elif idx == 2:
            # Step 3 details: 3 metrics tags
            metrics = [("Bias: BULLISH / BEARISH", ORANGE), ("Confidence: 85% Conviction", ORANGE), ("Risk Level: Low / Medium", ORANGE)]
            for m_idx, (metric_text, m_color) in enumerate(metrics):
                my = card_y + 1.80 + m_idx * 0.38
                box(s, cx + 0.15, my, 2.50, 0.28, RGBColor(0x16, 0x16, 0x16), RGBColor(0x28, 0x28, 0x28), Pt(0.5))
                tb(s, metric_text, cx + 0.20, my + 0.04, 2.40, 0.22, size=8.5, bold=True, color=WHITE)
                
            # Bottom badge
            box(s, cx + 0.50, card_y + 3.00, 1.80, 0.32, ORANGE)
            tb(s, "DECISION ENGINE", cx + 0.50, card_y + 3.06, 1.80, 0.26, size=9.5, bold=True, color=RGBColor(0x05, 0x05, 0x05), align=PP_ALIGN.CENTER)
            
        elif idx == 3:
            # Step 4 details: output chips
            tb(s, "Executive Thesis  •  Bull vs Bear", cx + 0.10, card_y + 1.80, card_w - 0.20, 0.25, size=8.5, color=LGRAY, align=PP_ALIGN.CENTER)
            tb(s, "Risk Register  •  Catalyst Calendar", cx + 0.10, card_y + 2.15, card_w - 0.20, 0.25, size=8.5, color=LGRAY, align=PP_ALIGN.CENTER)
            tb(s, "Investment Decision Box", cx + 0.10, card_y + 2.50, card_w - 0.20, 0.25, size=8.5, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
            
            # Bottom badge
            box(s, cx + 0.50, card_y + 3.00, 1.80, 0.32, ORANGE)
            tb(s, "OUTPUT", cx + 0.50, card_y + 3.06, 1.80, 0.26, size=9.5, bold=True, color=RGBColor(0x05, 0x05, 0x05), align=PP_ALIGN.CENTER)

    # BOTTOM HIGHLIGHT BAR
    box(s, 0.55, 5.68, 12.23, 1.25, card_bg, ORANGE, Pt(1.2))
    box(s, 0.55, 5.68, 0.05, 1.25, ORANGE)
    
    # Overlapping orange tab on top-left of the callout
    box(s, 0.75, 5.53, 3.80, 0.28, ORANGE)
    tb(s, "END-TO-END AUTOMATED RESEARCH PIPELINE", 0.75, 5.59, 3.80, 0.22, size=9, bold=True, color=RGBColor(0x05, 0x05, 0x05), align=PP_ALIGN.CENTER)
    
    # Summary body text
    tb_ins = s.shapes.add_textbox(Inches(0.75), Inches(5.92), Inches(11.83), Inches(0.85))
    tf_ins = tb_ins.text_frame
    tf_ins.word_wrap = True
    tf_ins.margin_top = Inches(0)
    tf_ins.margin_bottom = Inches(0)
    tf_ins.margin_left = Inches(0)
    tf_ins.margin_right = Inches(0)
    p_ins = tf_ins.paragraphs[0]
    
    r_ins = p_ins.add_run()
    r_ins.text = (
        "Quantum transforms fragmented market information into explainable institutional-grade "
        "investment intelligence through specialized AI agents and consensus-based reasoning."
    )
    r_ins.font.size = Pt(11.5)
    r_ins.font.color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
    r_ins.font.name = FONT

    slide_number(s, 7)
    return s


# ═══════════════════════════════════════════════════════════════════
#  SLIDE 08 — TECHNICAL ARCHITECTURE & CODE FLOW  (PREMIUM REDESIGN)
# ═══════════════════════════════════════════════════════════════════
def slide_08(prs):
    # Black background
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, SW, SH)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x05, 0x05, 0x05)
    bg.line.fill.background()

    ORANGE = RGBColor(0xFF, 0x8C, 0x42)
    C_BG   = RGBColor(0x11, 0x11, 0x11)
    C_BG2  = RGBColor(0x16, 0x16, 0x16)
    DIM    = RGBColor(0x28, 0x28, 0x28)
    LG     = RGBColor(0x9c, 0xa3, 0xaf)
    BLACK  = RGBColor(0x05, 0x05, 0x05)

    # Top orange stripe
    box(s, 0, 0, 13.33, 0.06, ORANGE)

    # ── TITLE ─────────────────────────────────────────────────────
    tb(s, "TECHNICAL ARCHITECTURE & CODE FLOW",
       0.55, 0.10, 12.2, 0.44, size=28, bold=True, color=WHITE)

    # Subtitle
    tb_sub = s.shapes.add_textbox(Inches(0.55), Inches(0.57), Inches(12.2), Inches(0.26))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_top = Inches(0); tf_sub.margin_bottom = Inches(0)
    tf_sub.margin_left = Inches(0); tf_sub.margin_right = Inches(0)
    p_sub = tf_sub.paragraphs[0]
    r_s1 = p_sub.add_run()
    r_s1.text = "How a single stock query travels through the "
    r_s1.font.size = Pt(12); r_s1.font.color.rgb = LG
    r_s1.font.name = FONT; r_s1.font.italic = True
    r_s2 = p_sub.add_run()
    r_s2.text = "Quantum Intelligence Engine."
    r_s2.font.size = Pt(12); r_s2.font.bold = True
    r_s2.font.color.rgb = ORANGE; r_s2.font.name = FONT; r_s2.font.italic = True

    # ── SIDE PANELS ───────────────────────────────────────────────
    panel_y = 1.00
    panel_h = 4.40   # ends y=5.40

    # Left panel: DATA SOURCES
    lp_x, lp_w = 0.10, 1.52
    box(s, lp_x, panel_y, lp_w, panel_h, C_BG, DIM, Pt(0.75))
    box(s, lp_x, panel_y, 0.05, panel_h, ORANGE)
    tb(s, "DATA\nSOURCES", lp_x+0.12, panel_y+0.10, lp_w-0.17, 0.46,
       size=9.5, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    ds_items = [
        ("\U0001f4c8", "Yahoo Finance"),
        ("\U0001f4f0", "Google News RSS"),
        ("\U0001f4ca", "Tech Indicators"),
        ("\U0001f310", "Market Context"),
    ]
    for i, (ico, lbl) in enumerate(ds_items):
        dy = panel_y + 0.65 + i * 0.93
        box(s, lp_x+0.10, dy, lp_w-0.20, 0.80, C_BG2, DIM, Pt(0.5))
        tb(s, ico,  lp_x+0.10, dy+0.05, lp_w-0.20, 0.38,
           size=20, color=WHITE, align=PP_ALIGN.CENTER)
        tb(s, lbl,  lp_x+0.10, dy+0.50, lp_w-0.20, 0.26,
           size=7.5, bold=True, color=LG, align=PP_ALIGN.CENTER)

    # Right panel: RELIABILITY LAYER
    rp_x, rp_w = 11.71, 1.52
    box(s, rp_x, panel_y, rp_w, panel_h, C_BG, DIM, Pt(0.75))
    box(s, rp_x, panel_y, 0.05, panel_h, ORANGE)
    tb(s, "RELIABILITY\nLAYER", rp_x+0.12, panel_y+0.10, rp_w-0.17, 0.46,
       size=9.5, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    rl_items = [
        ("\U0001f504", "Redis Cache"),
        ("\u2705",       "Req. Validation"),
        ("\U0001f6e1\ufe0f", "Fallback Logic"),
        ("\u26a0\ufe0f",   "Error Handling"),
        ("\U0001f512",  "Graceful Degrade"),
    ]
    for i, (ico, lbl) in enumerate(rl_items):
        ry = panel_y + 0.65 + i * 0.74
        box(s, rp_x+0.10, ry, rp_w-0.20, 0.62, C_BG2, DIM, Pt(0.5))
        tb(s, f"{ico}  {lbl}", rp_x+0.12, ry+0.18, rp_w-0.22, 0.26,
           size=7.5, bold=True, color=LG, align=PP_ALIGN.CENTER)

    # ── CENTER ARCHITECTURE ZONE ──────────────────────────────────
    arc_x  = 1.70           # left edge of centre zone
    arc_w  = 9.93           # width  (→ 11.63)
    arc_cx = arc_x + arc_w / 2   # 6.665 (slide centre)

    def vcr(cx, y_top, y_bot):
        box(s, cx - 0.016, y_top, 0.032, y_bot - y_top, ORANGE)

    def hcr(x_l, y, x_r):
        box(s, x_l, y, x_r - x_l, 0.025, ORANGE)

    # ── ROW 1: ENTRY PIPELINE  (y=1.02, h=0.56) ──────────────────
    r1_y, r1_h = 1.02, 0.56
    box(s, arc_x, r1_y, arc_w, r1_h, C_BG, DIM, Pt(0.75))
    box(s, arc_x, r1_y, 0.05, r1_h, ORANGE)
    tb(s, "ENTRY PIPELINE", arc_x+0.14, r1_y+0.06, 2.0, 0.22,
       size=9, bold=True, color=ORANGE)

    # 5 mini-chips inside the strip
    mnodes = [
        ("\U0001f464", "INVESTOR"),
        ("\U0001f50d", "SEARCH STOCK"),
        ("\U0001f5a5\ufe0f", "REACT + VITE"),
        ("\u26a1",    "FASTAPI GATEWAY"),
        ("\U0001f527", "CONTEXT BUILDER"),
    ]
    mn_w = 1.52; mn_arr = 0.13
    mn_total = len(mnodes) * mn_w + (len(mnodes) - 1) * mn_arr
    mn_xs = arc_x + (arc_w - mn_total) / 2
    mn_y  = r1_y + 0.20; mn_h = 0.26

    for m_i, (m_ico, m_lbl) in enumerate(mnodes):
        mx = mn_xs + m_i * (mn_w + mn_arr)
        box(s, mx, mn_y, mn_w, mn_h, C_BG2, ORANGE, Pt(0.5))
        tb_m = s.shapes.add_textbox(Inches(mx+0.04), Inches(mn_y+0.03),
                                    Inches(mn_w-0.08), Inches(mn_h-0.05))
        tf_m = tb_m.text_frame; tf_m.word_wrap = True
        tf_m.margin_top = Inches(0); tf_m.margin_bottom = Inches(0)
        tf_m.margin_left = Inches(0); tf_m.margin_right = Inches(0)
        p_m = tf_m.paragraphs[0]; p_m.alignment = PP_ALIGN.CENTER
        r_m = p_m.add_run()
        r_m.text = f"{m_ico}  {m_lbl}"
        r_m.font.size = Pt(8); r_m.font.bold = True
        r_m.font.color.rgb = WHITE; r_m.font.name = FONT
        if m_i < len(mnodes) - 1:
            ar = s.shapes.add_shape(33, Inches(mx+mn_w),
                                    Inches(mn_y+mn_h/2-0.05),
                                    Inches(mn_arr), Inches(0.10))
            ar.fill.solid()
            ar.fill.fore_color.rgb = ORANGE
            ar.line.fill.background()

    # ── ROW 2: THREE PARALLEL AGENTS  (y=1.74, h=1.34) ───────────
    r2_y, r2_h = 1.74, 1.34
    ag_w  = 3.08
    ag_gap = (arc_w - 3 * ag_w) / 2          # 0.345
    a_cx = [arc_x + i*(ag_w+ag_gap) + ag_w/2 for i in range(3)]
    # a_cx = [3.24, 6.665, 10.09]

    agents_info = [
        ("\U0001f4c9", "TECHNICAL AGENT",   "Weight: 40%",
         ["Price Action", "RSI / MACD", "Moving Averages", "Support & Resistance"],
         "Technical Signals"),
        ("\U0001f3e2", "FUNDAMENTAL AGENT", "Weight: 35%",
         ["Revenue Growth", "PE Ratio", "Profitability", "Financial Health"],
         "Fundamental Signals"),
        ("\U0001f9e0", "SENTIMENT AGENT",   "Weight: 25%",
         ["Google News RSS", "Financial Headlines", "Market Events"],
         "Sentiment Signals"),
    ]

    for a_i, (ico, title, weight, inputs, output) in enumerate(agents_info):
        ax = arc_x + a_i * (ag_w + ag_gap)
        box(s, ax, r2_y, ag_w, r2_h, C_BG, ORANGE, Pt(1.0))
        box(s, ax, r2_y, ag_w, 0.05, ORANGE)

        # Header: icon + title
        tb_ah = s.shapes.add_textbox(Inches(ax+0.10), Inches(r2_y+0.08),
                                     Inches(ag_w-0.20), Inches(0.28))
        tf_ah = tb_ah.text_frame; tf_ah.word_wrap = True
        tf_ah.margin_top = Inches(0); tf_ah.margin_bottom = Inches(0)
        tf_ah.margin_left = Inches(0); tf_ah.margin_right = Inches(0)
        p_ah = tf_ah.paragraphs[0]; p_ah.alignment = PP_ALIGN.CENTER
        r_ico = p_ah.add_run()
        r_ico.text = f"{ico}  "
        r_ico.font.size = Pt(14); r_ico.font.color.rgb = ORANGE; r_ico.font.name = FONT
        r_ttl = p_ah.add_run()
        r_ttl.text = title
        r_ttl.font.size = Pt(11); r_ttl.font.bold = True
        r_ttl.font.color.rgb = WHITE; r_ttl.font.name = FONT

        # Weight badge + divider
        tb(s, weight, ax+0.10, r2_y+0.38, ag_w-0.20, 0.20,
           size=9, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
        box(s, ax+0.15, r2_y+0.61, ag_w-0.30, 0.012, ORANGE)

        # Input bullets
        tb_inp = s.shapes.add_textbox(Inches(ax+0.14), Inches(r2_y+0.66),
                                      Inches(ag_w-0.28), Inches(0.50))
        tf_inp = tb_inp.text_frame; tf_inp.word_wrap = True
        tf_inp.margin_top = Inches(0); tf_inp.margin_bottom = Inches(0)
        tf_inp.margin_left = Inches(0); tf_inp.margin_right = Inches(0)
        first = True
        for inp in inputs:
            p_i = tf_inp.paragraphs[0] if first else tf_inp.add_paragraph()
            first = False
            r_i = p_i.add_run()
            r_i.text = f"\u25b8  {inp}"
            r_i.font.size = Pt(8.5); r_i.font.color.rgb = LG; r_i.font.name = FONT

        # Output badge
        box(s, ax+0.22, r2_y+r2_h-0.30, ag_w-0.44, 0.24, ORANGE)
        tb(s, output, ax+0.22, r2_y+r2_h-0.26, ag_w-0.44, 0.20,
           size=8.5, bold=True, color=BLACK, align=PP_ALIGN.CENTER)

    # Connectors: pipeline centre → branch bar → 3 agents
    r1_bot   = r1_y + r1_h      # 1.58
    branch_y = r1_bot + 0.08    # 1.66
    vcr(arc_cx, r1_bot, branch_y)
    hcr(a_cx[0], branch_y, a_cx[2])
    for cx2 in a_cx:
        vcr(cx2, branch_y, r2_y)

    # ── ROW 3: GROQ LLM  (y=3.22, h=0.54) ───────────────────────
    r3_y, r3_h = 3.22, 0.54
    r3_w = 4.20
    r3_x = arc_cx - r3_w / 2    # 4.565

    box(s, r3_x, r3_y, r3_w, r3_h, C_BG, ORANGE, Pt(1.5))
    box(s, r3_x, r3_y, r3_w, 0.05, ORANGE)

    tb_g = s.shapes.add_textbox(Inches(r3_x+0.10), Inches(r3_y+0.07),
                                Inches(r3_w-0.20), Inches(0.26))
    tf_g = tb_g.text_frame; tf_g.word_wrap = True
    tf_g.margin_top = Inches(0); tf_g.margin_bottom = Inches(0)
    tf_g.margin_left = Inches(0); tf_g.margin_right = Inches(0)
    p_g = tf_g.paragraphs[0]; p_g.alignment = PP_ALIGN.CENTER
    r_g = p_g.add_run()
    r_g.text = "\U0001f916  GROQ LLM  (Llama 3.3-70B)"
    r_g.font.size = Pt(12); r_g.font.bold = True
    r_g.font.color.rgb = WHITE; r_g.font.name = FONT
    tb(s, "Structured Prompting  \u2022  Reasoning Layer  \u2022  Sub-2s Inference",
       r3_x+0.10, r3_y+0.34, r3_w-0.20, 0.16,
       size=8, color=LG, align=PP_ALIGN.CENTER)

    # Convergence: 3 agent bottoms → horiz bar → Groq
    r2_bot = r2_y + r2_h        # 3.08
    conv_y = r2_bot + 0.07      # 3.15
    for cx2 in a_cx:
        vcr(cx2, r2_bot, conv_y)
    hcr(a_cx[0], conv_y, a_cx[2])
    vcr(arc_cx, conv_y, r3_y)

    # ── ROW 4: MASTER CONSENSUS ENGINE  (y=3.90, h=0.82) — LARGEST
    r4_y, r4_h = 3.90, 0.82
    r4_w = 5.60
    r4_x = arc_cx - r4_w / 2    # 3.865

    box(s, r4_x, r4_y, r4_w, r4_h, C_BG, ORANGE, Pt(2.0))
    box(s, r4_x, r4_y, r4_w, 0.06, ORANGE)

    tb_ce = s.shapes.add_textbox(Inches(r4_x+0.12), Inches(r4_y+0.08),
                                 Inches(r4_w-0.24), Inches(0.30))
    tf_ce = tb_ce.text_frame; tf_ce.word_wrap = True
    tf_ce.margin_top = Inches(0); tf_ce.margin_bottom = Inches(0)
    tf_ce.margin_left = Inches(0); tf_ce.margin_right = Inches(0)
    p_ce = tf_ce.paragraphs[0]; p_ce.alignment = PP_ALIGN.CENTER
    r_ce = p_ce.add_run()
    r_ce.text = "\u2696\ufe0f  MASTER CONSENSUS ENGINE"
    r_ce.font.size = Pt(14); r_ce.font.bold = True
    r_ce.font.color.rgb = ORANGE; r_ce.font.name = FONT

    # 3 metric chips
    chips = ["\u25c8  DIRECTION", "\u25c8  CONFIDENCE", "\u25c8  RISK LEVEL"]
    chip_w = 1.55; chip_h = 0.28; chip_gap = 0.12
    chip_total = len(chips) * chip_w + (len(chips) - 1) * chip_gap
    chip_sx = r4_x + (r4_w - chip_total) / 2
    chip_y  = r4_y + 0.43
    for c_i, chip in enumerate(chips):
        chip_x = chip_sx + c_i * (chip_w + chip_gap)
        box(s, chip_x, chip_y, chip_w, chip_h, ORANGE)
        tb(s, chip, chip_x+0.06, chip_y+0.04, chip_w-0.10, chip_h-0.06,
           size=9.5, bold=True, color=BLACK, align=PP_ALIGN.CENTER)

    # Connector: Groq → Consensus
    vcr(arc_cx, r3_y + r3_h, r4_y)

    # ── ROW 5: RESEARCH COMPOSITION → INSTITUTIONAL TERMINAL  (y=4.86)
    r5_y, r5_h = 4.86, 0.54
    comp_w = 4.50; mid_gap = 0.33; term_w = 4.70
    row5_total = comp_w + mid_gap + term_w   # 9.53
    row5_sx    = arc_cx - row5_total / 2     # 1.90
    comp_x     = row5_sx                     # 1.90
    term_x     = row5_sx + comp_w + mid_gap  # 6.73

    # Research Composition Layer
    box(s, comp_x, r5_y, comp_w, r5_h, C_BG, DIM, Pt(0.75))
    box(s, comp_x, r5_y, 0.05, r5_h, ORANGE)
    tb(s, "\U0001f4cb  RESEARCH COMPOSITION LAYER",
       comp_x+0.12, r5_y+0.06, comp_w-0.18, 0.24,
       size=10, bold=True, color=WHITE)
    tb(s, "Executive Thesis  \u2022  Bull vs Bear  \u2022  Risk Register  "
          "\u2022  Catalyst Calendar  \u2022  Decision Box",
       comp_x+0.12, r5_y+0.32, comp_w-0.18, 0.18, size=7.5, color=LG)

    # Arrow: Composition → Terminal
    ar5 = s.shapes.add_shape(33,
        Inches(comp_x+comp_w), Inches(r5_y+r5_h/2-0.07),
        Inches(mid_gap), Inches(0.14))
    ar5.fill.solid(); ar5.fill.fore_color.rgb = ORANGE; ar5.line.fill.background()

    # Institutional Research Terminal
    box(s, term_x, r5_y, term_w, r5_h, C_BG, ORANGE, Pt(1.2))
    box(s, term_x, r5_y, 0.05, r5_h, ORANGE)
    tb(s, "\U0001f3e6  INSTITUTIONAL RESEARCH TERMINAL",
       term_x+0.12, r5_y+0.06, term_w-0.18, 0.24,
       size=10, bold=True, color=ORANGE)
    tb(s, "Research Dashboard  \u2022  PDF Dossier  \u2022  Investment Recommendation",
       term_x+0.12, r5_y+0.32, term_w-0.18, 0.18, size=7.5, color=WHITE)

    # Connector: Consensus bottom → Row 5
    vcr(arc_cx, r4_y + r4_h, r5_y)

    # ── BOTTOM: TECH STACK BAR  (y=5.48) ─────────────────────────
    ts_y = 5.48; ts_h = 0.44
    box(s, 0.55, ts_y, 12.23, ts_h, C_BG, DIM, Pt(0.75))
    tb(s, "TECH STACK", 0.70, ts_y+0.13, 1.30, 0.22,
       size=9, bold=True, color=ORANGE)
    box(s, 2.10, ts_y+0.10, 0.012, ts_h-0.20, DIM)

    tech_items = [
        ("Frontend", "React + Vite"),
        ("Backend",  "FastAPI"),
        ("AI",       "Groq Llama 3.3"),
        ("Data",     "Yahoo Finance + Google News"),
        ("Deploy",   "Vercel + Render"),
    ]
    for t_i, (lbl, val) in enumerate(tech_items):
        tx = 2.30 + t_i * 2.10
        tb_t = s.shapes.add_textbox(Inches(tx), Inches(ts_y+0.09),
                                    Inches(2.00), Inches(ts_h-0.10))
        tf_t = tb_t.text_frame; tf_t.word_wrap = True
        tf_t.margin_top = Inches(0); tf_t.margin_bottom = Inches(0)
        tf_t.margin_left = Inches(0); tf_t.margin_right = Inches(0)
        p_t = tf_t.paragraphs[0]
        r_lbl = p_t.add_run(); r_lbl.text = f"{lbl}:  "
        r_lbl.font.size = Pt(8.5); r_lbl.font.bold = True
        r_lbl.font.color.rgb = ORANGE; r_lbl.font.name = FONT
        r_val = p_t.add_run(); r_val.text = val
        r_val.font.size = Pt(8.5); r_val.font.color.rgb = LG; r_val.font.name = FONT

    # ── BOTTOM: KEY ARCHITECTURAL ADVANTAGE bar  (y=6.00) ────────
    ins_y = 6.00; ins_h = 1.36
    box(s, 0.55, ins_y, 12.23, ins_h, C_BG, ORANGE, Pt(1.2))
    box(s, 0.55, ins_y, 0.05, ins_h, ORANGE)

    box(s, 0.75, ins_y-0.14, 3.10, 0.28, ORANGE)
    tb(s, "KEY ARCHITECTURAL ADVANTAGE",
       0.75, ins_y-0.10, 3.10, 0.22, size=9, bold=True,
       color=BLACK, align=PP_ALIGN.CENTER)

    tb_ins = s.shapes.add_textbox(Inches(0.75), Inches(ins_y+0.16),
                                  Inches(11.83), Inches(1.04))
    tf_ins = tb_ins.text_frame; tf_ins.word_wrap = True
    tf_ins.margin_top = Inches(0); tf_ins.margin_bottom = Inches(0)
    tf_ins.margin_left = Inches(0); tf_ins.margin_right = Inches(0)
    p_ins = tf_ins.paragraphs[0]; p_ins.alignment = PP_ALIGN.CENTER
    ins_runs = [
        ("Unlike traditional AI systems that rely on a single model response, Quantum ", False),
        ("distributes financial reasoning across specialized agents", True),
        (" and validates outcomes through a ", False),
        ("consensus engine", True),
        (" before generating investment recommendations \u2014 "
         "delivering traceable, explainable, institutional-grade intelligence.", False),
    ]
    for txt, hi in ins_runs:
        r_i = p_ins.add_run(); r_i.text = txt
        r_i.font.size = Pt(12); r_i.font.name = FONT; r_i.font.italic = True
        r_i.font.bold = hi
        r_i.font.color.rgb = ORANGE if hi else LG

    slide_number(s, 8)
    return s


# ═══════════════════════════════════════════════════════════════════
#  SLIDE 09 — CHALLENGES & LEARNINGS  (PREMIUM STORYTELLING)
# ═══════════════════════════════════════════════════════════════════
def slide_09(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, SW, SH)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x05, 0x05, 0x05)
    bg.line.fill.background()

    ORANGE = RGBColor(0xFF, 0x8C, 0x42)
    C_BG   = RGBColor(0x11, 0x11, 0x11)
    C_BG2  = RGBColor(0x1a, 0x10, 0x05)   # warm dark tint for learning strip
    DIM    = RGBColor(0x28, 0x28, 0x28)
    LG     = RGBColor(0x9c, 0xa3, 0xaf)
    BLACK  = RGBColor(0x05, 0x05, 0x05)

    box(s, 0, 0, 13.33, 0.06, ORANGE)

    # ── TITLE ─────────────────────────────────────────────────────
    tb(s, "CHALLENGES & LEARNINGS",
       0.55, 0.10, 12.2, 0.44, size=34, bold=True, color=WHITE)

    # Subtitle
    tb_sub = s.shapes.add_textbox(Inches(0.55), Inches(0.57),
                                  Inches(12.2), Inches(0.26))
    tf_sub = tb_sub.text_frame; tf_sub.word_wrap = True
    tf_sub.margin_top = Inches(0); tf_sub.margin_bottom = Inches(0)
    tf_sub.margin_left = Inches(0); tf_sub.margin_right = Inches(0)
    p_sub = tf_sub.paragraphs[0]
    r_s1 = p_sub.add_run()
    r_s1.text = "Building production-grade financial AI required solving problems "
    r_s1.font.size = Pt(12); r_s1.font.color.rgb = LG
    r_s1.font.name = FONT; r_s1.font.italic = True
    r_s2 = p_sub.add_run()
    r_s2.text = "far beyond model prompting."
    r_s2.font.size = Pt(12); r_s2.font.bold = True
    r_s2.font.color.rgb = ORANGE; r_s2.font.name = FONT; r_s2.font.italic = True

    # ── 4 VERTICAL-FLOW CHALLENGE CARDS  (y=1.00, h=3.70) ─────────
    # 4 cards side-by-side with 3 gaps of 0.22
    # card_w = (13.33 - 0.35 - 0.35 - 3*0.22) / 4 = 2.9925
    card_w = 2.99
    card_h = 3.70
    card_y = 1.00
    gaps   = 0.22

    # (main_icon, title, challenge_text, solution_text, learning_text)
    cards = [
        ("\U0001f6e1\ufe0f",
         "DATA RELIABILITY",
         "Market APIs return inconsistent data.",
         "Validation layer + preprocessing + fallbacks.",
         "Reliable AI starts with reliable data."),

        ("\u2696\ufe0f",
         "CONFLICTING SIGNALS",
         "Technical, fundamental & sentiment outputs disagreed.",
         "Weighted Consensus Engine.",
         "Multiple viewpoints outperform a single opinion."),

        ("\U0001f50d",
         "EXPLAINABILITY",
         "Users need to understand every recommendation.",
         "Confidence scoring + traceable reasoning.",
         "Trust is as important as accuracy."),

        ("\u26a1",
         "SCALABILITY",
         "Repeated queries raised latency & API load.",
         "Caching + modular architecture.",
         "Production systems require resilience."),
    ]

    for c_idx, (icon, title, challenge, solution, learning) in enumerate(cards):
        cx = 0.35 + c_idx * (card_w + gaps)   # left edge of card

        # ── Card container ────────────────────────────────────────
        box(s, cx, card_y, card_w, card_h, C_BG, ORANGE, Pt(1.2))
        box(s, cx, card_y, card_w, 0.05, ORANGE)   # top bar
        box(s, cx, card_y, 0.05, card_h, ORANGE)   # left bar

        # ── Large main icon ───────────────────────────────────────
        tb_icon = s.shapes.add_textbox(
            Inches(cx), Inches(card_y+0.12), Inches(card_w), Inches(0.52))
        tf_icon = tb_icon.text_frame; tf_icon.word_wrap = False
        tf_icon.margin_top = Inches(0); tf_icon.margin_bottom = Inches(0)
        tf_icon.margin_left = Inches(0); tf_icon.margin_right = Inches(0)
        p_icon = tf_icon.paragraphs[0]; p_icon.alignment = PP_ALIGN.CENTER
        r_icon = p_icon.add_run(); r_icon.text = icon
        r_icon.font.size = Pt(38); r_icon.font.name = FONT

        # ── Card title ────────────────────────────────────────────
        tb(s, title, cx+0.10, card_y+0.68, card_w-0.16, 0.40,
           size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

        # Orange divider below title
        box(s, cx+0.20, card_y+1.14, card_w-0.40, 0.025, ORANGE)

        # ── Challenge row  (warning icon + text) ─────────────────
        tb_ch = s.shapes.add_textbox(
            Inches(cx+0.12), Inches(card_y+1.20), Inches(card_w-0.22), Inches(0.52))
        tf_ch = tb_ch.text_frame; tf_ch.word_wrap = True
        tf_ch.margin_top = Inches(0); tf_ch.margin_bottom = Inches(0)
        tf_ch.margin_left = Inches(0); tf_ch.margin_right = Inches(0)
        p_ch = tf_ch.paragraphs[0]
        r_ch1 = p_ch.add_run()
        r_ch1.text = "\u26a0\ufe0f  "
        r_ch1.font.size = Pt(13); r_ch1.font.color.rgb = ORANGE; r_ch1.font.name = FONT
        r_ch2 = p_ch.add_run()
        r_ch2.text = challenge
        r_ch2.font.size = Pt(10); r_ch2.font.color.rgb = LG; r_ch2.font.name = FONT

        # ── Arrow ▼ ───────────────────────────────────────────────
        tb_arr1 = s.shapes.add_textbox(
            Inches(cx), Inches(card_y+1.76), Inches(card_w), Inches(0.22))
        tf_arr1 = tb_arr1.text_frame; tf_arr1.word_wrap = False
        tf_arr1.margin_top = Inches(0); tf_arr1.margin_bottom = Inches(0)
        tf_arr1.margin_left = Inches(0); tf_arr1.margin_right = Inches(0)
        p_arr1 = tf_arr1.paragraphs[0]; p_arr1.alignment = PP_ALIGN.CENTER
        r_arr1 = p_arr1.add_run(); r_arr1.text = "\u25bc"
        r_arr1.font.size = Pt(12); r_arr1.font.color.rgb = ORANGE; r_arr1.font.name = FONT

        # ── Solution row  (wrench icon + text) ───────────────────
        tb_sol = s.shapes.add_textbox(
            Inches(cx+0.12), Inches(card_y+2.02), Inches(card_w-0.22), Inches(0.50))
        tf_sol = tb_sol.text_frame; tf_sol.word_wrap = True
        tf_sol.margin_top = Inches(0); tf_sol.margin_bottom = Inches(0)
        tf_sol.margin_left = Inches(0); tf_sol.margin_right = Inches(0)
        p_sol = tf_sol.paragraphs[0]
        r_sol1 = p_sol.add_run()
        r_sol1.text = "\U0001f6e0\ufe0f  "
        r_sol1.font.size = Pt(13); r_sol1.font.color.rgb = ORANGE; r_sol1.font.name = FONT
        r_sol2 = p_sol.add_run()
        r_sol2.text = solution
        r_sol2.font.size = Pt(10); r_sol2.font.color.rgb = WHITE; r_sol2.font.name = FONT

        # ── Arrow ▼ ───────────────────────────────────────────────
        tb_arr2 = s.shapes.add_textbox(
            Inches(cx), Inches(card_y+2.56), Inches(card_w), Inches(0.22))
        tf_arr2 = tb_arr2.text_frame; tf_arr2.word_wrap = False
        tf_arr2.margin_top = Inches(0); tf_arr2.margin_bottom = Inches(0)
        tf_arr2.margin_left = Inches(0); tf_arr2.margin_right = Inches(0)
        p_arr2 = tf_arr2.paragraphs[0]; p_arr2.alignment = PP_ALIGN.CENTER
        r_arr2 = p_arr2.add_run(); r_arr2.text = "\u25bc"
        r_arr2.font.size = Pt(12); r_arr2.font.color.rgb = ORANGE; r_arr2.font.name = FONT

        # ── Learning strip (tinted bg + bulb icon + italic bold) ──
        box(s, cx+0.08, card_y+2.82, card_w-0.12, 0.68, C_BG2, ORANGE, Pt(0.75))
        box(s, cx+0.08, card_y+2.82, 0.04, 0.68, ORANGE)

        tb_lrn = s.shapes.add_textbox(
            Inches(cx+0.17), Inches(card_y+2.88), Inches(card_w-0.28), Inches(0.56))
        tf_lrn = tb_lrn.text_frame; tf_lrn.word_wrap = True
        tf_lrn.margin_top = Inches(0); tf_lrn.margin_bottom = Inches(0)
        tf_lrn.margin_left = Inches(0); tf_lrn.margin_right = Inches(0)
        p_lrn = tf_lrn.paragraphs[0]
        r_lrn1 = p_lrn.add_run()
        r_lrn1.text = "\U0001f4a1  "
        r_lrn1.font.size = Pt(13); r_lrn1.font.color.rgb = ORANGE; r_lrn1.font.name = FONT
        r_lrn2 = p_lrn.add_run()
        r_lrn2.text = learning
        r_lrn2.font.size = Pt(10); r_lrn2.font.bold = True; r_lrn2.font.italic = True
        r_lrn2.font.color.rgb = WHITE; r_lrn2.font.name = FONT

    # ── BOTTOM: BIGGEST LESSON  (y=4.84) ──────────────────────────
    bot_y = 4.84; bot_h = 2.30
    box(s, 0.35, bot_y, 12.63, bot_h, C_BG, ORANGE, Pt(1.8))
    box(s, 0.35, bot_y, 0.07, bot_h, ORANGE)

    # Overlapping tab
    box(s, 0.55, bot_y-0.14, 2.30, 0.28, ORANGE)
    tb(s, "BIGGEST LESSON",
       0.55, bot_y-0.10, 2.30, 0.22, size=9, bold=True,
       color=BLACK, align=PP_ALIGN.CENTER)

    # Intro sentence
    tb(s, "Building Quantum revealed that great financial AI requires four non-negotiable pillars:",
       0.55, bot_y+0.14, 12.23, 0.30, size=12, color=LG, italic=True)

    # 4 large pillar chips
    pillar_labels = [
        "DATA QUALITY",
        "EXPLAINABILITY",
        "CONSENSUS VALIDATION",
        "SYSTEM RELIABILITY",
    ]
    # chip_w = (12.63 - 0.50 - 3*0.18) / 4 = 2.932
    chip_w  = 2.93
    chip_h  = 0.70
    chip_gap = 0.18
    chip_y  = bot_y + 0.52
    chip_x0 = 0.49

    for p_i, plabel in enumerate(pillar_labels):
        chip_x = chip_x0 + p_i * (chip_w + chip_gap)
        box(s, chip_x, chip_y, chip_w, chip_h, ORANGE)
        tb(s, plabel, chip_x+0.08, chip_y+0.20, chip_w-0.14, chip_h-0.32,
           size=13, bold=True, color=BLACK, align=PP_ALIGN.CENTER)

    # Final tagline
    tb_tag = s.shapes.add_textbox(Inches(0.55), Inches(bot_y+1.34),
                                  Inches(12.23), Inches(0.32))
    tf_tag = tb_tag.text_frame; tf_tag.word_wrap = True
    tf_tag.margin_top = Inches(0); tf_tag.margin_bottom = Inches(0)
    tf_tag.margin_left = Inches(0); tf_tag.margin_right = Inches(0)
    p_tag = tf_tag.paragraphs[0]; p_tag.alignment = PP_ALIGN.CENTER
    r_tag1 = p_tag.add_run()
    r_tag1.text = "Model intelligence alone is "
    r_tag1.font.size = Pt(14); r_tag1.font.italic = True
    r_tag1.font.color.rgb = LG; r_tag1.font.name = FONT
    r_tag2 = p_tag.add_run()
    r_tag2.text = "not enough."
    r_tag2.font.size = Pt(14); r_tag2.font.bold = True; r_tag2.font.italic = True
    r_tag2.font.color.rgb = ORANGE; r_tag2.font.name = FONT

    slide_number(s, 9)
    return s


# ═══════════════════════════════════════════════════════════════════
#  SLIDE 10 — THANK YOU
# ═══════════════════════════════════════════════════════════════════
def slide_10(prs):
    s = new_slide(prs)
    box(s, 0, 0, 13.33, 0.06, AMBER)

    # Large watermark (ghost text)
    tb(s, "QUANTUM", 0.4, 0.9, 9.5, 3.5, size=130, bold=True,
       color=RGBColor(0x14, 0x14, 0x14))

    # Overlay text
    tb(s, "Thank You.", 0.55, 1.8, 9.0, 1.5, size=80, bold=True, color=WHITE)
    tb(s, "We look forward to your questions.", 0.55, 3.25, 9.0, 0.55,
       size=22, color=AMBER)

    box(s, 0.55, 4.0, 5.5, 0.028, AMBER)

    tb(s, "Team Logic Legends   |   Capgemini AgentifAI Buildathon 2025",
       0.55, 4.15, 9.0, 0.36, size=13, color=LGRAY)

    # GitHub link card
    box(s, 0.55, 4.7, 7.0, 0.72, CARD, BORDER)
    box(s, 0.55, 4.7, 0.040, 0.72, AMBER)
    tb(s, "GitHub Repository", 0.7, 4.76, 2.5, 0.26, size=11, bold=True, color=AMBER)
    tb(s, "github.com/AbhiTrivedi2712/QUANTAM-AI-RESEARCH-AGENT",
       0.7, 5.02, 6.7, 0.34, size=12, color=LGRAY)

    # Right: project summary
    box(s, 7.8, 1.6, 5.3, 5.6, CARD, BORDER)
    box(s, 7.8, 1.6, 0.040, 5.6, AMBER)
    tb(s, "Project at a Glance", 7.95, 1.7, 5.1, 0.36, size=14, bold=True, color=WHITE)
    box(s, 7.95, 2.04, 4.9, 0.025, BORDER2)
    summary_lines = [
        "Multi-Agent AI Platform for Financial Intelligence",
        "3 Specialist Agents: Technical  /  Fundamental  /  Sentiment",
        "Weighted Consensus Engine: 40%  +  35%  +  25%",
        "Real-Time Data via Yahoo Finance + RSS News Fallback",
        "Groq LLM + Google Gemini 1.5 for Narrative Intelligence",
        "React 18 + FastAPI + Vite — Full-Stack Architecture",
        "Offline Fallback Engine — Zero Downtime Guarantee",
        "5-min In-Memory Cache — Under 10ms Repeat Queries",
        "Auto Indian Ticker Resolution (.NS suffix detection)",
        "Deployed: Render (Backend)  /  Vercel (Frontend)",
    ]
    for i, line in enumerate(summary_lines):
        cy = 2.16 + i*0.5
        box(s, 7.95, cy+0.15, 0.07, 0.07, AMBER)
        tb(s, line, 8.12, cy+0.06, 4.8, 0.4, size=11.5, color=LGRAY)

    slide_number(s, 10)
    return s


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════
def main():
    print("QUANTUM PPT — Premium Redesign (Black + Gold)")
    print("=" * 50)
    print("Architecture image : " + (ARCH_IMG     or "NOT FOUND"))
    print("Pipeline image     : " + (PIPELINE_IMG or "NOT FOUND"))
    print("Dashboard screen 1 : " + (DASH_SCREEN1 or "NOT FOUND"))
    print("Dashboard screen 2 : " + (DASH_SCREEN2 or "NOT FOUND"))
    print()

    prs = Presentation()
    prs.slide_width  = SW
    prs.slide_height = SH

    print("Building slides...")
    slide_01(prs);  print("  [OK] Slide 01 - Cover")
    slide_02(prs);  print("  [OK] Slide 02 - The Problem")
    slide_03(prs);  print("  [OK] Slide 03 - Our Solution")
    slide_04(prs);  print("  [OK] Slide 04 - How It Works")
    slide_05(prs);  print("  [OK] Slide 05 - Technical Architecture & Intelligence Flow")
    slide_06(prs);  print("  [OK] Slide 06 - Approach & Methodology [NEW]")
    slide_07(prs);  print("  [OK] Slide 07 - Solution Demonstration [NEW]")
    slide_08(prs);  print("  [OK] Slide 08 - Technical Architecture [NEW]")
    slide_09(prs);  print("  [OK] Slide 09 - Challenges & Learnings [NEW]")
    slide_10(prs);  print("  [OK] Slide 10 - Thank You [NEW]")

    out = r"C:\Users\singh\QUANTAM-AI-RESEARCH-AGENT\QUANTUM_Deep_Dive_Presentation.pptx"
    prs.save(out)
    print()
    print("DONE! Saved to:")
    print("  " + out)
    print()
    print("Open in Microsoft PowerPoint - ready to present!")

if __name__ == "__main__":
    main()
