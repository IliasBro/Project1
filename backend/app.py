from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import pickle
import pandas as pd
import datetime
import os


app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)


# Connect to Azure Cosmos DB for MongoDB
# Replace the connection string below with your Cosmos DB connection string.
connection_string = os.environ.get("MONGODB_URI")
if not connection_string:
    raise ValueError("MONGODB_URI not set in environment variables")

client = MongoClient(connection_string)
db = client["hdp2"]
predictions_collection = db["predictions"]

def compute_probability(name: str, gender: str) -> float:
    name_clean = name.strip().lower()
    gender_clean = gender.strip().lower()

    # Suche alle Einträge mit diesem Namen & Geschlecht
    results = list(db["scraped_data"].find({
        "name": {"$regex": f"^{name_clean}$", "$options": "i"},
        "gender": {"$regex": f"^{gender_clean}$", "$options": "i"}
    }))

    if not results:
        return 0.05  # Name nicht vorhanden

    # Suche das zuletzt vorkommende Jahr + besten Rang
    most_recent = max(results, key=lambda x: int(x["year"]))
    best_rank = min(int(r["rank"]) for r in results)

    # Ermittele MIN_YEAR, MAX_YEAR und MAX_RANK dynamisch aus der DB
    years = [int(r["year"]) for r in db["scraped_data"].find()]
    ranks = [int(r["rank"]) for r in db["scraped_data"].find()]
    MIN_YEAR = min(years)
    MAX_YEAR = max(years)
    MAX_RANK = max(ranks)

    year_score = (int(most_recent["year"]) - MIN_YEAR) / (MAX_YEAR - MIN_YEAR)
    rank_score = (MAX_RANK - best_rank) / (MAX_RANK - 1)
    combined = (year_score + rank_score) / 2
    return round(0.05 + combined * 0.90, 2)


@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/predict", methods=["GET"])
def predict():
    name = request.args.get("name", "").strip()
    gender = request.args.get("gender", "female").strip()
    if not name:
        return jsonify({"error": "Missing name parameter"}), 400

    prob = compute_probability(name, gender)
    predictions_collection.insert_one({
        "name": name,
        "gender": gender,
        "probability_top50_2027": prob,
        "timestamp": datetime.datetime.utcnow()
    })

    return jsonify({
        "name": name,
        "gender": gender,
        "probability_top50_2027": prob
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
