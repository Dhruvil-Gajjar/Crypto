import os
import csv
import holidays

import pandas as pd
import plotly.offline as py
from fbprophet import Prophet
import matplotlib.pyplot as plt
from fbprophet.plot import plot_plotly
from django.conf import settings

from datetime import datetime
from core.models import *


chart_models = ["gold", "euro", "jpy", "gbp", "cny"]


gold_obj = Gold.objects.all().order_by('-dateTimeStamp').first()
euro_obj = Euro.objects.all().order_by('-dateTimeStamp').first()
jpy_obj = JPY.objects.all().order_by('-dateTimeStamp').first()
cny_obj = CNY.objects.all().order_by('-dateTimeStamp').first()
gbp_obj = GBP.objects.all().order_by('-dateTimeStamp').first()


def get_price(value):
    if "," in str(value):
        new_value = str(value).replace(",", "")
        return new_value

    return value


def get_values_list(model_name):
    queryset = model_name.objects.all().order_by('-dateTimeStamp')
    values_list = []
    for obj in queryset[:2]:
        values_list.append(obj.price)

    new_value = values_list[0]
    old_value = values_list[1]

    if "," in str(new_value):
        new_value = str(new_value).replace(",", "")
    if "," in str(old_value):
        old_value = str(old_value).replace(",", "")

    return new_value, old_value


def calculate_difference(model_name):
    new_value, old_value = get_values_list(model_name)

    difference = float(new_value) - float(old_value)
    return float('%.3f' % difference)


def calculate_average(model_name):
    new_value, old_value = get_values_list(model_name)

    difference = float(new_value) - float(old_value)
    average = float(difference) / float(old_value)

    if average > float(old_value):
        final_average = "+" + str(float('%.3f' % average))
    else:
        final_average = str(float('%.3f' % average))

    return final_average


def get_cards_data():
    data = [
        {
            "commodity_name": "GOLD",
            "price": get_price(gold_obj.price) if gold_obj else 0,
            "difference": calculate_difference(Gold),
            "average": calculate_average(Gold),
            "commodity_img": "https://s2.coinmarketcap.com/static/img/coins/32x32/624.png"
        },
        {
            "commodity_name": "EURO",
            "price": get_price(euro_obj.price) if euro_obj else 0,
            "difference": calculate_difference(Euro),
            "average": calculate_average(Euro),
            "commodity_img": "https://s2.coinmarketcap.com/static/img/coins/32x32/2083.png"
        },
        {
            "commodity_name": "JPY",
            "price": get_price(jpy_obj.price) if jpy_obj else 0,
            "difference": calculate_difference(JPY),
            "average": calculate_average(JPY),
            "commodity_img": "https://s2.coinmarketcap.com/static/img/coins/32x32/2989.png"
        },
        {
            "commodity_name": "CNY",
            "price": get_price(cny_obj.price) if cny_obj else 0,
            "difference": calculate_difference(CNY),
            "average": calculate_average(CNY),
            "commodity_img": "https://s2.coinmarketcap.com/static/img/coins/32x32/3408.png"
        },
        {
            "commodity_name": "GBP",
            "price": get_price(gbp_obj.price) if gbp_obj else 0,
            "difference": calculate_difference(GBP),
            "average": calculate_average(GBP),
            "commodity_img": "https://s2.coinmarketcap.com/static/img/coins/32x32/6906.png"
        },
        {
            "commodity_name": "GYNERO",
            "price": get_price(gbp_obj.price) if gbp_obj else 0,
            "difference": calculate_difference(Euro),
            "average": calculate_average(Euro),
            "commodity_img": "https://s2.coinmarketcap.com/static/img/coins/32x32/624.png"
        }
    ]

    return data


def prepare_last_ten_days_data(model_name):
    queryset = model_name.objects.all().order_by('-dateTimeStamp')
    values_list = []
    for obj in queryset[:20]:
        values_list.append(float(str(obj.price).replace(",", "")))

    return values_list


