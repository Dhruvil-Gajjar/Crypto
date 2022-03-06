from django.contrib.auth.views import LoginView
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from users.models import User
from users.forms import SignupForm, RegisterForm, EditUserForm, UpdateUserForm


@transaction.atomic
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'Auth/signup.html', {'form': form})


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

    context.update({
        'form': form
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
