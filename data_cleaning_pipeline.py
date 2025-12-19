import pandas as pd


def clean_data(df):
    # 1️⃣ Remove duplicate records
    df.drop_duplicates(inplace=True)

    # 2️⃣ Handle missing values
    df.dropna(subset=[
        'employee_id',
        'date',
        'calls_handled',
        'avg_call_time'
    ], inplace=True)

    # 3️⃣ Date parsing & validation
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df[df['date'].notnull()]

    # 4️⃣ Data type enforcement
    df['calls_handled'] = df['calls_handled'].astype(int)
    df['escalation_count'] = df['escalation_count'].astype(int)
    df['avg_call_time'] = df['avg_call_time'].astype(float)

    # 5️⃣ Business rule validation
    df = df[df['calls_handled'] >= 0]
    df = df[df['avg_call_time'].between(3.0, 10.0)]
    df = df[df['escalation_count'] >= 0]

    # 6️⃣ Normalize resolution status
    df['resolution_status'] = df['resolution_status'].str.capitalize()

    return df
