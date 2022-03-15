from django.urls import path
from subscription.views import *


urlpatterns = [
    path('subscriptions/', SubscriptionView.as_view(), name='subscriptions'),
    path('config/', stripe_config),
    path('create-checkout-session/', create_checkout_session, name="create_checkout_session"),
    path('success/', success),
    path('cancel/', cancel),
    path('webhook/', stripe_webhook),
]
