import os
import csv

from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Gold, Euro, JPY, CNY, GBP

data = os.path.join(settings.BASE_DIR, 'Historical_Data')

import_csv = ["EUR_USD_Historical_Data.csv", "GBP_USD_Historical_Data.csv", "Gold_Futures_Historical_Data.csv",
              "USD_CNY_Historical_Data.csv", "USD_JPY_Historical_Data.csv"]


def prepare_date(date):
    datetime_object = datetime.strptime(str(date).strip(), '%b %d, %Y')
    return datetime_object


class Command(BaseCommand):
    help = 'Imports Historic Data Of Commodities'

    def handle(self, *args, **kwargs):
        for csv_file in import_csv:
            model = None
            if "EUR_USD" in csv_file:
                model = Euro
            elif "GBP_USD" in csv_file:
                model = GBP
            elif "Gold_Futures" in csv_file:
                model = Gold
            elif "USD_CNY" in csv_file:
                model = CNY
            elif "USD_JPY" in csv_file:
                model = JPY

            data_file = data + "/" + csv_file
            with open(data_file) as f:
                reader = csv.reader(f)
                # skip header
                next(reader)
                for row in reader:
                    date_time = prepare_date(row[0])
                    price = row[1]
                    model.objects.create(
                        price=price,
                        dateTimeStamp=date_time
                    )

        self.stdout.write("Historic Data Imported Successfully!!")

# python manage.py import_historic_data
