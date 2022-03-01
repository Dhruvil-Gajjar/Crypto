from django.urls import path

from core.views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
]
