import pandas as pd


def calculate_kpis(df):
    """
    Calculates basic KPIs for reporting
    """

    # Example KPI logic (simple + interview safe)
    df['performance_flag'] = df['calls_handled'].apply(
        lambda x: 'High' if x >= 45 else 'Normal'
    )

    return df
