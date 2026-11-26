-- ============================================================================
-- Project 23: Music Streaming Trends Analysis
-- File: 02_load_data.ctl
-- Purpose: Oracle SQL*Loader Control File for FACT_TRACK_STREAM
-- ============================================================================
OPTIONS (SKIP=1, ERRORS=50)
LOAD DATA
INFILE 'data/cleaned/fact_streams.csv'
BADFILE 'sql/fact_streams.bad'
DISCARDFILE 'sql/fact_streams.dsc'
TRUNCATE
INTO TABLE FACT_TRACK_STREAM
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    TRACK_KEY,
    TRACK_ID,
    TRACK_NAME,
    ARTIST_ID,
    GENRE_ID,
    DATE_ID,
    STREAMS,
    POPULARITY,
    EXPLICIT_FLAG,
    DURATION_MS,
    DANCEABILITY,
    ENERGY,
    VALENCE,
    TEMPO_BPM,
    LOUDNESS_DB,
    ACOUSTICNESS,
    INSTRUMENTALNESS,
    LIVENESS,
    SPEECHINESS
)
