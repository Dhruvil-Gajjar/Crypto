import stripe

from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from users.models import User
from subscription.models import OrderDetail
from core.utils import get_cards_data, get_last_ten_days_chart, get_sparkline


@login_required
def dashboard_view(request):
    user_obj = User.objects.filter(pk=request.user.id)
    if user_obj.first().is_plan_selected or user_obj.first().is_superuser:
        context = {"user_obj": user_obj}
        try:
            # Retrieve the subscription & product
            stripe_customer = OrderDetail.objects.filter(user=request.user, is_active=True).first()
            subscription = None
            if stripe_customer:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                try:
                    subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
                except Exception as e:
                    print(f"DashboardView Error ====> {e}")

            # Get Cards
            cards = get_cards_data()
            cards_chart = get_last_ten_days_chart()

            # Get charts
            sparklines = get_sparkline()

            context.update({
                'subscription': subscription,
                'cards': cards,
                'cards_chart': cards_chart,
                'sparklines': sparklines
            })

            return render(request, 'dashboard.html', context=context)

        except OrderDetail.DoesNotExist:
            return render(request, 'dashboard.html', context=context)
    else:
        return redirect('subscriptions')


def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        context = {}
        return render(request, 'landing_page.html', context=context)
