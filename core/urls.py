from django.urls import path

from core.views.dashboard import DashboardView, PlanView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('plan', PlanView.as_view(), name='plan'),
]
