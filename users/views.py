import stripe
from datetime import datetime
from django.conf import settings
from django.db import transaction
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from users.models import User
from users.tasks import send_activation_link
from users.tokens import account_activation_token
from users.forms import SignupForm, RegisterForm, EditUserForm, UpdateUserForm

from subscription.models import OrderDetail, OrderHistory


@transaction.atomic
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            to_email = form.cleaned_data.get('email')
            message = render_to_string('Auth/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': user.pk,
                'token': account_activation_token.make_token(user),
            })
            send_activation_link.delay(message, to_email)
            return render(
                request,
                'Auth/confirm_email.html',
                {'first_name': user.first_name, 'last_name': user.last_name}
            )
    else:
        form = SignupForm()
    return render(request, 'Auth/signup.html', {'form': form})


def activate_user(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return HttpResponse('Activation link is invalid!')


class UserLoginView(LoginView):
    template_name = 'Auth/login.html'


@login_required()
def list_users(request):
    context = {}
    users = User.objects.filter(is_staff=False)
    context.update({
        "users": users
    })
    return render(request, 'Users/list_users.html', context=context)


@login_required
# @user_passes_test(lambda u: u.is_superuser)
def manage_user(request, uid=None):
    context = {}

    if uid:
        user = get_object_or_404(User, pk=uid)
        context.update({
            'user': user
        })

    if request.method == "POST":
        if uid:
            form = EditUserForm(request.POST, instance=user)
        else:
            form = RegisterForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('list_users')
    else:
        if uid:
            form = EditUserForm(instance=user)
        else:
            form = RegisterForm()
    context.update({
        'form': form
    })
    return render(request, 'Users/manage_user.html', context=context)


@login_required
def update_profile(request, uid=None):
    context = {}

    if uid:
        user = get_object_or_404(User, pk=uid)

        if request.method == "POST":
            form = UpdateUserForm(request.POST, instance=user)

            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = UpdateUserForm(instance=user)

    subscription = OrderDetail.objects.filter(user=request.user, is_active=True).first()
    subscription_history = OrderHistory.objects.filter(user=request.user).order_by('created_at')
    context.update({
        'form': form,
        'subscription': subscription,
        'subscription_history': subscription_history if subscription_history.exists() else None
    })
    return render(request, 'Users/update_profile.html', context=context)


@login_required
@require_POST
@csrf_exempt
# @user_passes_test(lambda u: u.is_superuser)
def user_action(request, action, uid=None):
    user = get_object_or_404(User, pk=uid)

    if action == 'toggle-status':
        user.is_active = not user.is_active
        user.save()

        return JsonResponse({
            'success': True,
            'message': 'Status Updated'
        })

    elif action == 'delete':
        user.deleted_by = request.user
        user.delete()

        return JsonResponse({
            'success': True,
            'message': 'Successfully Deleted'
        })
