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
