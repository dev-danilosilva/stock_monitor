from typing import List
from datetime import date, timedelta


def get_last_n_days(n: int) -> List[date]:
    last_7_days = []
    today = date.today()
    for delta_time in range(1, 8    ):
        last_7_days.append(today - timedelta(days=delta_time))
    return last_7_days
