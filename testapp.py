import pandas as pd
features = pd.read_csv("scraped_data.csv")  # or load your pickled features
print(features["name"].unique()[:20])
