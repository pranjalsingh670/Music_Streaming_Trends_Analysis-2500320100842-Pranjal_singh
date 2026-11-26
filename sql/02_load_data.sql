-- ============================================================================
-- Project 23: Music Streaming Trends Analysis
-- File: 02_load_data.sql
-- Purpose: Oracle SQL Staging & Verification Load Script
-- Note: Use SQL*Loader (02_load_data.ctl) or Oracle External Tables / SQL Developer
--       Import Wizard to populate DIM_* and FACT_TRACK_STREAM from data/cleaned/*.csv
-- ============================================================================

-- Example SQL*Loader invocation (run from OS shell):
-- sqlldr userid=analytics/password@ORCL control=sql/02_load_data.ctl log=load_fact.log bad=load_fact.bad

-- Post-Load Reconciliation Checks (must match Python cleaned dataset counts)
SELECT 'DIM_ARTIST' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM DIM_ARTIST
UNION ALL
SELECT 'DIM_GENRE'  AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM DIM_GENRE
UNION ALL
SELECT 'DIM_DATE'   AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM DIM_DATE
UNION ALL
SELECT 'FACT_TRACK_STREAM' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM FACT_TRACK_STREAM;

-- Data Integrity Verification: Ensure no NULLs in key metrics or orphan foreign keys
SELECT COUNT(*) AS ORPHAN_ARTISTS
FROM FACT_TRACK_STREAM f
LEFT JOIN DIM_ARTIST a ON f.ARTIST_ID = a.ARTIST_ID
WHERE a.ARTIST_ID IS NULL;

SELECT COUNT(*) AS OUT_OF_RANGE_POPULARITY
FROM FACT_TRACK_STREAM
WHERE POPULARITY < 0 OR POPULARITY > 100;
