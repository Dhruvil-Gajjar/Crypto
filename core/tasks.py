import os
import time
import requests
import holidays

import pandas as pd
from fbprophet import Prophet
from celery import shared_task
from datetime import date, timedelta, datetime
from django.conf import settings

from core.models import *
from core.utils import calculatingError
from project.celery import app


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


@app.task()
def predGoldPrice(df, file_name):
    X_train = df.iloc[:]
    X_train.tail()

    holiday = pd.DataFrame([])
    for date, name in sorted(holidays.UnitedStates(years=[2015, 2016, 2017, 2018, 2019, 2020, 2021]).items()):
        holiday = holiday.append(pd.DataFrame({'ds': date, 'holiday': "US-Holidays"}, index=[0]), ignore_index=True)
    holiday['ds'] = pd.to_datetime(holiday['ds'], format='%Y-%m-%d', errors='ignore')
    model = Prophet(daily_seasonality=True,
                    holidays=holiday,
                    seasonality_mode=('additive'),
                    changepoint_prior_scale=0.5,
                    n_changepoints=100,
                    holidays_prior_scale=0.5
                    )

    model.fit(X_train, algorithm='Newton')
    future = model.make_future_dataframe(periods=30, freq="D")
    forecast = model.predict(future)
    forecast.tail(10)
    fig1 = model.plot(forecast)
    forecast.to_csv('output_file.csv')
    fig = model.plot_components(forecast)
    list(forecast)
    df_output = pd.read_csv('output_file.csv')
    calculatingError(df_output, df, file_name)


@shared_task
def data_prediction_process():
    model = file_name = None
    for model_name in models:
        if "Euro" in model_name:
            model = Euro
            file_name = "euro"
        elif "GBP" in model_name:
            model = GBP
            file_name = "gbp"
        elif "CNY" in model_name:
            model = CNY
            file_name = "cny"
        elif "JPY" in model_name:
            model = JPY
            file_name = "jpy"
        elif "Gold" in model_name:
            model = Gold
            file_name = "gold"

        # Remove old file
        file_path = os.path.join(settings.ML_DIRECTORY_PATH, f'final_predicted_{file_name}.csv')
        if os.path.isfile(file_path):
            os.remove(file_path)

        # Process data
        pd_list = []
        obj = model.objects.filter(predicted_price=None).order_by('dateTimeStamp').first()
        pd_list.append({
            'Date': obj.dateTimeStamp.strftime('%Y-%m-%d'),
            'Price': float(str(obj.price).replace(",", ""))
        })

        df = pd.DataFrame(pd_list)
        df.columns = ['ds', 'y']
        predGoldPrice.delay(df, file_name)
        time.sleep(600)


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

    # file_path = os.path.join(settings.ML_DIRECTORY_PATH, 'final_predicted_gold.csv')
    # if os.path.isfile(file_path):
    #     os.remove(file_path)
    # pd_list = []
    # obj = Gold.objects.filter(predicted_price=None).order_by('dateTimeStamp').first()
    # pd_list.append({
    #     'Date': obj.dateTimeStamp.strftime('%Y-%m-%d'),
    #     'Price': float(str(obj.price).replace(",", ""))
    # })
    #
    # df = pd.DataFrame(pd_list)
    # df.columns = ['ds', 'y']
    # predGoldPrice(df)
    # print(df)
    # df = pd.DataFrame(list())

# from core.tasks import ingest_price_data
# from core.tasks import delete_tables_data
# from core.tasks import test_data

