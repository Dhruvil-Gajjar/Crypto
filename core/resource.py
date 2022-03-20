from import_export import resources
from import_export.fields import Field
from import_export import widgets

from core.models import *
# %b %d, %Y


class CustomDateTimeWidget(widgets.DateTimeWidget):
    def clean(self, value, row=None, *args, **kwargs):
        print("*"*80)
        print(self)


class GoldResource(resources.ModelResource):
    dateTimeStamp = Field(attribute='dateTimeStamp', column_name='Date', widget=widgets.DateTimeWidget("%b %d, %Y"))
    price = Field(attribute='price', column_name='Price')

    class Meta:
        model = Gold
        fields = ("id", "dateTimeStamp", "price")


class EuroResource(resources.ModelResource):
    dateTimeStamp = Field(attribute='dateTimeStamp', column_name='Date')
    price = Field(attribute='price', column_name='Price')

    class Meta:
        model = Euro
        fields = ("id", "dateTimeStamp", "price")


class JPYResource(resources.ModelResource):
    dateTimeStamp = Field(attribute='dateTimeStamp', column_name='Date')
    price = Field(attribute='price', column_name='Price')

    class Meta:
        model = JPY
        fields = ("id", "dateTimeStamp", "price")


class CNYResource(resources.ModelResource):
    dateTimeStamp = Field(attribute='dateTimeStamp', column_name='Date')
    price = Field(attribute='price', column_name='Price')

    class Meta:
        model = CNY
        fields = ("id", "dateTimeStamp", "price")


class GBPResource(resources.ModelResource):
    dateTimeStamp = Field(attribute='dateTimeStamp', column_name='Date')
    price = Field(attribute='price', column_name='Price')

    class Meta:
        model = GBP
        fields = ("id", "dateTimeStamp", "price")
