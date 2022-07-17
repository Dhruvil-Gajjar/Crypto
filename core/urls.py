from django.urls import path

from core.views.dashboard import dashboard_view, landing_view

urlpatterns = [
    path('', landing_view, name='landing_page'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
