from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from users.models import User


# @login_required()
# def dashboard(request):
#     user_obj = User.objects.filter(pk=request.user.id)
#     context = {
#         "user_obj": user_obj
#     }
#
#     return render(request, 'dashboard.html', context=context)


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        user_obj = User.objects.filter(pk=self.request.user.id)
        context = {
            "user_obj": user_obj
        }
        return context
