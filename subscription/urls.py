from django.urls import path
from subscription.views import *


urlpatterns = [
    path('subscriptions/', SubscriptionView.as_view(), name='subscriptions'),
    path('my-subscriptions/', my_subscriptions, name='my_subscriptions'),

    path('config/', stripe_config),
    path('create-checkout-session/', create_checkout_session, name="create_checkout_session"),
    path('success/', success),
    path('cancel/', cancel),
    path('webhook/', stripe_webhook),

    # List
    path('products/list/', list_products, name='list_products'),

    # Add/Edit
    path('manage/product/', manage_product, name='add_product'),
    path('manage/product/<uuid:uid>/', manage_product, name='edit_product'),
]
