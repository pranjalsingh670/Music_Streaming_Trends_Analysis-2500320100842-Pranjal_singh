# Project 23: Music Streaming Trends Analysis

**Domain:** Sports and Entertainment  
**Tech Stack:** Python (`pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`) · Oracle SQL · Power BI  

---

## Overview
An end-to-end data analytics solution analyzing Spotify track performance, artist streaming dominance, 10-year audio-feature evolution (2015–2025), and statistical drivers of track popularity.

## Repository Structure
```text
├── data/
│   ├── generate_spotify_dataset.py   # Reproducible raw dataset generator (with test cases)
│   ├── raw/spotify_tracks_raw.csv    # 2,575 raw tracks (duplicates, missing dates, outliers)
│   └── cleaned/                      # 2,500 cleaned tracks + Star Schema CSVs
├── sql/
│   ├── 01_ddl_star_schema.sql        # Oracle DDL (DIM_ARTIST, DIM_GENRE, DIM_DATE, FACT_TRACK_STREAM)
│   ├── 02_load_data.sql              # Post-load reconciliation & integrity checks
│   ├── 02_load_data.ctl              # SQL*Loader control file
│   ├── 03_top_artist_and_trend_queries.sql
│   └── 04_analytical_views.sql       # Oracle Views for Power BI
├── powerbi/
│   ├── dax_measures.dax              # KPI, RANKX, and YoY DAX measures
│   ├── PowerBI_Dashboard_Guide.md    # Step-by-step .pbix build & slicer/drill-down guide
│   └── dashboard_mockup.png          # Executive dashboard visual preview
├── docs/
│   ├── charts/                       # Exported publication-quality charts
│   ├── star_schema_diagram.png       # Star Schema ER diagram
│   ├── data_quality_report.md        # Key Test Cases & reconciliation audit
│   ├── insights_summary.md           # Key analytical findings
│   └── demo_video_script.md          # 3-minute demo walkthrough script
├── music_streaming_trends_analysis.ipynb  # Executed Python EDA & cleaning notebook
├── SRS_Music_Streaming_Trends_Analysis.md # Software Requirements Specification
├── Music_Streaming_Trends_Analysis.pptx   # Executive PowerPoint presentation
└── README.md
```

## Key Results
- **Dataset Reconciliation:** `2,575` raw rows cleaned to `2,500` canonical tracks (`75.893B` total streams, `62.65` avg popularity).
- **Top 3 Artists by Streams:** Taylor Swift (`8,969.31M`), Bad Bunny (`8,318.66M`), Drake (`7,925.43M`) — **100% verified** between Python and SQL `DENSE_RANK()`.
- **Top Genre:** Pop (`25,596.88M` streams, 33.7% share).
- **Strongest Popularity Correlations:** `loudness_db` ($r = +0.4001$), `danceability` ($r = +0.3261$), `energy` ($r = +0.2645$), `acousticness` ($r = -0.3743$).

## Quick Start
```powershell
# 1. Create virtual environment & install dependencies
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pandas seaborn matplotlib scipy nbformat jupyter python-pptx python-docx

# 2. Generate raw data & run notebook
.\.venv\Scripts\python.exe data\generate_spotify_dataset.py
.\.venv\Scripts\jupyter.exe nbconvert --to notebook --execute --inplace music_streaming_trends_analysis.ipynb
```
