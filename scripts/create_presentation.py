"""
Generate a vibrant, executive 10-slide PowerPoint presentation for Project 23:
Music Streaming Trends Analysis (Music_Streaming_Trends_Analysis.pptx)
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

# Rich, cohesive Spotify + Modern Analytics Palette
NAVY       = RGBColor(15, 23, 42)     # #0F172A
DARK_CARD  = RGBColor(30, 41, 59)     # #1E293B
EMERALD    = RGBColor(29, 185, 84)    # #1DB954 (Spotify Green)
BLUE       = RGBColor(37, 99, 235)    # #2563EB
VIOLET     = RGBColor(124, 58, 237)   # #7C3AED
CORAL      = RGBColor(244, 63, 94)    # #F43F5E
AMBER      = RGBColor(245, 158, 11)   # #F59E0B
TEAL       = RGBColor(13, 148, 136)   # #0D9488
SLATE      = RGBColor(71, 85, 105)    # #475569
LIGHT_BG   = RGBColor(244, 247, 251)  # #F4F7FB
WHITE      = RGBColor(255, 255, 255)
SOFT_BLUE  = RGBColor(239, 246, 255)
SOFT_GREEN = RGBColor(236, 253, 245)
SOFT_VIO   = RGBColor(245, 243, 255)
SOFT_CORAL = RGBColor(255, 241, 242)
SOFT_AMBER = RGBColor(255, 251, 235)
BORDER     = RGBColor(203, 213, 225)


def set_bg(slide, color=LIGHT_BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, title_text, subtitle_text, badge_text, accent=BLUE):
    # Top multi-color accent strip
    widths = [(0.0, 4.5, EMERALD), (4.5, 4.5, BLUE), (9.0, 4.333, VIOLET)]
    for x, w, col in widths:
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(0), Inches(w), Inches(0.12))
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

    # Category pill badge
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.26), Inches(2.5), Inches(0.32))
    pill.fill.solid()
    pill.fill.fore_color.rgb = accent
    pill.line.fill.background()
    ptf = pill.text_frame
    ptf.margin_left = ptf.margin_right = Inches(0.1)
    ptf.margin_top = ptf.margin_bottom = Inches(0.02)
    pp = ptf.paragraphs[0]
    pp.text = badge_text.upper()
    pp.alignment = PP_ALIGN.CENTER
    pp.font.size = Pt(10)
    pp.font.bold = True
    pp.font.color.rgb = WHITE

    # Title & Subtitle
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.62), Inches(12.1), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(25)
    p.font.bold = True
    p.font.color.rgb = NAVY
    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.size = Pt(12.5)
        p2.font.color.rgb = SLATE


def add_card(slide, left, top, width, height, title, body, accent, bg_color=WHITE, title_size=14, body_size=12.5):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = BORDER
    card.line.width = Pt(1)

    # Left colored stripe
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top + 0.08), Inches(0.09), Inches(height - 0.16))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = accent
    stripe.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(left + 0.22), Inches(top + 0.12), Inches(width - 0.34), Inches(height - 0.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.size = Pt(title_size)
    p1.font.bold = True
    p1.font.color.rgb = accent
    p1.space_after = Pt(4)

    p2 = tf.add_paragraph()
    p2.text = body
    p2.font.size = Pt(body_size)
    p2.font.color.rgb = NAVY


def add_image_slide(prs, title, subtitle, badge, accent, img_path, cards=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    add_header(slide, title, subtitle, badge, accent)
    if Path(img_path).exists():
        if cards:
            # Framed chart container on left
            frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(1.55), Inches(8.2), Inches(5.45))
            frame.fill.solid()
            frame.fill.fore_color.rgb = WHITE
            frame.line.color.rgb = BORDER
            slide.shapes.add_picture(str(img_path), Inches(0.68), Inches(1.68), width=Inches(7.94))

            # Right-hand insight cards
            card_h = (5.45 - 0.18 * (len(cards) - 1)) / len(cards)
            for idx, (c_title, c_body, c_col, c_bg) in enumerate(cards):
                add_card(
                    slide, 8.95, 1.55 + idx * (card_h + 0.18), 3.85, card_h,
                    c_title, c_body, c_col, c_bg, title_size=12.5, body_size=11.5
                )
        else:
            frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(1.52), Inches(11.63), Inches(5.6))
            frame.fill.solid()
            frame.fill.fore_color.rgb = WHITE
            frame.line.color.rgb = BORDER
            slide.shapes.add_picture(str(img_path), Inches(1.05), Inches(1.64), width=Inches(11.23))


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ------------------------------------------------------------------
    # Slide 1: Hero Title Slide
    # ------------------------------------------------------------------
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s1, NAVY)

    # Decorative color blocks on right
    for y, h, col in [(0.0, 2.5, EMERALD), (2.5, 2.5, BLUE), (5.0, 2.5, VIOLET)]:
        b = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.95), Inches(y), Inches(0.383), Inches(h))
        b.fill.solid()
        b.fill.fore_color.rgb = col
        b.line.fill.background()

    # Left glowing accent bar
    lbar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.85), Inches(1.65), Inches(0.12), Inches(3.8))
    lbar.fill.solid()
    lbar.fill.fore_color.rgb = EMERALD
    lbar.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.65), Inches(10.8), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "HCL TECH INDUSTRY-GRADE PROJECT  ·  PROJECT #23"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = EMERALD

    p1 = tf.add_paragraph()
    p1.text = "Music Streaming Trends Analysis"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "Python Audio-Feature Analytics   |   Oracle SQL Star Schema   |   Power BI Trend Dashboard"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(147, 197, 253)
    p2.space_before = Pt(14)

    p3 = tf.add_paragraph()
    p3.text = "Presented by: Pranjal Singh (2500320100842)"
    p3.font.size = Pt(16)
    p3.font.bold = True
    p3.font.color.rgb = AMBER
    p3.space_before = Pt(20)

    p4 = tf.add_paragraph()
    p4.text = "Domain: Sports & Entertainment   ·   github.com/pranjalsingh670/Music_Streaming_Trends_Analysis-2500320100842-Pranjal_singh"
    p4.font.size = Pt(13)
    p4.font.color.rgb = RGBColor(203, 213, 225)
    p4.space_before = Pt(8)

    # Bottom KPI Preview Pills on Slide 1
    pills = [
        ("75.89B", "Total Streams", EMERALD),
        ("2,500", "Cleaned Tracks", BLUE),
        ("35 / 10", "Artists / Genres", VIOLET),
        ("62.65", "Avg Popularity", AMBER),
    ]
    for i, (val, lbl, col) in enumerate(pills):
        x = 1.2 + i * 2.85
        box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(5.85), Inches(2.55), Inches(1.05))
        box.fill.solid()
        box.fill.fore_color.rgb = DARK_CARD
        box.line.color.rgb = col
        box.line.width = Pt(1.75)
        btf = box.text_frame
        bp1 = btf.paragraphs[0]
        bp1.text = val
        bp1.alignment = PP_ALIGN.CENTER
        bp1.font.size = Pt(22)
        bp1.font.bold = True
        bp1.font.color.rgb = col
        bp2 = btf.add_paragraph()
        bp2.text = lbl
        bp2.alignment = PP_ALIGN.CENTER
        bp2.font.size = Pt(11)
        bp2.font.color.rgb = WHITE

    # ------------------------------------------------------------------
    # Slide 2: Problem Statement & KPIs
    # ------------------------------------------------------------------
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s2)
    add_header(s2, "Problem Statement & KPI Definitions",
               "Aligning data quality engineering with music streaming analytics",
               "01 · Objectives & KPIs", BLUE)

    add_card(s2, 0.6, 1.6, 5.9, 2.55,
             "Business Challenge",
             "Raw Spotify catalogues contain duplicate tracks, missing or malformed release dates, and out-of-range popularity scores that distort artist rankings and audio-feature trend models.",
             CORAL, SOFT_CORAL, title_size=15, body_size=13)
    add_card(s2, 6.8, 1.6, 5.9, 2.55,
             "Solution Architecture",
             "End-to-end Python (pandas/scipy) cleaning & EDA -> Oracle SQL Star Schema (DDL, Load, Views) -> Power BI Dashboard with 5 KPI cards, 4 slicers, and drill-down.",
             EMERALD, SOFT_GREEN, title_size=15, body_size=13)

    kpi_cards = [
        ("KPI 1: Total Streams", "75.893 Billion streams across 2,500 canonical tracks (100% reconciled).", BLUE, SOFT_BLUE),
        ("KPI 2: Avg Popularity", "62.65 / 100 mean score bounded strictly to [0, 100].", VIOLET, SOFT_VIO),
        ("KPI 3: Artist Share %", "Top 10 artists capture ~74.3% of all platform streams.", TEAL, SOFT_GREEN),
        ("KPI 4: Correlation (r)", "Loudness (+0.400) & Danceability (+0.326) lead popularity.", AMBER, SOFT_AMBER),
    ]
    for i, (t, b, c, bgc) in enumerate(kpi_cards):
        add_card(s2, 0.6 + i * 3.1, 4.45, 2.9, 2.45, t, b, c, bgc, title_size=13, body_size=12)

    # ------------------------------------------------------------------
    # Slide 3: Data Quality Audit & Key Test Cases
    # ------------------------------------------------------------------
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s3)
    add_header(s3, "Data Quality Audit & Key Test Cases",
               "Reconciling 2,575 raw Spotify records to 2,500 canonical tracks",
               "02 · Data Quality", CORAL)

    tcs = [
        ("TC-01: Duplicate Tracks (75 Detected)",
         "45 exact row duplicates + 30 near-duplicates (same track_name + artist_name) resolved by sorting streams DESC and retaining the canonical record.",
         BLUE, SOFT_BLUE),
        ("TC-02: Missing & Malformed Release Dates (70 Detected)",
         "55 NULL dates + 15 malformed strings ('2022-13-45', 'unknown') coerced, imputed via artist/global median, and flagged (IS_IMPUTED_DATE = 'Y').",
         AMBER, SOFT_AMBER),
        ("TC-03: Outlier Popularity (25 Detected)",
         "Out-of-range scores (< 0 or > 100, e.g., -12, 999) replaced with genre median popularity; 0 invalid values remain post-cleaning.",
         CORAL, SOFT_CORAL),
        ("100% Cross-Tool Reconciliation",
         "Zero orphan foreign keys in Oracle Star Schema; Python pandas Top 10 Artists by Streams matches SQL DENSE_RANK() 100%.",
         EMERALD, SOFT_GREEN),
    ]
    positions = [(0.6, 1.65), (6.8, 1.65), (0.6, 4.45), (6.8, 4.45)]
    for (x, y), (t, b, c, bgc) in zip(positions, tcs):
        add_card(s3, x, y, 5.9, 2.45, t, b, c, bgc, title_size=15, body_size=13)

    # ------------------------------------------------------------------
    # Slide 4: Star Schema
    # ------------------------------------------------------------------
    add_image_slide(
        prs,
        "Oracle SQL Star Schema Architecture",
        "Normalized warehouse design in sql/01_ddl_star_schema.sql",
        "03 · Data Model", VIOLET,
        "docs/star_schema_diagram.png",
    )

    # ------------------------------------------------------------------
    # Slide 5: Top 10 Artists
    # ------------------------------------------------------------------
    add_image_slide(
        prs,
        "Top 10 Artists by Total Streams (Verified)",
        "100% reconciled between Python pandas and Oracle SQL DENSE_RANK()",
        "04 · Artist Rankings", EMERALD,
        "docs/charts/top_10_artists.png",
        [
            ("#1 Taylor Swift", "8,969.31M streams across her catalogue.", EMERALD, SOFT_GREEN),
            ("#2 Bad Bunny & #3 Drake", "8,318.66M and 7,925.43M streams respectively.", BLUE, SOFT_BLUE),
            ("Top 10 Concentration", "56.39B streams (~74.3% of total platform volume).", VIOLET, SOFT_VIO),
            ("SQL Verification", "Exact match on rank, track count, and stream totals.", TEAL, SOFT_GREEN),
        ],
    )

    # ------------------------------------------------------------------
    # Slide 6: Genre Performance
    # ------------------------------------------------------------------
    add_image_slide(
        prs,
        "Streaming Volume by Genre",
        "Pop, Hip-Hop, and Latin drive two-thirds of total platform streams",
        "05 · Genre Mix", TEAL,
        "docs/charts/genre_performance.png",
        [
            ("Pop Leads All Genres", "25,596.88M streams (33.7% platform share).", BLUE, SOFT_BLUE),
            ("Hip-Hop & Latin", "15,592.52M (20.5%) and 9,733.68M (12.8%).", VIOLET, SOFT_VIO),
            ("Global Expansion", "K-Pop (7,292M) and Afrobeats (1,856M) show strong draw.", AMBER, SOFT_AMBER),
        ],
    )

    # ------------------------------------------------------------------
    # Slide 7: Yearly Audio-Feature Trends
    # ------------------------------------------------------------------
    add_image_slide(
        prs,
        "Yearly Audio-Feature Evolution (2015–2025)",
        "Excluding imputed dates (IS_IMPUTED_DATE = 'N') for pure temporal accuracy",
        "06 · 10-Year Trends", AMBER,
        "docs/charts/yearly_audio_trends.png",
    )

    # ------------------------------------------------------------------
    # Slide 8: Feature Correlation Heatmap
    # ------------------------------------------------------------------
    add_image_slide(
        prs,
        "Audio Features vs. Popularity Correlation",
        "Pearson correlation matrix across 2,500 cleaned tracks",
        "07 · Statistical Drivers", CORAL,
        "docs/charts/feature_correlation_heatmap.png",
        [
            ("Loudness (r = +0.4001)", "Strongest positive driver of track popularity.", CORAL, SOFT_CORAL),
            ("Danceability (r = +0.3261)", "Rhythmically engaging tracks chart higher.", EMERALD, SOFT_GREEN),
            ("Energy (r = +0.2645)", "Upbeat production outperforms low-energy tracks.", BLUE, SOFT_BLUE),
            ("Acousticness (r = -0.3743)", "Acoustic-heavy tracks show lower mass popularity.", VIOLET, SOFT_VIO),
        ],
    )

    # ------------------------------------------------------------------
    # Slide 9: Power BI Dashboard Mockup
    # ------------------------------------------------------------------
    add_image_slide(
        prs,
        "Power BI Executive Dashboard & Slicers",
        "5 KPI cards, 4 global slicers (Year, Genre, Tier, Explicit), and drill-down",
        "08 · Power BI", BLUE,
        "powerbi/dashboard_mockup.png",
    )

    # ------------------------------------------------------------------
    # Slide 10: Recommendations & Deliverables
    # ------------------------------------------------------------------
    s10 = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s10)
    add_header(s10, "Key Recommendations & Project Deliverables",
               "Actionable takeaways for labels, A&R, and playlist curation teams",
               "09 · Summary", EMERALD)

    recs = [
        ("Playlist & A&R Strategy",
         "Prioritize high-danceability, louder, concise (< 3.3 min) tracks across Pop, Hip-Hop, and Latin for maximum streaming velocity.",
         EMERALD, SOFT_GREEN),
        ("Data Governance at Ingestion",
         "Enforce automated deduplication on (track_name, artist_name), date validation flags, and [0, 100] popularity CHECK constraints.",
         BLUE, SOFT_BLUE),
        ("Complete Deliverables Checklist",
         "Executed Jupyter Notebook (.ipynb) · SRS with GitHub link · Oracle SQL (DDL, Load, Queries, Views) · Star Schema Diagram · Power BI DAX & Guide · Data Quality Report · Insights Summary · Demo Script · PPTX.",
         VIOLET, SOFT_VIO),
    ]
    for idx, (t, b, c, bgc) in enumerate(recs):
        add_card(s10, 0.6, 1.65 + idx * 1.8, 12.1, 1.55, t, b, c, bgc, title_size=15, body_size=13)

    out_path = Path("Music_Streaming_Trends_Analysis.pptx")
    try:
        prs.save(out_path)
        print(f"Saved {out_path}")
    except PermissionError:
        alt_path = Path("Music_Streaming_Trends_Analysis_Colored.pptx")
        prs.save(alt_path)
        print(f"Main PPTX was open/locked; saved {alt_path}")


if __name__ == "__main__":
    main()
