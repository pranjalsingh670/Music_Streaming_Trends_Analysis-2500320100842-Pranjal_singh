# Software Requirements Specification (SRS)
## Project 23: Music Streaming Trends Analysis

**Document Version:** 1.0  
**Date:** November 26, 2026  
**Domain:** Sports and Entertainment  
**GitHub Repository:** [https://github.com/pranjalsingh670/HCL-project](https://github.com/pranjalsingh670/HCL-project)

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) defines the functional, data, analytical, and architectural requirements for **Project 23: Music Streaming Trends Analysis**. The system ingests raw Spotify track and audio-feature metadata, performs automated data quality remediation in Python, persists a normalized star schema in Oracle SQL, and delivers interactive executive analytics in Power BI.

### 1.2 Scope
The solution covers:
- End-to-end ETL and exploratory data analysis in Python (`music_streaming_trends_analysis.ipynb`).
- Relational star-schema modeling, data loading, window-function queries, and analytical views in Oracle SQL (`sql/`).
- Interactive KPI cards, slicers, and drill-down dashboards in Power BI (`powerbi/`).
- Comprehensive documentation, data-quality auditing, insights reporting, and executive presentation (`Music_Streaming_Trends_Analysis.pptx`).

### 1.3 Problem Statement
Streaming platforms and music labels manage millions of tracks with varying audio characteristics (`danceability`, `energy`, `valence`, `loudness_db`, `tempo_bpm`, `acousticness`, `duration_ms`). Raw catalogues frequently suffer from duplicate track entries, missing or malformed release dates, and out-of-range popularity scores. Without a clean, reconciled analytical pipeline, stakeholders cannot accurately identify top-performing artists, track multi-year audio-feature shifts, or quantify which audio attributes drive popularity.

---

## 2. KPI Definitions

| KPI Name | Formula / Definition | Target / Acceptance |
|---|---|---|
| **Total Streams** | $\sum \text{STREAMS}$ across deduplicated tracks | Reconciles 100% between Python & Oracle SQL (`75.893B`) |
| **Average Popularity** | $\text{AVG}(\text{POPULARITY})$ bounded to $[0, 100]$ | Zero out-of-range values post-cleaning (`62.65`) |
| **Artist Stream Share (%)** | $(\text{Artist Streams} / \text{Total Platform Streams}) \times 100$ | Top 10 artists verified across Python & SQL |
| **Yearly Feature Trend** | $\text{AVG}(\text{Feature})$ grouped by `RELEASE_YEAR` (excluding imputed dates) | Covers 2015–2025 with YoY deltas |
| **Feature-Popularity Correlation ($r$)** | Pearson correlation $r$ between audio features and `POPULARITY` | Computed with statistical $p$-values |
| **Explicit Track %** | $(\text{Count of Explicit Tracks} / \text{Total Tracks}) \times 100$ | Exposed as KPI card & slicer in Power BI |

---

## 3. System Architecture & Star Schema

The analytical warehouse follows a **Star Schema** (`sql/01_ddl_star_schema.sql`, `docs/star_schema_diagram.png`):
- **Fact Table:** `FACT_TRACK_STREAM` (grain: one canonical track; foreign keys `ARTIST_ID`, `GENRE_ID`, `DATE_ID`; measures `STREAMS`, `POPULARITY`, `DURATION_MS`, and 8 audio features).
- **Dimension Tables:**
  - `DIM_ARTIST` (`ARTIST_ID`, `ARTIST_NAME`, `PRIMARY_GENRE`, `ARTIST_TIER`, `COUNTRY_REGION`)
  - `DIM_GENRE` (`GENRE_ID`, `GENRE_NAME`, `GENRE_CATEGORY`)
  - `DIM_DATE` (`DATE_ID`, `RELEASE_DATE`, `RELEASE_YEAR`, `RELEASE_QUARTER`, `RELEASE_MONTH`, `MONTH_NAME`, `IS_IMPUTED_DATE`)

---

## 4. Functional Requirements

