import os
import csv
import requests

import pandas as pd
from celery import shared_task
from datetime import date, timedelta, datetime
from django.conf import settings

from core.models import *
from core.utils import predGoldPrice
from project.celery import app
from users.tasks import send_subscription_reminder

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
    except Exception as e:
        print(f"get_missing_dates Error ====> {e}")
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
        print(f"get_price_from_fixer Error ====> {e}")
        return None


def prepare_date(date):
    datetime_object = datetime.strptime(str(date).strip(), '%Y-%m-%d')
    return datetime_object


@shared_task
def ingest_price_data():
    today = date.today()
    yesterday = today - timedelta(days=1)

    model, symbol = None, None
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
                print(f"ingest_price_data Info ====> Started importing {symbol} data")

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

        print(f"ingest_price_data Info ====> Ingesting data completed")
    except Exception as e:
        print(f"ingest_price_data Error ====> {e}")


@app.task()
def ingest_predicted_data():
    try:
        print(f"ingest_predicted_data Info ====> Starting to ingest predicted!")

        file_list = ["euro", "gbp", "cny", "jpy", "gold"]
        for file_name in file_list:
            file_path = os.path.join(settings.ML_DIRECTORY_PATH, f'final_predicted_{file_name}.csv')
            if os.path.isfile(file_path):
                # Delete if data exists
                PredictionData.objects.filter(commodity=str(file_name)).all().delete()

                with open(file_path) as f:
                    reader = csv.reader(f)
                    # skip header
                    next(reader)

                    for row in reader:
                        PredictionData.objects.create(
                            price=str(row[4]).strip(),
                            dateTimeStamp=prepare_date(row[1]),
                            commodity=str(file_name)
                        )

        print(f"ingest_predicted_data Info ====> Successfully ingested prediction data!")
    except Exception as e:
        print(f"ingest_predicted_data Error ====> {e}")
        pass

    send_subscription_reminder.delay()


@shared_task
def data_prediction_process():
    print(f"data_prediction_process Info ====> Starting to process data for commodities!")

    model, file_name, processed_model = None, None, []
    for model_name in models:
        if "Euro" in model_name and "Euro" not in processed_model:
            model = Euro
            file_name = "euro"
        elif "GBP" in model_name and "GBP" not in processed_model:
            model = GBP
            file_name = "gbp"
        elif "CNY" in model_name and "CNY" not in processed_model:
            model = CNY
            file_name = "cny"
        elif "JPY" in model_name and "JPY" not in processed_model:
            model = JPY
            file_name = "jpy"
        elif "Gold" in model_name and "Gold" not in processed_model:
            model = Gold
            file_name = "gold"
        else:
            break

        if str(model) not in processed_model:
            processed_model.append(str(model))

            # Remove old files
            op_file = os.path.join(settings.ML_DIRECTORY_PATH, 'output_file.csv')
            if os.path.isfile(op_file):
                os.remove(op_file)

            op_calculated = os.path.join(settings.ML_DIRECTORY_PATH, 'output_file_calculated.csv')
            if os.path.isfile(op_calculated):
                os.remove(op_calculated)

            final_csv_path = os.path.join(settings.ML_DIRECTORY_PATH, f'final_predicted_{file_name}.csv')
            if os.path.isfile(final_csv_path):
                os.remove(final_csv_path)

            print(f"data_prediction_process Info ====> Preparing dataframe for {str(model)}")

            # Process data
            pd_list = []
            model_queryset = model.objects.all().order_by('dateTimeStamp')
            for obj in model_queryset:
                if obj.dateTimeStamp and obj.price:
                    pd_list.append({
                        'Date': obj.dateTimeStamp.strftime('%Y-%m-%d'),
                        'Price': float(str(obj.price).replace(",", ""))
                    })

            df = pd.DataFrame(pd_list)
            df.columns = ['ds', 'y']

            print(f"data_prediction_process Info ====> Starting to process data for {str(model)}")

            process_next = predGoldPrice(df, file_name)
            if process_next:
                last_obj = model_queryset.last()
                last_obj.is_data_processed = True
                last_obj.save()
                continue
        else:
            break

    print(f"data_prediction_process Info ====> Process data completed for {str(datetime.today())}")
    ingest_predicted_data.delay()


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


def process_initial_data():
    data_prediction_process.delay()
