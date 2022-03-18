from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from core.resource import *
from core.forms import EuroForm


# Gold
class GoldAdmin(ImportExportModelAdmin):
    resource_class = GoldResource


admin.site.register(Gold, GoldAdmin)


# Euro
class EuroAdmin(ImportExportModelAdmin):
    resource_class = EuroResource
    form = EuroForm


admin.site.register(Euro, EuroAdmin)


# JPY
class JPYAdmin(ImportExportModelAdmin):
    resource_class = JPYResource


admin.site.register(JPY, JPYAdmin)


# CNY
class CNYAdmin(ImportExportModelAdmin):
    resource_class = CNYResource


admin.site.register(CNY, CNYAdmin)


# GBP
class GBPAdmin(ImportExportModelAdmin):
    resource_class = GBPResource


admin.site.register(GBP, GBPAdmin)
