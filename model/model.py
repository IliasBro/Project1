import pandas as pd
import numpy as np
import pickle

def load_dataset(file_path):
    """Load the scraped CSV data."""
    return pd.read_csv(file_path)

def process_name_features(group):
    """
    For a given (name, gender) group, compute:
      - most_recent_year: maximum of the 'year' column
      - best_ranking: minimum (i.e. best) of the 'rank' column
    """
    # Ensure proper numeric conversion
    group["year"] = group["year"].astype(int)
    group["rank"] = group["rank"].astype(int)
    return pd.Series({
        "most_recent_year": group["year"].max(),
        "best_ranking": group["rank"].min()
    })

def main():
    # Load the scraped dataset (ensure 'scraped_data.csv' is in your project root)
    df = load_dataset("scraped_data.csv")
    
    # Group by name and gender to compute features per unique name
    features = df.groupby(["name", "gender"]).apply(process_name_features).reset_index()
    
    # Determine global constants from the entire dataset
    MIN_YEAR = df["year"].astype(int).min()
    MAX_YEAR = df["year"].astype(int).max()
    MAX_RANK = df["rank"].astype(int).max()
    
    # Create the payload to pickle
    payload = {
        "features": features,
        "MIN_YEAR": MIN_YEAR,
        "MAX_YEAR": MAX_YEAR,
        "MAX_RANK": MAX_RANK
    }
    
    # Save the payload into a pickle file (model.plk)
    with open("model/model.plk", "wb") as f:
        pickle.dump(payload, f)
    
    print("Model saved successfully!")
    
if __name__ == "__main__":
    main()
