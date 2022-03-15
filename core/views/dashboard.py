import stripe

from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import User
from subscription.models import OrderDetail


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        user_obj = User.objects.filter(pk=self.request.user.id)
        context = {"user_obj": user_obj}
        try:
            # Retrieve the subscription & product
            stripe_customer = OrderDetail.objects.get(user=self.request.user, is_active=True)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
            product = stripe.Product.retrieve(subscription.plan.product)

            context.update({
                'subscription': subscription,
                'product': product
            })

            return context

        except OrderDetail.DoesNotExist:
            return context
