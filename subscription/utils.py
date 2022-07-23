from datetime import datetime, timedelta


def get_date_N_days_after(days):
    date_N_days_fter = datetime.now() + timedelta(days=days)
    return int(round(date_N_days_fter.timestamp()))
