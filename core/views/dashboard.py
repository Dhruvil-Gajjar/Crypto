from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import User


# @login_required()
def dashboard(request):
    user_obj = User.objects.filter(pk=request.user.id)
    context = {
        "user_obj": user_obj
    }

    return render(request, 'dashboard.html', context=context)
