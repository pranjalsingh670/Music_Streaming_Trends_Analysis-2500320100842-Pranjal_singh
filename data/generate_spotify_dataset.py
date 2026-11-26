"""
Generate a realistic Spotify Tracks dataset (raw) for Project 23:
Music Streaming Trends Analysis.

Intentionally injects the Key Test Cases required by the HCL Tech specification:
1. Duplicate tracks (exact duplicates & near-duplicates by track_name + artist_name)
2. Missing & malformed release dates
3. Outlier popularity values (< 0, > 100)
"""

from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)

ARTISTS = [
    # (artist_name, primary_genre, tier, country_region, base_stream_m)
    ("Taylor Swift", "Pop", "Superstar", "North America", 95),
    ("The Weeknd", "R&B", "Superstar", "North America", 88),
    ("Drake", "Hip-Hop", "Superstar", "North America", 84),
    ("Bad Bunny", "Latin", "Superstar", "Latin America", 80),
    ("Ed Sheeran", "Pop", "Superstar", "Europe", 75),
    ("Dua Lipa", "Pop", "Superstar", "Europe", 68),
    ("Billie Eilish", "Indie/Alt", "Superstar", "North America", 66),
    ("Kendrick Lamar", "Hip-Hop", "Superstar", "North America", 64),
    ("Ariana Grande", "Pop", "Superstar", "North America", 62),
    ("BTS", "K-Pop", "Superstar", "Asia", 60),
    ("Post Malone", "Hip-Hop", "Mainstream", "North America", 52),
    ("SZA", "R&B", "Mainstream", "North America", 50),
    ("Olivia Rodrigo", "Pop", "Mainstream", "North America", 48),
    ("Travis Scott", "Hip-Hop", "Mainstream", "North America", 46),
    ("Coldplay", "Rock", "Superstar", "Europe", 55),
    ("Imagine Dragons", "Rock", "Mainstream", "North America", 44),
    ("Calvin Harris", "Electronic/Dance", "Mainstream", "Europe", 42),
    ("David Guetta", "Electronic/Dance", "Mainstream", "Europe", 40),
    ("Burna Boy", "Afrobeats", "Mainstream", "Africa", 38),
    ("Rema", "Afrobeats", "Mainstream", "Africa", 36),
    ("Karol G", "Latin", "Mainstream", "Latin America", 43),
    ("BLACKPINK", "K-Pop", "Mainstream", "Asia", 45),
    ("Morgan Wallen", "Country", "Mainstream", "North America", 39),
    ("Luke Combs", "Country", "Mainstream", "North America", 35),
    ("Arctic Monkeys", "Rock", "Mainstream", "Europe", 37),
    ("Tame Impala", "Indie/Alt", "Emerging", "Oceania", 24),
    ("Fred again..", "Electronic/Dance", "Emerging", "Europe", 26),
    ("Sabrina Carpenter", "Pop", "Mainstream", "North America", 41),
    ("Tyla", "Afrobeats", "Emerging", "Africa", 28),
    ("Peso Pluma", "Latin", "Emerging", "Latin America", 31),
    ("Zach Bryan", "Country", "Emerging", "North America", 27),
    ("Hozier", "Indie/Alt", "Emerging", "Europe", 29),
    ("NewJeans", "K-Pop", "Emerging", "Asia", 33),
    ("Vance Joy", "Indie/Alt", "Indie", "Oceania", 15),
    ("Phoebe Bridgers", "Indie/Alt", "Indie", "North America", 16),
]

