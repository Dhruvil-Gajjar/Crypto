from datetime import datetime, timedelta, timezone
from users.models import User


def get_date_N_days_after(days):
    date_N_days_fter = datetime.now() + timedelta(days=days)
    return int(round(date_N_days_fter.timestamp()))


def calculate_diff_in_days(user_email):
    now = datetime.now().replace(tzinfo=timezone.utc)
    date_joined = User.objects.filter(email=user_email).first().date_joined
    diff = now - date_joined
    return diff.days