def get_last_ten_days_chart():
    data = {
        "GOLD": prepare_last_ten_days_data(Gold),
        "EURO": prepare_last_ten_days_data(Euro),
        "JPY": prepare_last_ten_days_data(JPY),
        "CNY": prepare_last_ten_days_data(CNY),
        "GBP": prepare_last_ten_days_data(GBP),
        "GYNERO": prepare_last_ten_days_data(Euro),
    }

    return data


def get_timeStamp(dtObj):
    try:
        unix_time = datetime.timestamp(dtObj) * 1000
        return int(unix_time)
    except:
        return None


def get_sparkline():
    sparkline_dict = {
        "gold": [],
        "euro": [],
        "jpy": [],
        "gbp": [],
        "cny": [],
    }

    try:
        model = None
        predicted_queryset = PredictionData.objects.all()
        for model_name in chart_models:
            if "gold" in model_name:
                model = Gold
            elif "euro" in model_name:
                model = Euro
            elif "jpy" in model_name:
                model = JPY
            elif "gbp" in model_name:
                model = GBP
            elif "cny" in model_name:
                model = CNY

            pre_queryset = predicted_queryset.filter(commodity=model_name).order_by('-dateTimeStamp')
            model_queryset = model.objects.all().order_by('-dateTimeStamp')

            pre_obj = pre_queryset.last()
            mod_obj = model_queryset.first()

            if (pre_obj and mod_obj) or \
                    str(pre_obj.dateTimeStamp).split(" ")[0] == str(mod_obj.dateTimeStamp).split(" ")[0]:

                for obj in pre_queryset:
                    time_stamp = get_timeStamp(obj.dateTimeStamp)
                    if time_stamp:
                        sparkline_dict[model_name].append([time_stamp, float("{:.1f}".format(float(obj.price)))])

                del sparkline_dict[model_name][-1]

            for obj in model_queryset:
                time_stamp = get_timeStamp(obj.dateTimeStamp)
                if time_stamp:
                    sparkline_dict[model_name].append([time_stamp, float(str(obj.price).replace(",", ""))])

        sparkline_dict["gynero"] = sparkline_dict["euro"]
        return sparkline_dict
    except Exception as e:
        print(f"Error get_sparkline : \n{e}")
        return sparkline_dict


"""
    Data Processing Script
"""