### 4.1 Python Data Engineering & Analysis (`music_streaming_trends_analysis.ipynb`)
- **FR-01:** Ingest `data/raw/spotify_tracks_raw.csv` (2,575 records).
- **FR-02:** Detect and remove exact duplicate rows and near-duplicate `(track_name, artist_name)` pairs, retaining the record with the highest stream count.
- **FR-03:** Parse `release_date`; coerce malformed strings, impute missing dates using artist/global median, and flag imputed rows (`IS_IMPUTED_DATE = 'Y'`).
- **FR-04:** Identify outlier popularity scores (`< 0` or `> 100`) and replace with genre median popularity.
- **FR-05:** Compute Top 10 Artists by Streams, Genre totals, Yearly Audio Feature Trends (2015–2025), and Pearson correlation matrix with $p$-values.
- **FR-06:** Export cleaned star-schema CSVs (`dim_artists.csv`, `dim_genres.csv`, `dim_dates.csv`, `fact_streams.csv`).

### 4.2 Oracle SQL Layer (`sql/`)
- **FR-07:** Define DDL (`01_ddl_star_schema.sql`) with primary keys, foreign keys, `CHECK` constraints (`POPULARITY BETWEEN 0 AND 100`, audio features `BETWEEN 0 AND 1`), and B-tree indexes.
- **FR-08:** Provide SQL*Loader control file (`02_load_data.ctl`) and post-load reconciliation queries (`02_load_data.sql`).
- **FR-09:** Implement analytical queries (`03_top_artist_and_trend_queries.sql`) using `DENSE_RANK()`, `LAG()`, `NTILE(4)`, and `GROUP BY`.
- **FR-10:** Expose Oracle views (`04_analytical_views.sql`: `VW_TOP_ARTISTS_BY_STREAMS`, `VW_YEARLY_AUDIO_TRENDS`, `VW_GENRE_PERFORMANCE`) for Power BI.

### 4.3 Power BI Dashboard (`powerbi/`)
- **FR-11:** Provide DAX measures (`dax_measures.dax`) for KPI cards, YoY stream growth, and `RANKX` artist ranking.
- **FR-12:** Support 4 global slicers (`Release Year`, `Genre`, `Artist Tier`, `Explicit Flag`) and drill-down hierarchies (`Year -> Quarter -> Month` and `Genre -> Artist -> Track`).

---

## 5. Non-Functional Requirements
- **NFR-01 (Reproducibility):** Fixed random seed (`SEED = 42`) and deterministic cleaning rules ensure 100% repeatable results.
- **NFR-02 (Data Integrity):** Enforced via Oracle `CHECK` and `FOREIGN KEY` constraints plus Python `assert` verification checks.
- **NFR-03 (Performance):** Indexed foreign keys and pre-aggregated Oracle views ensure sub-second Power BI slicer responsiveness.

---

## 6. Data Source, Verification Approach & Key Test Cases

- **Data Source & Verification Approach:** Spotify tracks dataset (`2,575` raw rows -> `2,500` cleaned rows); Top 10 artists by streams cross-verified between Python `pandas` and SQL `DENSE_RANK()`.
- **Key Test Cases:**
  1. **Duplicate Tracks:** 45 exact duplicates + 30 near-duplicates detected and deduplicated.
  2. **Missing Release Dates:** 55 `NULL` + 15 malformed dates detected, imputed, and flagged (`is_imputed_date = 'Y'`).
  3. **Outlier Popularity:** 25 out-of-range popularity values (`-12` to `999`) detected and remediated to valid `[0, 100]` range.

---

## 7. Measurable Acceptance Criteria
1. **Top Artists, Genres & Yearly Trends Correct:** Top 10 artists (`Taylor Swift` #1 at `8,969.31M` streams), 10 genres (`Pop` #1 at `25,596.88M`), and 2015–2025 feature trends match 100% across Python and SQL.
2. **Feature-Popularity Correlation Shown:** Pearson $r$ and $p$-values computed and visualized (`loudness_db` $+0.4001$, `danceability` $+0.3261$, `acousticness` $-0.3743$).
3. **All Industry-Grade Deliverables Completed:** SRS (with GitHub link), Jupyter Notebook, Oracle SQL scripts, Star Schema diagram, Power BI assets, Data Quality Report, Insights Summary, PPTX deck, Demo Video Script, and README.
