import pandas as pd
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["logs_db"]
logs_collection = db["processing_logs"]

# Function to insert log
def insert_log(records_processed, source_file, notes=""):
    log = {
        "timestamp": pd.Timestamp.now(),
        "records_processed": records_processed,
        "source_file": source_file,
        "notes": notes
    }
    logs_collection.insert_one(log)
    print("✅ Log inserted into MongoDB")

insert_log(
    records_processed=12000,  # ya len(kpi_df) agar pipeline me hai
    source_file="operational_metrics_sample.csv",
    notes="Data cleaned, KPIs calculated, inserted into MySQL"
)