from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from core.resource import *
from core.models import PredictionData


# Gold
@admin.register(Gold)
class GoldAdmin(ImportExportModelAdmin):
    resource_class = GoldResource
    list_display = ('dateTimeStamp', 'price')
    ordering = ["-dateTimeStamp"]


# Euro
@admin.register(Euro)
class EuroAdmin(ImportExportModelAdmin):
    resource_class = EuroResource
    list_display = ('dateTimeStamp', 'price')
    ordering = ["-dateTimeStamp"]


# JPY
@admin.register(JPY)
class JPYAdmin(ImportExportModelAdmin):
    resource_class = JPYResource
    list_display = ('dateTimeStamp', 'price')
    ordering = ["-dateTimeStamp"]


# CNY
@admin.register(CNY)
class CNYAdmin(ImportExportModelAdmin):
    resource_class = CNYResource
    list_display = ('dateTimeStamp', 'price')
    ordering = ["-dateTimeStamp"]


# GBP
@admin.register(GBP)
class GBPAdmin(ImportExportModelAdmin):
    resource_class = GBPResource
    list_display = ('dateTimeStamp', 'price')
    ordering = ["-dateTimeStamp"]


@admin.register(PredictionData)
class PredictionDataAdmin(admin.ModelAdmin):
    list_display = ('commodity', 'dateTimeStamp', 'price')
    ordering = ["commodity", "-dateTimeStamp"]