def predGoldPrice(df, file_name):
    try:
        X_train = df.iloc[:]
        X_train.tail()

        holiday = pd.DataFrame([])
        for date, name in sorted(holidays.UnitedStates(years=[2015, 2016, 2017, 2018, 2019, 2020, 2021]).items()):
            holiday = holiday.append(pd.DataFrame({'ds': date, 'holiday': "US-Holidays"}, index=[0]), ignore_index=True)
        holiday['ds'] = pd.to_datetime(holiday['ds'], format='%Y-%m-%d', errors='ignore')
        model = Prophet(
            daily_seasonality=True,
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
        forecast.to_csv(os.path.join(settings.ML_DIRECTORY_PATH, 'output_file.csv'))
        fig = model.plot_components(forecast)
        list(forecast)
        op_file = os.path.join(settings.ML_DIRECTORY_PATH, 'output_file.csv')
        df_output = pd.read_csv(op_file)
        final_op = calculatingError(df_output, df, file_name)
        if final_op:
            return True
    except Exception as e:
        print(f"predGoldPrice Error ====> {e}")
        return True


def calculatingError(df_output, df, file_name):
    try:
        # assigning the output variable to array
        output_yhat = df_output.iloc[:, -1:].values

        # assigning the actual variable to array
        output_actual = df.iloc[:, -1:].values

        # Calculating Percent Error
        i = 0
        output_percent_error = []

        while i < len(output_actual):
            output_percent_error.append(100 - (1 * ((output_yhat[i] * 100) / output_actual[i])))
            i += 1

        # Calculating the Difference between actual and predicted
        i = 0
        output_difference = []
        while i < len(output_actual):
            output_difference.append(output_actual[i] - output_yhat[i])
            i += 1

        # Calculating the Integrated error
        i = 0
        output_integrated = []
        while i < len(output_percent_error):
            output_integrated.append(((output_yhat[i] * output_percent_error[i]) / 100) + output_yhat[i])
            i += 1

        # Assigning the percent error for 45 days
        re_output_yhat = output_yhat[-30:]
        re_output_yhat = pd.DataFrame(re_output_yhat).values

        # Assigning the below 45 days ds
        # pred_df=df.iloc[-47:-2,0]
        pred_df = pd.DataFrame(df.iloc[-47:-2, 0])

        # Assigning the percent error for 45 days
        pred_percent_error = output_percent_error[-47:-2]
        pred_percent_error = pd.DataFrame(pred_percent_error)

        # Combining the 45 days data
        df_combined = pred_df.copy()
        df_combined['y'] = pred_percent_error.values

        # Prediciting the 45 days record keeping percent error as output
        predError(df_combined)

        # Reading the generated dataset
        op_calculated = os.path.join(settings.ML_DIRECTORY_PATH, 'output_file_calculated.csv')
        df_error = pd.read_csv(op_calculated)

        # assigning the output variable to array
        re_output_ds = df_error.iloc[:, 1].values
        re_output_ds = pd.DataFrame(re_output_ds[-30:])
        re_output_ds.columns = ['ds']

        # assigning the output variable to array
        re_output_error_percent = df_error.iloc[:, -1:].values
        re_output_error_percent = re_output_error_percent[-30:]
        len(re_output_error_percent)

        # Calculating the Output Integrated error
        i = 0
        re_output_integrated = []
        while i < len(re_output_yhat):
            re_output_integrated.append(((re_output_yhat[i] * re_output_error_percent[i]) / 100) + re_output_yhat[i])
            i += 1

        df_final = re_output_ds.copy()

        # Predicted values
        re_output_yhat = pd.DataFrame(re_output_yhat)
        df_final['yhat'] = re_output_yhat.values

        # %Error Values
        re_output_error_percent = pd.DataFrame(re_output_error_percent)
        df_final['%age Prediction'] = re_output_error_percent.values

        # %Integration Values
        re_output_integrated = pd.DataFrame(re_output_integrated)
        df_final['%age Integration'] = re_output_integrated.values

        df_final['da'] = pd.to_datetime(df_final["ds"])
        df_final["day"] = df_final["da"].dt.weekday
        df_final["true"] = df_final["da"].dt.weekday > 4
        df_final = df_final[df_final.true != True]
        df_final = df_final.drop('da', 1)
        df_final = df_final.drop('day', 1)
        df_final = df_final.drop('true', 1)
        df_final.to_csv(os.path.join(settings.ML_DIRECTORY_PATH, f'final_predicted_{file_name}.csv'))
        return True
    except Exception as e:
        print(f"calculatingError Error ====> {e}")
        return True


def predError(df):
    try:
        X_train = df.iloc[:]
        X_train.tail()

        holiday = pd.DataFrame([])
        for date, name in sorted(holidays.UnitedStates(years=[2015, 2016, 2017, 2018, 2019, 2020, 2021]).items()):
            holiday = holiday.append(pd.DataFrame({'ds': date, 'holiday': "US-Holidays"}, index=[0]), ignore_index=True)
        holiday['ds'] = pd.to_datetime(holiday['ds'], format='%Y-%m-%d', errors='ignore')
        model = Prophet(
            daily_seasonality=True,
            holidays=holiday,
            seasonality_mode=('additive'),
            changepoint_prior_scale=0.5,
            n_changepoints=100,
            holidays_prior_scale=0.5
        )

        model.fit(X_train, algorithm='Newton')
        future = model.make_future_dataframe(periods=30, freq="D")
        forecast_new = model.predict(future)
        forecast_new.tail(10)
        fig1 = model.plot(forecast_new)
        forecast_new.to_csv(os.path.join(settings.ML_DIRECTORY_PATH, 'output_file_calculated.csv'))
        fig = model.plot_components(forecast_new)
        list(forecast_new)
    except Exception as e:
        print(f"predError Error ====> {e}")
        return True
