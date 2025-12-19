import mysql.connector
import pandas as pd
from store_logs_mongo import insert_log

# 1️⃣ Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lalit@282002",
    database="reporting_db"
)
cursor = conn.cursor()

# 2️⃣ Sample KPI DataFrame
kpi_df = pd.DataFrame({
    'employee_id': ['EMP101', 'EMP102', 'EMP103'],
    'date': ['2025-12-19', '2025-12-19', '2025-12-19'],
    'calls_handled': [45, 38, 50],
    'avg_call_time': [5.2, 6.1, 4.8],
    'escalation_count': [2, 3, 1],
    'resolution_status': ['Resolved', 'Resolved', 'Escalated']
})

kpi_df['date'] = pd.to_datetime(kpi_df['date'])

# 3️⃣ Insert function
def insert_kpis(df):
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO employee_kpis
            (employee_id, date, calls_handled, avg_call_time, escalation_count, resolution_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            row['employee_id'],
            row['date'],
            int(row['calls_handled']),
            float(row['avg_call_time']),
            int(row['escalation_count']),
            row['resolution_status']
        ))
    conn.commit()
    print("✅ Data inserted into MySQL")

# ✅ CALL IT (THIS WAS MISSING)
insert_kpis(kpi_df)

# 4️⃣ Log into MongoDB
insert_log(
    records_processed=len(kpi_df),
    source_file="operational_metrics_sample.csv",
    notes="Data cleaned, KPIs calculated, inserted into MySQL"
)