GENRE_PROFILES = {
    # genre: (dance, energy, valence, tempo, loudness, acoustic, instrum, speech, dur_sec, category)
    "Pop":              (0.68, 0.67, 0.56, 118, -5.6, 0.18, 0.02, 0.07, 198, "Mainstream"),
    "Hip-Hop":          (0.76, 0.66, 0.48, 122, -6.2, 0.12, 0.01, 0.22, 192, "Urban"),
    "R&B":              (0.65, 0.54, 0.44, 106, -7.1, 0.28, 0.03, 0.10, 206, "Urban"),
    "Electronic/Dance": (0.74, 0.82, 0.52, 126, -5.1, 0.06, 0.18, 0.06, 195, "Electronic"),
    "Rock":             (0.50, 0.78, 0.49, 128, -5.8, 0.14, 0.09, 0.05, 228, "Band/Guitar"),
    "Latin":            (0.78, 0.74, 0.69, 112, -5.3, 0.21, 0.01, 0.11, 200, "Global"),
    "Indie/Alt":        (0.55, 0.56, 0.43, 114, -7.8, 0.39, 0.12, 0.04, 222, "Alternative"),
    "Country":          (0.58, 0.63, 0.59, 116, -6.4, 0.34, 0.01, 0.04, 204, "Roots"),
    "K-Pop":            (0.73, 0.79, 0.63, 121, -4.8, 0.10, 0.01, 0.09, 190, "Global"),
    "Afrobeats":        (0.79, 0.71, 0.67, 108, -6.0, 0.24, 0.02, 0.12, 194, "Global"),
}

ADJECTIVES = [
    "Midnight", "Golden", "Electric", "Neon", "Velvet", "Broken", "Summer", "Endless",
    "Silver", "Wild", "Silent", "Crimson", "Starlight", "Ocean", "Shadow", "Crystal",
    "Lost", "After", "Sweet", "Burning", "Fading", "Lunar", "Gravity", "Echoes"
]
NOUNS = [
    "Dreams", "Nights", "Heart", "Horizon", "Lights", "Memories", "Fever", "Rain",
    "Waves", "Fire", "Shadows", "Rhythm", "Sky", "Road", "Love", "Pulse",
    "Mirage", "Soul", "Crown", "Time", "Escape", "Mirrors", "Vibe", "Stars"
]


def clip01(val: float) -> float:
    return float(np.clip(val, 0.01, 0.99))


