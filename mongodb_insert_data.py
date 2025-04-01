import csv
from pymongo import MongoClient

#Deine Azure Cosmos DB MongoDB-Verbindungszeichenfolge:
connection_string = "mongodb+srv://hdp2:ABcd1234@hdp2.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"

#Mit Azure verbinden
client = MongoClient(connection_string)
db = client["hdp2"]  # Muss mit deinem Azure-Datenbanknamen übereinstimmen
collection = db["scraped_data"]  # Neue Collection für Rohdaten

#CSV-Datei laden
csv_file = "scraped_data.csv"

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    records = list(reader)
    for record in records:
        try:
            record["rank"] = int(record["rank"])
            record["year"] = int(record["year"])
        except Exception:
            record["rank"] = None
            record["year"] = None

#In MongoDB einfügen
if records:
    collection.delete_many({})  # Optional: Vorher leeren
    result = collection.insert_many(records)
    print(f"Inserted {len(result.inserted_ids)} records into Azure MongoDB.")
else:
    print("No records found in CSV.")
