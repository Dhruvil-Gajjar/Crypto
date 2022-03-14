from django.urls import path

from core.views.dashboard import DashboardView, SubscriptionView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('subscriptions', SubscriptionView.as_view(), name='subscriptions'),
]
