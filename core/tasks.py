import pandas as pd
from datetime import date
from celery import shared_task

from core.models import *

models = ["Euro", "GBP", "CNY", "JPY", "GBP"]


def get_missing_dates(dateTimeStamp):
    try:
        today = date.today()
        difference = pd.date_range(start=dateTimeStamp.strftime("%Y-%m-%d"), end=str(today))
        missing_dates = []
        for i in difference.values:
            missing_dates.append(str(i))
        if len(missing_dates) > 0:
            return missing_dates[1:-1]
        else:
            return None
    except:
        return None


def get_model_missing_date(model_name):
    from_date = model_name.objects.all().order_by('-created_at').first().dateTimeStamp
    return from_date


@shared_task
def import_data_from_fixer():
    for model_name in models:
        model = None
        if "Euro" in model_name:
            model = Euro
        elif "GBP" in model_name:
            model = GBP
        elif "Gold" in model_name:
            model = Gold
        elif "CNY" in model_name:
            model = CNY
        elif "JPY" in model_name:
            model = JPY

        url = "http://data.fixer.io/api/latest?access_key=e9b8fceb2ddfa5591cdf6e7e9f9d8382&base=USD&symbols=GBP,AUD,CAD,PLN,MXN"