import pandas as pd

from data_generator import generate_fake_data
from data_cleaning_pipeline import clean_data
from kpi_calculation import calculate_kpis
from store_kpis_mysql import insert_kpis
from store_logs_mongo import insert_log


def run_pipeline():
    print("🚀 Pipeline started...")

    # 1️⃣ Fetch / Generate data
    df_raw = generate_fake_data(rows=12000)

    # 2️⃣ Clean data
    df_clean = clean_data(df_raw)

    # 3️⃣ Calculate KPIs
    kpi_df = calculate_kpis(df_clean)

    # 4️⃣ Store KPIs in MySQL
    insert_kpis(kpi_df)

    # 5️⃣ Log success in MongoDB
    insert_log(
        records_processed=len(kpi_df),
        source_file="generated_operational_data",
        notes="Automated reporting pipeline executed successfully"
    )

    print("✅ Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()
