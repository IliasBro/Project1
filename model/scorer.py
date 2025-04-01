import pandas as pd

# Load once at startup
df = pd.read_csv("scraped_data.csv")
df["year"] = df["year"].astype(int)
MAX_RANK = df["rank"].max()   # e.g. 1200
MIN_YEAR = df["year"].min()   # 1890
MAX_YEAR = df["year"].max()   # 2026

def compute_probability(name: str, gender: str) -> float:
    name, gender = name.strip().lower(), gender.strip().lower()

    subset = df[
        (df["name"].str.lower() == name) &
        (df["gender"].str.lower() == gender)
    ]
    # Not found → default 5%
    if subset.empty:
        return 0.05

    last = subset.sort_values("year").iloc[-1]
    last_year, last_rank = last.year, last.rank

    # Normalize year into [0,1]
    year_score = (last_year - MIN_YEAR) / (MAX_YEAR - MIN_YEAR)
    # Normalize rank into [0,1] (higher rank = lower score)
    rank_score = (MAX_RANK - last_rank) / (MAX_RANK - 1)

    combined = (year_score + rank_score) / 2
    return round(0.05 + combined * 0.90, 2)
