# Data Quality Report
## Project 23: Music Streaming Trends Analysis

### 1. Executive Summary
The raw Spotify tracks dataset (`data/raw/spotify_tracks_raw.csv`) contained **2,575 records** across 21 attributes. Following deterministic cleaning and validation in `music_streaming_trends_analysis.ipynb`, **2,500 canonical tracks** were retained and exported to the star schema (`data/cleaned/`), achieving 100% schema compliance for Oracle SQL and Power BI.

---

### 2. Key Test Cases & Remediation Summary

| Test Case ID | Issue Category | Detected Count | Detection Rule | Remediation Action | Post-Clean Count |
|---|---|---|---|---|---|
| **TC-01a** | Exact Row Duplicates | 45 | `df.duplicated()` | Drop exact duplicate rows | 0 |
| **TC-01b** | Near-Duplicate Tracks | 30 | `df.duplicated(subset=['track_name', 'artist_name'])` | Sort by `streams DESC`, keep canonical highest-stream entry | 0 |
| **TC-02a** | Missing Release Dates (`NULL`) | 55 | `release_date.isna()` | Impute using artist median release date (fallback: global median) and set `is_imputed_date = 'Y'` | 0 |
| **TC-02b** | Malformed Release Dates | 15 | `pd.to_datetime(..., errors='coerce').isna()` | Coerce unparseable strings (`2022-13-45`, `unknown`, etc.) to `NaT`, impute & flag `is_imputed_date = 'Y'` | 0 |
| **TC-03** | Outlier Popularity | 25 | `popularity < 0` or `popularity > 100` | Replace invalid scores (`-12` to `999`) with genre median popularity; flag `is_outlier_popularity = True` | 0 |

---

### 3. Reconciliation & Integrity Verification
- **Raw Row Count:** `2,575`
- **Deduplicated Row Count:** `2,500` (`-75` duplicate/near-duplicate rows)
- **Cleaned Total Streams:** `75.893 Billion` (`75,893M`)
- **Star-Schema Table Counts:**
  - `dim_artists.csv`: 35 unique artists
  - `dim_genres.csv`: 10 unique genres
  - `dim_dates.csv`: unique valid/imputed release dates
  - `fact_streams.csv`: 2,500 fact records (zero orphan foreign keys, zero out-of-range popularity scores)
- **Cross-Tool Verification:** Python `groupby` Top 10 Artists by Streams matches the SQL `DENSE_RANK() OVER (ORDER BY SUM(streams) DESC)` query 100%.
