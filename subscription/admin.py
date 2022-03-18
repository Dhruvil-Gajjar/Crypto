from django.contrib import admin
from subscription.models import Product, OrderDetail, OrderHistory


admin.site.register(Product)
admin.site.register(OrderDetail)
admin.site.register(OrderHistory)
