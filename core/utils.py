from core.models import *


def get_trail():
    gold_obj = Gold.objects.all().order_by('created_at').first()
    euro_obj = Euro.objects.all().order_by('created_at').first()
    jpy_obj = JPY.objects.all().order_by('created_at').first()
    cny_obj = CNY.objects.all().order_by('created_at').first()
    gbp_obj = GBP.objects.all().order_by('created_at').first()

    trail = [
        {
            "price": gold_obj.price if gold_obj else 0,
            "commodity_img": "https://s2.coinmarketcap.com/static/img/coins/32x32/624.png"
        },
        {
            "price": euro_obj.price if euro_obj else 0,
            "commodity_img": "https://s2.coinmarketcap.com/static/img/coins/32x32/2083.png"
        },
        {
            "price": jpy_obj.price if jpy_obj else 0,
            "commodity_img": "https://s2.coinmarketcap.com/static/img/coins/32x32/2989.png"
        },
        {
            "price": cny_obj.price if cny_obj else 0,
            "commodity_img": "https://s2.coinmarketcap.com/static/img/coins/32x32/3408.png"
        },
        {
            "price": gbp_obj.price if gbp_obj else 0,
            "commodity_img": "https://s2.coinmarketcap.com/static/img/coins/32x32/6906.png"
        }
    ]

    return trail


def get_timeStamp(dtObj):
    try:
        time_stamp = str(dtObj.timestamp()).split(".")[0]
        return int(time_stamp)
    except:
        return None


def get_sparkline():
    sparkline_dict = {
        "data": []
    }

    gold_queryset = Gold.objects.all().order_by('created_at')
    for obj in gold_queryset:
        time_stamp = get_timeStamp(obj.dateTimeStamp)
        if time_stamp:
            sparkline_dict["data"].append([time_stamp, float(str(obj.price).replace(",", ""))])

    return sparkline_dict


def get_prediction():
    prediction_dict = {
        "actual": [],
        "predicted": []
    }

    gold_queryset = Gold.objects.all().order_by('created_at')
    for obj in gold_queryset:
        if obj.price and obj.predicted_price:
            prediction_dict["actual"].append(float(str(obj.price).replace(",", "")))
            prediction_dict["predicted"].append(float(1740.7343300059))

    return prediction_dict
