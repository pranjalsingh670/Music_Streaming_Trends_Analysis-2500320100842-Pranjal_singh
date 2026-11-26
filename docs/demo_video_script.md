# Demo Video Script (3 Minutes)
## Project 23: Music Streaming Trends Analysis

| Segment | Duration | Visual on Screen | Narration Points |
|---|---|---|---|
| **1. Introduction & Problem** | 0:00 – 0:30 | Title slide + GitHub repo README | Introduce Project 23 (*Music Streaming Trends Analysis*, Sports & Entertainment domain). State the goal: uncover top streaming artists/genres, 2015–2025 audio-feature shifts, and drivers of track popularity. |
| **2. Data Quality & Cleaning** | 0:30 – 1:10 | Jupyter Notebook (`music_streaming_trends_analysis.ipynb`) | Walk through the 2,575 raw tracks and the 3 key test cases: 75 duplicate/near-duplicate tracks removed, 70 missing/malformed release dates imputed and flagged, and 25 outlier popularity scores (`<0` or `>100`) remediated. |
| **3. Python EDA & Verification** | 1:10 – 1:55 | Notebook charts (`top_10_artists.png`, `yearly_audio_trends.png`, `feature_correlation_heatmap.png`) | Show the Top 10 Artists by Streams and confirm 100% reconciliation with SQL `DENSE_RANK()`. Highlight yearly rise in danceability, shorter track durations, and correlation between danceability/loudness and popularity. |
| **4. Oracle SQL Star Schema** | 1:55 – 2:25 | `docs/star_schema_diagram.png` + `sql/` scripts | Briefly explain `DIM_ARTIST`, `DIM_GENRE`, `DIM_DATE`, and `FACT_TRACK_STREAM` plus analytical views (`VW_TOP_ARTISTS_BY_STREAMS`, `VW_YEARLY_AUDIO_TRENDS`). |
| **5. Power BI Dashboard** | 2:25 – 3:00 | Power BI Desktop / `powerbi/dashboard_mockup.png` | Demonstrate the 5 KPI cards, 4 global slicers (Year, Genre, Artist Tier, Explicit), and drill-down (`Genre -> Artist -> Track`). Wrap up with key business takeaways. |
