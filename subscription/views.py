import json
import stripe

from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseNotFound, JsonResponse, HttpResponse
from django.views.generic import ListView, CreateView, DetailView, TemplateView

from users.models import User
from subscription.utils import create_order_history
from subscription.models import Product, OrderDetail


class SubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = "Subscriptions/subscriptions.html"

    def get_context_data(self, **kwargs):
        products = Product.objects.all().order_by('price')
        context = {
            "products": products
        }
        return context


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        stripe_product_id = request.POST.get('stripeProductId')
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': Product.objects.filter(stripeProductId=stripe_product_id).first().stripeProductId,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@login_required
def success(request):
    stripe_customer = OrderDetail.objects.get(user=request.user, is_active=True)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
    product = stripe.Product.retrieve(subscription.plan.product)

    return render(request, 'Subscriptions/success.html', {
        'product': product,
    })


@login_required
def cancel(request):
    return render(request, 'Subscriptions/cancel.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Fetch Subscription End & Start Date
        subscription = stripe.Subscription.retrieve(stripe_subscription_id)
        # current_period_end
        # current_period_start
        product = stripe.Product.retrieve(subscription.plan.product)

        # Get the user and create a new Order
        user = User.objects.get(id=client_reference_id)
        order_obj = OrderDetail.objects.filter(user=user)

        # Create Order History
        if order_obj.exists():
            create_order_history(order_obj, subscription, product)
            order_obj.delete()

        OrderDetail.objects.create(
            user=user,
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
            productName=product.name,
            subscriptionStartDate=subscription.current_period_start,
            subscriptionEndDate=subscription.current_period_end
        )

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> Payment Successful!!")
        print(user.username if user.username else user.id + ' just subscribed.')
    return HttpResponse(status=200)
