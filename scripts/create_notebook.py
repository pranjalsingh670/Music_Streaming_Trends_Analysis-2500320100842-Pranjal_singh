"""
Build the Project 23 Jupyter Notebook: music_streaming_trends_analysis.ipynb
"""

import nbformat as nbf
from pathlib import Path


def md(text: str):
    return nbf.v4.new_markdown_cell(text.strip())


def code(src: str):
    return nbf.v4.new_code_cell(src.strip())


nb = nbf.v4.new_notebook()
nb["metadata"]["kernelspec"] = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}

cells = [
    md("""
# Project 23: Music Streaming Trends Analysis
**Domain:** Sports and Entertainment  
**Tech Stack:** Python (pandas, numpy, scipy, matplotlib, seaborn) | Oracle SQL | Power BI  

## 1. Problem Statement & KPI Definitions
Music streaming platforms generate massive catalogues of tracks with rich audio metadata (danceability, energy, valence, tempo, loudness, acousticness). Record labels, playlist curators, and A&R teams need to understand:
1. Which **artists and genres** dominate total streaming volume?
2. How have **audio features evolved** over the last decade (2015–2025)?
3. Which **audio features correlate** most strongly with track popularity?

### Key Performance Indicators (KPIs)
| KPI | Definition |
|---|---|
| **Total Streams** | Sum of streams across all deduplicated tracks |
| **Average Popularity** | Mean Spotify popularity score (0–100) after outlier remediation |
| **Artist Stream Share (%)** | Artist streams divided by total platform streams |
| **Track Duration (min)** | Mean track length in minutes (`duration_ms / 60000`) |
| **Feature-Popularity Correlation ($r$)** | Pearson correlation between each audio feature and `popularity` |
"""),

    code("""
import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.dpi"] = 120

CHARTS_DIR = Path("docs/charts")
CHARTS_DIR.mkdir(parents=True, exist_ok=True)
CLEAN_DIR = Path("data/cleaned")
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

df_raw = pd.read_csv("data/raw/spotify_tracks_raw.csv")
print(f"Raw dataset shape: {df_raw.shape[0]:,} rows x {df_raw.shape[1]} columns")
df_raw.head(3)
"""),

    md("""
## 2. Data Quality Audit & Key Test Cases
We explicitly test the three required edge cases from the project specification:
1. **Duplicate Tracks**: Exact `track_id` duplicates and near-duplicates sharing `(track_name, artist_name)`.
2. **Missing / Malformed Release Dates**: `NaN` or unparseable date strings.
3. **Outlier Popularity**: Values outside the valid `[0, 100]` range.
"""),

    code("""
# Test Case 1: Duplicate Tracks
exact_dup_count = df_raw.duplicated().sum()
id_dup_count = df_raw.duplicated(subset=["track_id"]).sum()
near_dup_count = df_raw.duplicated(subset=["track_name", "artist_name"]).sum()

# Test Case 2: Missing & Malformed Release Dates
parsed_dates = pd.to_datetime(df_raw["release_date"], errors="coerce")
missing_date_raw = df_raw["release_date"].isna().sum()
malformed_date_count = parsed_dates.isna().sum() - missing_date_raw

# Test Case 3: Outlier Popularity
outlier_pop_mask = (df_raw["popularity"] < 0) | (df_raw["popularity"] > 100) | df_raw["popularity"].isna()
outlier_pop_count = outlier_pop_mask.sum()

audit_summary = pd.DataFrame([
    {"Test Case": "TC-01a: Exact Row Duplicates", "Detected Count": int(exact_dup_count), "Action": "Drop exact duplicates"},
    {"Test Case": "TC-01b: Near-Duplicate (Track + Artist)", "Detected Count": int(near_dup_count - exact_dup_count), "Action": "Keep record with highest streams"},
    {"Test Case": "TC-02a: Missing Release Dates (NULL)", "Detected Count": int(missing_date_raw), "Action": "Impute with artist/global median & flag"},
    {"Test Case": "TC-02b: Malformed Release Dates", "Detected Count": int(malformed_date_count), "Action": "Coerce to NaT, impute & flag"},
    {"Test Case": "TC-03: Outlier Popularity (<0 or >100)", "Detected Count": int(outlier_pop_count), "Action": "Replace with genre median popularity"},
])
audit_summary
"""),

    md("""
## 3. Data Cleaning & Reconciliation
Let's apply deterministic cleaning rules and verify row counts and stream totals before and after cleaning.
"""),

    code("""
df = df_raw.copy()

# 1. Deduplicate: sort by streams desc so we keep the canonical highest-stream entry
df = df.sort_values("streams", ascending=False)
df = df.drop_duplicates(subset=["track_name", "artist_name"], keep="first").reset_index(drop=True)

# 2. Parse & impute release_date
df["release_date_parsed"] = pd.to_datetime(df["release_date"], errors="coerce")
df["is_imputed_date"] = np.where(df["release_date_parsed"].isna(), "Y", "N")
global_median_date = df["release_date_parsed"].median()
artist_median_dates = df.groupby("artist_name")["release_date_parsed"].transform("median")
df["release_date_clean"] = df["release_date_parsed"].fillna(artist_median_dates).fillna(global_median_date)

df["release_year"] = df["release_date_clean"].dt.year
df["release_quarter"] = df["release_date_clean"].dt.quarter
df["release_month"] = df["release_date_clean"].dt.month

# 3. Fix outlier popularity (<0 or >100) using genre median of valid rows
valid_pop = df["popularity"].between(0, 100)
genre_median_pop = df.loc[valid_pop].groupby("genre")["popularity"].median()
df["is_outlier_popularity"] = ~valid_pop
df.loc[~valid_pop, "popularity"] = df.loc[~valid_pop, "genre"].map(genre_median_pop).round(1)

# Save cleaned dataset
df_clean = df.drop(columns=["release_date_parsed"]).rename(columns={"release_date_clean": "release_date_std"})
df_clean.to_csv(CLEAN_DIR / "spotify_tracks_cleaned.csv", index=False)

print(f"Cleaned dataset shape: {df_clean.shape[0]:,} rows x {df_clean.shape[1]} columns")
print(f"Remaining duplicate (track_name, artist_name): {df_clean.duplicated(subset=['track_name', 'artist_name']).sum()}")
print(f"Remaining NULL release_date_std: {df_clean['release_date_std'].isna().sum()}")
print(f"Remaining out-of-range popularity: {(~df_clean['popularity'].between(0, 100)).sum()}")
"""),

    md("""
## 4. Top 10 Artists by Streams (Verification Against SQL)
We compute the Top 10 artists by total streams in Python and cross-verify against an SQLite window-function query matching our Oracle SQL (`DENSE_RANK() OVER (ORDER BY SUM(streams) DESC)`).
"""),

    code("""
top10_py = (
    df_clean.groupby(["artist_name", "genre"], as_index=False)
    .agg(
        track_count=("track_id", "count"),
        total_streams=("streams", "sum"),
        avg_popularity=("popularity", "mean"),
    )
    .sort_values("total_streams", ascending=False)
    .head(10)
    .reset_index(drop=True)
)
top10_py["artist_rank"] = top10_py.index + 1
top10_py["total_streams_M"] = (top10_py["total_streams"] / 1e6).round(2)
top10_py["avg_popularity"] = top10_py["avg_popularity"].round(2)
top10_py["stream_share_pct"] = (top10_py["total_streams"] * 100.0 / df_clean["streams"].sum()).round(2)

# Cross-verify with SQL query
conn = sqlite3.connect(":memory:")
df_clean.to_sql("fact_tracks", conn, index=False, if_exists="replace")
sql_top10 = pd.read_sql_query('''
    SELECT
        DENSE_RANK() OVER (ORDER BY SUM(streams) DESC) AS artist_rank,
        artist_name,
        SUM(streams) AS total_streams,
        COUNT(track_id) AS track_count
    FROM fact_tracks
    GROUP BY artist_name
    ORDER BY artist_rank
    LIMIT 10
''', conn)
conn.close()

assert (top10_py["artist_name"].values == sql_top10["artist_name"].values).all(), "Mismatch!"
assert (top10_py["total_streams"].values == sql_top10["total_streams"].values).all(), "Stream sum mismatch!"
print("VERIFICATION PASSED: Python and SQL Top 10 Artists by Streams match 100%.")
top10_py[["artist_rank", "artist_name", "genre", "track_count", "total_streams_M", "avg_popularity", "stream_share_pct"]]
"""),

    code("""
fig, ax = plt.subplots(figsize=(10, 5.5))
plot_df = top10_py.sort_values("total_streams_M", ascending=True)
bars = ax.barh(plot_df["artist_name"], plot_df["total_streams_M"], color=sns.color_palette("viridis", len(plot_df)))
ax.set_title("Top 10 Artists by Total Streams (Millions)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Total Streams (Millions)")
ax.set_ylabel("")
for bar in bars:
    w = bar.get_width()
    ax.text(w + 15, bar.get_y() + bar.get_height() / 2, f"{w:,.1f}M", va="center", fontsize=9, fontweight="bold")
ax.set_xlim(0, plot_df["total_streams_M"].max() * 1.15)
plt.tight_layout()
plt.savefig(CHARTS_DIR / "top_10_artists.png", dpi=150)
plt.show()
"""),

    md("""
## 5. Genre Performance & Yearly Audio-Feature Trends (2015–2025)
"""),

    code("""
genre_summary = (
    df_clean.groupby("genre", as_index=False)
    .agg(
        tracks=("track_id", "count"),
        total_streams_M=("streams", lambda s: round(s.sum() / 1e6, 2)),
        avg_popularity=("popularity", "mean"),
        avg_danceability=("danceability", "mean"),
        avg_energy=("energy", "mean"),
        avg_valence=("valence", "mean"),
    )
    .sort_values("total_streams_M", ascending=False)
    .round(3)
)
display(genre_summary)

fig, ax = plt.subplots(figsize=(10, 5))
g_sorted = genre_summary.sort_values("total_streams_M", ascending=True)
bars = ax.barh(g_sorted["genre"], g_sorted["total_streams_M"], color=sns.color_palette("mako", len(g_sorted)))
ax.set_title("Total Streams by Genre (Millions)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Total Streams (Millions)")
for bar in bars:
    w = bar.get_width()
    ax.text(w + 15, bar.get_y() + bar.get_height() / 2, f"{w:,.0f}M", va="center", fontsize=9)
ax.set_xlim(0, g_sorted["total_streams_M"].max() * 1.14)
plt.tight_layout()
plt.savefig(CHARTS_DIR / "genre_performance.png", dpi=150)
plt.show()
"""),

    code("""
yearly_trends = (
    df_clean[df_clean["is_imputed_date"] == "N"]
    .groupby("release_year", as_index=False)
    .agg(
        tracks=("track_id", "count"),
        avg_danceability=("danceability", "mean"),
        avg_energy=("energy", "mean"),
        avg_valence=("valence", "mean"),
        avg_acousticness=("acousticness", "mean"),
        avg_duration_min=("duration_ms", lambda s: s.mean() / 60000.0),
        avg_popularity=("popularity", "mean"),
    )
    .sort_values("release_year")
)

fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
for col, label in [
    ("avg_danceability", "Danceability"),
    ("avg_energy", "Energy"),
    ("avg_valence", "Valence"),
    ("avg_acousticness", "Acousticness"),
]:
    axes[0].plot(yearly_trends["release_year"], yearly_trends[col], marker="o", linewidth=2, label=label)
axes[0].set_title("Yearly Audio Feature Trends (2015–2025)", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Release Year")
axes[0].set_ylabel("Mean Score (0–1)")
axes[0].legend(frameon=True)

axes[1].plot(yearly_trends["release_year"], yearly_trends["avg_duration_min"], marker="s", color="#d95f02", linewidth=2.2)
axes[1].set_title("Average Track Duration Over Time (Minutes)", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Release Year")
axes[1].set_ylabel("Duration (min)")
plt.tight_layout()
plt.savefig(CHARTS_DIR / "yearly_audio_trends.png", dpi=150)
plt.show()

yearly_trends.round(4)
"""),

    md("""
## 6. Correlation Between Audio Features & Popularity
We compute Pearson correlation coefficients ($r$) and p-values between all audio features and `popularity`.
"""),

    code("""
feature_cols = [
    "popularity", "streams", "danceability", "energy", "valence",
    "loudness_db", "tempo_bpm", "acousticness", "instrumentalness",
    "liveness", "speechiness", "duration_ms"
]
corr_matrix = df_clean[feature_cols].corr(method="pearson")

corr_rows = []
for col in feature_cols:
    if col == "popularity":
        continue
    r, p = stats.pearsonr(df_clean[col], df_clean["popularity"])
    corr_rows.append({"Feature": col, "Pearson_r": round(r, 4), "p_value": f"{p:.2e}"})

corr_df = pd.DataFrame(corr_rows).sort_values("Pearson_r", key=abs, ascending=False).reset_index(drop=True)
display(corr_df)

fig, ax = plt.subplots(figsize=(10, 7.5))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", center=0, linewidths=0.5, ax=ax)
ax.set_title("Audio Features & Popularity Correlation Matrix", fontsize=14, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(CHARTS_DIR / "feature_correlation_heatmap.png", dpi=150)
plt.show()
"""),

    code("""
fig, axes = plt.subplots(1, 3, figsize=(14, 4.3))
for ax, feat, color in zip(
    axes,
    ["danceability", "loudness_db", "acousticness"],
    ["#1b9e77", "#7570b3", "#e7298a"],
):
    sns.regplot(
        data=df_clean.sample(min(800, len(df_clean)), random_state=42),
        x=feat,
        y="popularity",
        scatter_kws={"alpha": 0.35, "s": 18, "color": color},
        line_kws={"color": "#222222", "linewidth": 2},
        ax=ax,
    )
    r_val = df_clean[feat].corr(df_clean["popularity"])
    ax.set_title(f"{feat} vs Popularity (r = {r_val:+.3f})", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig(CHARTS_DIR / "popularity_vs_features.png", dpi=150)
plt.show()
"""),

    md("""
## 7. Star Schema Export (Oracle SQL & Power BI)
We export normalized dimension and fact tables to `data/cleaned/` matching `sql/01_ddl_star_schema.sql`.
"""),

    code("""
# DIM_ARTIST
dim_artists = (
    df_clean[["artist_name", "genre", "artist_tier", "country_region"]]
    .drop_duplicates(subset=["artist_name"])
    .sort_values("artist_name")
    .reset_index(drop=True)
)
dim_artists.insert(0, "artist_id", range(1, len(dim_artists) + 1))
dim_artists = dim_artists.rename(columns={"genre": "primary_genre"})
dim_artists.to_csv(CLEAN_DIR / "dim_artists.csv", index=False)

# DIM_GENRE
dim_genres = (
    df_clean[["genre", "genre_category"]]
    .drop_duplicates(subset=["genre"])
    .sort_values("genre")
    .reset_index(drop=True)
)
dim_genres.insert(0, "genre_id", range(1, len(dim_genres) + 1))
dim_genres = dim_genres.rename(columns={"genre": "genre_name"})
dim_genres.to_csv(CLEAN_DIR / "dim_genres.csv", index=False)

# DIM_DATE
dim_dates = (
    df_clean[["release_date_std", "release_year", "release_quarter", "release_month", "is_imputed_date"]]
    .drop_duplicates(subset=["release_date_std", "is_imputed_date"])
    .sort_values("release_date_std")
    .reset_index(drop=True)
)
dim_dates["date_id"] = dim_dates["release_date_std"].dt.strftime("%Y%m%d").astype(int)
dim_dates = dim_dates.drop_duplicates(subset=["date_id"]).reset_index(drop=True)
dim_dates["month_name"] = dim_dates["release_date_std"].dt.strftime("%B")
dim_dates = dim_dates[["date_id", "release_date_std", "release_year", "release_quarter", "release_month", "month_name", "is_imputed_date"]]
dim_dates = dim_dates.rename(columns={"release_date_std": "release_date"})
dim_dates.to_csv(CLEAN_DIR / "dim_dates.csv", index=False)

# FACT_TRACK_STREAM
fact = df_clean.merge(dim_artists[["artist_id", "artist_name"]], on="artist_name", how="left")
fact = fact.merge(dim_genres[["genre_id", "genre_name"]], left_on="genre", right_on="genre_name", how="left")
fact["date_id"] = fact["release_date_std"].dt.strftime("%Y%m%d").astype(int)
fact.insert(0, "track_key", range(1, len(fact) + 1))

fact_cols = [
    "track_key", "track_id", "track_name", "artist_id", "genre_id", "date_id",
    "streams", "popularity", "explicit_flag", "duration_ms",
    "danceability", "energy", "valence", "tempo_bpm", "loudness_db",
    "acousticness", "instrumentalness", "liveness", "speechiness"
]
fact[fact_cols].to_csv(CLEAN_DIR / "fact_streams.csv", index=False)

print("Star Schema Export Summary:")
print(f"  dim_artists.csv  : {len(dim_artists):,} rows")
print(f"  dim_genres.csv   : {len(dim_genres):,} rows")
print(f"  dim_dates.csv    : {len(dim_dates):,} rows")
print(f"  fact_streams.csv : {len(fact):,} rows")
"""),
]

nb["cells"] = cells
Path("music_streaming_trends_analysis.ipynb").write_text(nbf.writes(nb), encoding="utf-8")
print("Wrote music_streaming_trends_analysis.ipynb")
