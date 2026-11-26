"""
Generate an executive 10-slide PowerPoint presentation for Project 23:
Music Streaming Trends Analysis (Music_Streaming_Trends_Analysis.pptx)
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

NAVY = RGBColor(15, 23, 42)
BLUE = RGBColor(29, 78, 216)
TEAL = RGBColor(15, 118, 110)
SLATE = RGBColor(71, 85, 105)
LIGHT_BG = RGBColor(248, 250, 252)
WHITE = RGBColor(255, 255, 255)


def set_bg(slide, color=LIGHT_BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, title_text, subtitle_text=""):
    # Top accent bar
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(0.14))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.32), Inches(12.1), Inches(0.95))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = NAVY
    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.size = Pt(13)
        p2.font.color.rgb = SLATE


def add_bullets(slide, items, left=0.65, top=1.45, width=12.0, height=5.5, font_size=16):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for idx, (head, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = f"• {head}: " if head else "• "
        r1.font.bold = True
        r1.font.size = Pt(font_size)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = body
        r2.font.size = Pt(font_size)
        r2.font.color.rgb = SLATE


def add_image_slide(prs, title, subtitle, img_path, caption_bullets=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    add_header(slide, title, subtitle)
    if Path(img_path).exists():
        if caption_bullets:
            slide.shapes.add_picture(str(img_path), Inches(0.55), Inches(1.4), width=Inches(8.1))
            add_bullets(slide, caption_bullets, left=8.85, top=1.5, width=4.0, height=5.4, font_size=13.5)
        else:
            slide.shapes.add_picture(str(img_path), Inches(0.9), Inches(1.35), width=Inches(11.5))


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title Slide
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s1, NAVY)
    bar = s1.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.28), Inches(7.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "HCL TECH INDUSTRY-GRADE PROJECT  |  PROJECT #23"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(96, 165, 250)

    p1 = tf.add_paragraph()
    p1.text = "Music Streaming Trends Analysis"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "Python Audio-Feature Analytics  ·  Oracle SQL Star Schema  ·  Power BI Trend Dashboard"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_before = Pt(16)

    p3 = tf.add_paragraph()
    p3.text = "Domain: Sports & Entertainment  |  GitHub: github.com/pranjalsingh670/music-streaming-trends-analysis"
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_before = Pt(30)

    # Slide 2: Problem Statement & KPIs
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s2)
    add_header(s2, "Problem Statement & KPI Definitions", "Aligning data engineering with music streaming business decisions")
    add_bullets(s2, [
        ("Business Challenge", "Raw streaming catalogues contain duplicate tracks, missing/malformed release dates, and out-of-range popularity scores that distort artist rankings and trend models."),
        ("Objective", "Build a reconciled Python -> Oracle SQL -> Power BI pipeline to track Top Artists, Genre performance, 2015–2025 audio-feature shifts, and popularity drivers."),
        ("KPI 1 — Total Streams", "75.893 Billion streams across 2,500 canonical tracks (100% reconciled across Python & SQL)."),
        ("KPI 2 — Average Popularity", "62.65 / 100 mean popularity after outlier remediation."),
        ("KPI 3 — Artist Stream Share (%)", "Top 10 artists capture ~74.3% of total platform streams."),
        ("KPI 4 — Feature-Popularity Correlation (r)", "Pearson correlation & p-values quantifying impact of loudness, danceability, energy, and acousticness."),
    ])

    # Slide 3: Data Quality Audit & Key Test Cases
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s3)
    add_header(s3, "Data Quality Audit & Key Test Cases", "Reconciling 2,575 raw Spotify records to 2,500 canonical tracks")
    add_bullets(s3, [
        ("TC-01: Duplicate Tracks (75 detected)", "45 exact row duplicates + 30 near-duplicates (same track_name + artist_name) resolved by retaining the highest-stream record."),
        ("TC-02: Missing & Malformed Release Dates (70 detected)", "55 NULL dates + 15 malformed strings (e.g., '2022-13-45', 'unknown') imputed via artist/global median and flagged (IS_IMPUTED_DATE = 'Y')."),
        ("TC-03: Outlier Popularity (25 detected)", "Out-of-range values (< 0 or > 100, e.g., -12, 999) replaced with genre median popularity; 0 invalid values remain."),
        ("Reconciliation Result", "100% pass on Oracle CHECK & FK constraints and Python-to-SQL Top 10 Artist cross-verification."),
    ])

    # Slide 4: Star Schema Architecture
    add_image_slide(
        prs,
        "Oracle SQL Star Schema Architecture",
        "Normalized warehouse design in sql/01_ddl_star_schema.sql",
        "docs/star_schema_diagram.png",
    )

    # Slide 5: Top 10 Artists by Streams
    add_image_slide(
        prs,
        "Top 10 Artists by Total Streams (Verified)",
        "100% reconciled between Python pandas and Oracle SQL DENSE_RANK()",
        "docs/charts/top_10_artists.png",
        [
            ("#1 Taylor Swift", "8,969.31M streams"),
            ("#2 Bad Bunny", "8,318.66M streams"),
            ("#3 Drake", "7,925.43M streams"),
            ("Top 10 Concentration", "56.39B streams (~74.3% of all platform streams)."),
            ("SQL Verification", "Exact match on artist rank, track count, and stream totals."),
        ],
    )

    # Slide 6: Genre Performance
    add_image_slide(
        prs,
        "Streaming Volume by Genre",
        "Pop, Hip-Hop, and Latin drive two-thirds of total streams",
        "docs/charts/genre_performance.png",
        [
            ("Pop Dominance", "25,596.88M streams (33.7% share)."),
            ("Hip-Hop & Latin", "15,592.52M (20.5%) and 9,733.68M (12.8%)."),
            ("Global Growth", "K-Pop (7,292M) and Afrobeats (1,856M) show strong engagement."),
        ],
    )

    # Slide 7: Yearly Audio-Feature Trends
    add_image_slide(
        prs,
        "Yearly Audio-Feature Evolution (2015–2025)",
        "Excluding imputed dates (IS_IMPUTED_DATE = 'N') for pure temporal accuracy",
        "docs/charts/yearly_audio_trends.png",
    )

    # Slide 8: Correlation Matrix
    add_image_slide(
        prs,
        "Audio Features vs. Popularity Correlation",
        "Pearson correlation matrix across 2,500 cleaned tracks",
        "docs/charts/feature_correlation_heatmap.png",
        [
            ("Loudness (r = +0.4001)", "Strongest positive correlation with popularity."),
            ("Danceability (r = +0.3261)", "Rhythmically engaging tracks chart higher."),
            ("Energy (r = +0.2645)", "Upbeat tracks outperform low-energy tracks."),
            ("Acousticness (r = -0.3743)", "Acoustic-heavy tracks show lower mass popularity."),
        ],
    )

    # Slide 9: Power BI Executive Dashboard
    add_image_slide(
        prs,
        "Power BI Trend Dashboard & Slicers",
        "5 KPI cards, 4 global slicers, and Genre -> Artist -> Track drill-down",
        "powerbi/dashboard_mockup.png",
    )

    # Slide 10: Recommendations & Deliverables
    s10 = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s10)
    add_header(s10, "Key Recommendations & Project Deliverables", "Actionable takeaways for labels, A&R, and playlist teams")
    add_bullets(s10, [
        ("Playlist & A&R Strategy", "Prioritize high-danceability, louder, concise (<3.3 min) tracks in Pop, Hip-Hop, and Latin for maximum stream velocity."),
        ("Data Governance", "Enforce automated deduplication and [0, 100] popularity checks at ingestion before BI reporting."),
        ("Deliverables Included", "Executed Jupyter Notebook (.ipynb), SRS with GitHub link, Oracle SQL DDL/Load/Queries/Views, Star Schema diagram, Power BI DAX & Guide, Data Quality Report, Insights Summary, Demo Script, and PPTX."),
    ])

    out_path = Path("Music_Streaming_Trends_Analysis.pptx")
    prs.save(out_path)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