def main() -> None:
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)

    n_base = 2500
    rows = []
    used_titles = set()

    for i in range(1, n_base + 1):
        artist_name, genre, tier, region, base_stream_m = ARTISTS[
            rng.choice(len(ARTISTS), p=np.array([a[4] for a in ARTISTS]) / sum(a[4] for a in ARTISTS))
        ]
        prof = GENRE_PROFILES[genre]
        year = int(rng.integers(2015, 2026))
        month = int(rng.integers(1, 13))
        day = int(rng.integers(1, 29))
        release_date = f"{year:04d}-{month:02d}-{day:02d}"

        # Subtle yearly evolution trends (2015 -> 2025):
        # higher danceability, shorter duration, slightly lower acousticness
        year_offset = year - 2015
        danceability = clip01(prof[0] + 0.005 * year_offset + rng.normal(0, 0.09))
        energy = clip01(prof[1] + 0.002 * year_offset + rng.normal(0, 0.10))
        valence = clip01(prof[2] - 0.002 * year_offset + rng.normal(0, 0.13))
        tempo = float(np.clip(prof[3] + rng.normal(0, 14), 65, 195))
        loudness = float(np.clip(prof[4] + 0.08 * year_offset + rng.normal(0, 1.8), -18.0, -1.5))
        acousticness = clip01(prof[5] - 0.004 * year_offset + rng.normal(0, 0.11))
        instrumentalness = float(np.clip(prof[6] + rng.exponential(0.03), 0.0, 0.95))
        speechiness = clip01(prof[7] + 0.002 * year_offset + rng.normal(0, 0.04))
        duration_ms = int(np.clip((prof[8] - 2.2 * year_offset + rng.normal(0, 22)) * 1000, 95000, 380000))

        # Popularity driven meaningfully by danceability, loudness, energy, and artist tier
        tier_boost = {"Superstar": 18, "Mainstream": 11, "Emerging": 5, "Indie": 0}[tier]
        pop_raw = (
            40
            + tier_boost
            + 18 * (danceability - 0.5)
            + 12 * (energy - 0.5)
            + 1.6 * (loudness + 6.5)
            - 14 * (acousticness - 0.2)
            - 10 * instrumentalness
            + 0.4 * year_offset
            + rng.normal(0, 8.5)
        )
        popularity = round(float(np.clip(pop_raw, 8, 99)), 1)

        # Streams scale exponentially with popularity + artist base draw
        stream_mult = np.exp((popularity - 55) / 14.0) * rng.lognormal(0, 0.45)
        streams = int(max(50_000, base_stream_m * 1_000_000 * 0.18 * stream_mult))

        # Unique track title
        while True:
            title = f"{rng.choice(ADJECTIVES)} {rng.choice(NOUNS)}"
            if rng.random() < 0.25:
                title += f" (Pt. {int(rng.integers(1, 5))})"
            key = (title, artist_name)
            if key not in used_titles:
                used_titles.add(key)
                break

        explicit = "Y" if (genre in ("Hip-Hop", "Latin", "R&B") and rng.random() < 0.62) or rng.random() < 0.18 else "N"

        rows.append({
            "track_id": f"TRK{i:05d}",
            "track_name": title,
            "artist_name": artist_name,
            "artist_tier": tier,
            "country_region": region,
            "genre": genre,
            "genre_category": prof[9],
            "release_date": release_date,
            "streams": streams,
            "popularity": popularity,
            "explicit_flag": explicit,
            "duration_ms": duration_ms,
            "danceability": round(danceability, 4),
            "energy": round(energy, 4),
            "valence": round(valence, 4),
            "tempo_bpm": round(tempo, 2),
            "loudness_db": round(loudness, 2),
            "acousticness": round(acousticness, 4),
            "instrumentalness": round(instrumentalness, 4),
            "liveness": round(clip01(0.16 + rng.normal(0, 0.08)), 4),
            "speechiness": round(speechiness, 4),
        })

    df = pd.DataFrame(rows)

    # --- Inject Key Test Case 1: Duplicate tracks ---
    # 45 exact duplicates
    exact_dups = df.sample(n=45, random_state=SEED).copy()
    # 30 near-duplicates (same track_name + artist_name, different track_id)
    near_dups = df.sample(n=30, random_state=SEED + 1).copy()
    near_dups["track_id"] = [f"TRKDUP{j:03d}" for j in range(1, 31)]
    near_dups["streams"] = (near_dups["streams"] * 0.92).astype(int)

    df_raw = pd.concat([df, exact_dups, near_dups], ignore_index=True)

    # --- Inject Key Test Case 2: Missing & malformed release dates ---
    missing_date_idx = rng.choice(df_raw.index, size=55, replace=False)
    df_raw.loc[missing_date_idx, "release_date"] = np.nan

    remaining_idx = df_raw.index.difference(missing_date_idx)
    malformed_idx = rng.choice(remaining_idx, size=15, replace=False)
    bad_dates = ["2022-13-45", "unknown", "2021/02/30", "N/A", "2020-00-10"]
    df_raw.loc[malformed_idx, "release_date"] = [bad_dates[k % len(bad_dates)] for k in range(15)]

    # --- Inject Key Test Case 3: Outlier popularity ---
    pop_outlier_idx = rng.choice(df_raw.index, size=25, replace=False)
    outlier_vals = [-12.0, -5.0, -1.0, 105.0, 118.0, 135.0, 250.0, 999.0]
    df_raw.loc[pop_outlier_idx, "popularity"] = [outlier_vals[k % len(outlier_vals)] for k in range(25)]

    # Shuffle rows
    df_raw = df_raw.sample(frac=1.0, random_state=SEED).reset_index(drop=True)

    out_path = out_dir / "spotify_tracks_raw.csv"
    df_raw.to_csv(out_path, index=False)
    print(f"Generated {len(df_raw)} raw rows -> {out_path}")


if __name__ == "__main__":
    main()
