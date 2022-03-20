import os
import requests

import pandas as pd
from celery import shared_task
from datetime import date, timedelta, datetime
from django.conf import settings

from core.models import *
from core.utils import predGoldPrice

FIXER_BASE_URL = settings.FIXER_BASE_URL
FIXER_ACCESS_KEY = settings.FIXER_ACCESS_KEY

models = ["Euro", "GBP", "CNY", "JPY", "Gold"]


def get_missing_dates(dateTimeStamp):
    try:
        today = date.today()
        difference = pd.date_range(start=dateTimeStamp.strftime("%Y-%m-%d"), end=str(today))
        missing_dates = []
        for i in difference.values:
            missing_dates.append(str(i))
        if len(missing_dates) > 0:
            return missing_dates[1:]
        else:
            return None
    except:
        return None


def get_price_from_fixer(symbol, missing_date=None):
    try:
        if not missing_date:
            url = FIXER_BASE_URL + "latest?access_key=" + FIXER_ACCESS_KEY + "&base=USD&symbols=" + symbol
        else:
            url = FIXER_BASE_URL + missing_date + "?access_key=" + FIXER_ACCESS_KEY + "&base=USD&symbols=" + symbol

        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["rates"][symbol]
    except Exception as e:
        print(e)
        return None


def prepare_date(date):
    datetime_object = datetime.strptime(str(date).strip(), '%Y-%m-%d')
    return datetime_object


@shared_task
def ingest_price_data():
    today = date.today()
    yesterday = today - timedelta(days=1)

    model = symbol = None
    try:
        for model_name in models:
            if "Euro" in model_name:
                model = Euro
                symbol = "EUR"
            elif "GBP" in model_name:
                model = GBP
                symbol = "GBP"
            elif "CNY" in model_name:
                model = CNY
                symbol = "CNY"
            elif "JPY" in model_name:
                model = JPY
                symbol = "JPY"
            elif "Gold" in model_name:
                model = Gold
                symbol = "XAU"

            if model:
                print('#### >>>>>>>>>>>>>>>>>>>>>>>> Starting to importing %s data' % symbol)

                dateTime_obj = model.objects.all().order_by('-dateTimeStamp').first().dateTimeStamp
                last_date = str(dateTime_obj).split(" ")[0].strip()

                if str(yesterday) != last_date and str(today) != last_date:
                    missing_dates_list = get_missing_dates(dateTime_obj)
                    for missing_date in missing_dates_list:
                        missed_date = str(missing_date).split("T")[0].strip()
                        price = get_price_from_fixer(symbol=symbol, missing_date=missed_date)
                        if price:
                            model.objects.create(
                                price=price,
                                dateTimeStamp=prepare_date(missed_date)
                            )
                else:
                    if str(today) != last_date:
                        price = get_price_from_fixer(symbol=symbol)
                        if price:
                            model.objects.create(
                                price=price,
                                dateTimeStamp=datetime.now()
                            )

        print('#### >>>>>>>>>>>>>>>>>>>>>>>> Ingesting data completed')
    except Exception as e:
        print(e)


def delete_tables_data():
    model = None
    for model_name in models:
        if "Euro" in model_name:
            model = Euro
        elif "GBP" in model_name:
            model = GBP
        elif "CNY" in model_name:
            model = CNY
        elif "JPY" in model_name:
            model = JPY
        elif "Gold" in model_name:
            model = Gold

        # model.objects.all().delete()
        # a = model.objects.all().order_by('-dateTimeStamp').first().delete()


# def test_data():
    # final_csv = settings.BASE_DIR + "/" + 'final_predicted.csv'
    # print(final_csv)
    # pd_list = []
    # queryset = Gold.objects.filter(predicted_price=None).order_by('dateTimeStamp')
    # for obj in queryset:
    #     pd_list.append({
    #         'Date': obj.dateTimeStamp.strftime('%Y-%m-%d'),
    #         'Price': float(str(obj.price).replace(",", ""))
    #     })
    #
    # df = pd.DataFrame(pd_list)
    # df.columns = ['ds', 'y']
    # predGoldPrice(df)
    # print(df)
    # df = pd.DataFrame(list())

# from core.tasks import ingest_price_data
# from core.tasks import delete_tables_data
# from core.tasks import test_data

# df = pd.read_csv('gold_data_sept.csv')
# df.columns=['ds','y']
# predGoldPrice(df)
