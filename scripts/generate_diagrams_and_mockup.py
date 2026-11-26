"""
Generate Star-Schema ER Diagram (docs/star_schema_diagram.png)
and Power BI Dashboard Mockup (powerbi/dashboard_mockup.png).
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np


def draw_star_schema():
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    ax.text(
        50, 95,
        "Project 23: Music Streaming Trends Analysis — Star Schema (Oracle SQL & Power BI)",
        ha="center", va="center", fontsize=14, fontweight="bold", color="#0F172A"
    )

    def draw_table(x, y, w, h, title, fields, header_color):
        # Shadow
        ax.add_patch(mpatches.FancyBboxPatch(
            (x + 0.6, y - 0.6), w, h, boxstyle="round,pad=0.4",
            facecolor="#CBD5E1", edgecolor="none", zorder=1
        ))
        # Body
        ax.add_patch(mpatches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.4",
            facecolor="#FFFFFF", edgecolor="#334155", linewidth=1.4, zorder=2
        ))
        # Header
        ax.add_patch(mpatches.FancyBboxPatch(
            (x, y + h - 6), w, 6, boxstyle="round,pad=0.4",
            facecolor=header_color, edgecolor="#334155", linewidth=1.4, zorder=3
        ))
        ax.text(x + w / 2, y + h - 3, title, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color="white", zorder=4)

        step = (h - 7.5) / max(len(fields), 1)
        for idx, fld in enumerate(fields):
            fy = y + h - 8.2 - idx * step
            ax.text(x + 1.5, fy, fld, ha="left", va="center",
                    fontsize=8.3, family="monospace", color="#1E293B", zorder=4)

    # Fact Table (Center)
    draw_table(
        34, 24, 32, 62,
        "FACT_TRACK_STREAM",
        [
            "PK  TRACK_KEY (NUMBER)",
            "UQ  TRACK_ID (VARCHAR2)",
            "    TRACK_NAME (VARCHAR2)",
            "FK  ARTIST_ID (NUMBER)",
            "FK  GENRE_ID (NUMBER)",
            "FK  DATE_ID (NUMBER)",
            "--- Metrics & Features ---",
            "    STREAMS (NUMBER)",
            "    POPULARITY (0-100)",
            "    EXPLICIT_FLAG (Y/N)",
            "    DURATION_MS (NUMBER)",
            "    DANCEABILITY (0-1)",
            "    ENERGY (0-1)",
            "    VALENCE (0-1)",
            "    TEMPO_BPM (NUMBER)",
            "    LOUDNESS_DB (NUMBER)",
            "    ACOUSTICNESS (0-1)",
            "    INSTRUMENTALNESS (0-1)",
            "    LIVENESS / SPEECHINESS",
        ],
        "#1D4ED8"
    )

    # DIM_ARTIST (Left)
    draw_table(
        3, 55, 24, 28,
        "DIM_ARTIST",
        [
            "PK  ARTIST_ID",
            "    ARTIST_NAME",
            "    PRIMARY_GENRE",
            "    ARTIST_TIER",
            "    COUNTRY_REGION",
        ],
        "#0F766E"
    )

    # DIM_GENRE (Right)
    draw_table(
        73, 55, 24, 24,
        "DIM_GENRE",
        [
            "PK  GENRE_ID",
            "UQ  GENRE_NAME",
            "    GENRE_CATEGORY",
        ],
        "#7C3AED"
    )

    # DIM_DATE (Left Bottom)
    draw_table(
        3, 14, 24, 31,
        "DIM_DATE",
        [
            "PK  DATE_ID (YYYYMMDD)",
            "    RELEASE_DATE",
            "    RELEASE_YEAR",
            "    RELEASE_QUARTER",
            "    RELEASE_MONTH",
            "    MONTH_NAME",
            "    IS_IMPUTED_DATE",
        ],
        "#B45309"
    )

    # Relationships
    arrow_kw = dict(arrowstyle="-|>", lw=2.0, color="#475569", mutation_scale=15)
    ax.annotate("", xy=(34, 66), xytext=(27, 68), arrowprops=arrow_kw)
    ax.text(30.5, 69.5, "1 : N", fontsize=9, fontweight="bold", color="#0F766E", ha="center")

    ax.annotate("", xy=(66, 66), xytext=(73, 66), arrowprops=arrow_kw)
    ax.text(69.5, 68.5, "1 : N", fontsize=9, fontweight="bold", color="#7C3AED", ha="center")

    ax.annotate("", xy=(34, 38), xytext=(27, 30), arrowprops=arrow_kw)
    ax.text(29.5, 37.5, "1 : N", fontsize=9, fontweight="bold", color="#B45309", ha="center")

    Path("docs").mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig("docs/star_schema_diagram.png", dpi=160)
    plt.close()
    print("Saved docs/star_schema_diagram.png")


def draw_powerbi_mockup():
    df = pd.read_csv("data/cleaned/spotify_tracks_cleaned.csv")
    fig = plt.figure(figsize=(15, 8.5), facecolor="#F1F5F9")

    # Top Title Bar
    fig.text(0.02, 0.955, "SPOTIFY MUSIC STREAMING TRENDS DASHBOARD  |  Power BI Executive View",
             fontsize=15, fontweight="bold", color="#0F172A")
    fig.text(0.02, 0.925, "Slicers: [Year: 2015-2025]   [Genre: All]   [Artist Tier: All]   [Explicit: All]",
             fontsize=10, color="#475569")

    # KPI Cards
    kpis = [
        ("TOTAL STREAMS", f"{df['streams'].sum() / 1e9:.2f} B", "#1D4ED8"),
        ("TOTAL TRACKS", f"{len(df):,}", "#0F766E"),
        ("UNIQUE ARTISTS", f"{df['artist_name'].nunique()}", "#7C3AED"),
        ("AVG POPULARITY", f"{df['popularity'].mean():.1f} / 100", "#B45309"),
        ("EXPLICIT SHARE", f"{(df['explicit_flag'] == 'Y').mean() * 100:.1f}%", "#BE123C"),
    ]
    for idx, (label, val, col) in enumerate(kpis):
        ax_k = fig.add_axes([0.02 + idx * 0.194, 0.80, 0.18, 0.10])
        ax_k.set_facecolor("white")
        for spine in ax_k.spines.values():
            spine.set_edgecolor("#CBD5E1")
        ax_k.set_xticks([])
        ax_k.set_yticks([])
        ax_k.text(0.5, 0.68, label, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#64748B")
        ax_k.text(0.5, 0.28, val, ha="center", va="center", fontsize=16, fontweight="bold", color=col)

    # Panel 1: Top 10 Artists
    ax1 = fig.add_axes([0.05, 0.42, 0.42, 0.32])
    top10 = df.groupby("artist_name")["streams"].sum().nlargest(10).sort_values() / 1e6
    ax1.barh(top10.index, top10.values, color="#1D4ED8", alpha=0.88)
    ax1.set_title("Top 10 Artists by Total Streams (M)", fontsize=11, fontweight="bold", pad=8)
    ax1.set_xlabel("Streams (Millions)")
    ax1.grid(axis="x", linestyle="--", alpha=0.4)

    # Panel 2: Genre Share
    ax2 = fig.add_axes([0.54, 0.42, 0.43, 0.32])
    g_streams = df.groupby("genre")["streams"].sum().sort_values(ascending=True) / 1e6
    ax2.barh(g_streams.index, g_streams.values, color="#0F766E", alpha=0.88)
    ax2.set_title("Total Streams by Genre (M)", fontsize=11, fontweight="bold", pad=8)
    ax2.set_xlabel("Streams (Millions)")
    ax2.grid(axis="x", linestyle="--", alpha=0.4)

    # Panel 3: Yearly Audio Feature Trends
    ax3 = fig.add_axes([0.05, 0.06, 0.42, 0.28])
    yr = df[df["is_imputed_date"] == "N"].groupby("release_year")[["danceability", "energy", "valence"]].mean()
    for col, c in zip(["danceability", "energy", "valence"], ["#1D4ED8", "#EA580C", "#16A34A"]):
        ax3.plot(yr.index, yr[col], marker="o", label=col.title(), color=c, linewidth=2)
    ax3.set_title("Yearly Audio Feature Trends (2015–2025)", fontsize=11, fontweight="bold", pad=8)
    ax3.legend(fontsize=8)
    ax3.grid(True, linestyle="--", alpha=0.4)

    # Panel 4: Feature-Popularity Scatter
    ax4 = fig.add_axes([0.54, 0.06, 0.43, 0.28])
    sample = df.sample(min(500, len(df)), random_state=42)
    ax4.scatter(sample["danceability"], sample["popularity"], alpha=0.45, s=22, color="#7C3AED")
    m, b = np.polyfit(df["danceability"], df["popularity"], 1)
    xs = np.linspace(df["danceability"].min(), df["danceability"].max(), 50)
    ax4.plot(xs, m * xs + b, color="#0F172A", linewidth=2)
    r_val = df["danceability"].corr(df["popularity"])
    ax4.set_title(f"Danceability vs Popularity (r = {r_val:+.3f})", fontsize=11, fontweight="bold", pad=8)
    ax4.set_xlabel("Danceability")
    ax4.set_ylabel("Popularity")
    ax4.grid(True, linestyle="--", alpha=0.4)

    Path("powerbi").mkdir(exist_ok=True)
    plt.savefig("powerbi/dashboard_mockup.png", dpi=150)
    plt.close()
    print("Saved powerbi/dashboard_mockup.png")


if __name__ == "__main__":
    draw_star_schema()
    draw_powerbi_mockup()
