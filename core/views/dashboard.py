from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from users.models import User


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        user_obj = User.objects.filter(pk=self.request.user.id)
        context = {
            "user_obj": user_obj
        }
        return context


class SubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = "Subscriptions/subscriptions.html"


