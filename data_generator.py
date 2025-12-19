import pandas as pd
import random
from datetime import datetime, timedelta


def generate_fake_data(rows=12000):
    EMPLOYEES = [f"EMP{100+i}" for i in range(1, 51)]
    START_DATE = datetime(2024, 1, 1)

    data = []

    for _ in range(rows):
        employee_id = random.choice(EMPLOYEES)
        date = START_DATE + timedelta(days=random.randint(0, 180))
        calls_handled = random.randint(25, 60)
        avg_call_time = round(random.uniform(4.0, 8.5), 2)
        escalation_count = random.randint(0, 6)
        resolution_status = (
            "Escalated" if escalation_count >= 3 else "Resolved"
        )

        data.append([
            employee_id,
            date.strftime("%Y-%m-%d"),
            calls_handled,
            avg_call_time,
            escalation_count,
            resolution_status
        ])

    df = pd.DataFrame(data, columns=[
        "employee_id",
        "date",
        "calls_handled",
        "avg_call_time",
        "escalation_count",
        "resolution_status"
    ])

    return df
