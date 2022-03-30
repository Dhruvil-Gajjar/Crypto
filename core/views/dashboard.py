import stripe

from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import User
from subscription.models import OrderDetail
from core.utils import get_cards_data, get_last_ten_days_chart, get_sparkline


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        user_obj = User.objects.filter(pk=self.request.user.id)
        context = {"user_obj": user_obj}
        try:
            # Retrieve the subscription & product
            stripe_customer = OrderDetail.objects.filter(user=self.request.user, is_active=True).first()
            subscription = None
            if stripe_customer:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                try:
                    subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
                except Exception as e:
                    print(e)

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

            return context

        except OrderDetail.DoesNotExist:
            return context
