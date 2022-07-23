import stripe

from datetime import datetime
from django.urls import reverse
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import login
from django.db.models.query_utils import Q
from django.core.mail import BadHeaderError
from django.utils.encoding import force_bytes
from django.contrib.auth.views import LoginView
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from users.models import User
from users.tasks import send_activation_link
from users.tokens import account_activation_token
from users.forms import SignupForm, RegisterForm, EditUserForm, UpdateUserForm, ResendActivationEmailForm, \
    UserPasswordResetForm


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
            mail_subject = 'GYNERO - Activate your account.'
            message = render_to_string('Auth/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': user.pk,
                'token': account_activation_token.make_token(user),
            })
            send_activation_link.delay(mail_subject, message, to_email)
            return render(
                request,
                'Auth/confirm_email.html',
                {'first_name': user.first_name, 'last_name': user.last_name}
            )
    else:
        form = SignupForm()
    return render(request, 'Auth/signup-new.html', {'form': form})


def resend_activation_email(request):
    if request.method == 'POST':
        form = ResendActivationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email, is_active=0).first()
            if user:
                current_site = get_current_site(request)
                to_email = form.cleaned_data.get('email')
                mail_subject = 'GYNERO - Activate your account.'
                message = render_to_string('Auth/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': user.pk,
                    'token': account_activation_token.make_token(user),
                })
                send_activation_link.delay(mail_subject, message, to_email)
                return render(
                    request,
                    'Auth/confirm_email.html',
                    {'first_name': user.first_name, 'last_name': user.last_name}
                )
            else:
                form.add_error("email", "User not found for given e-mail!")
    else:
        form = ResendActivationEmailForm()

    return render(request, 'Auth/resend_email.html', {'form': form})


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


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user_obj = User.objects.filter(email=username)
        if user_obj.exists():
            if user_obj.first().is_active:
                if user_obj.filter(password=password).first():
                    login(request, user_obj.first(), backend='django.contrib.auth.backends.ModelBackend')
                    return redirect(reverse('dashboard'))
                else:
                    messages.error(request, 'Username or password not correct !!')
                    return redirect(reverse('login'))
            else:
                messages.error(request, 'Please activate your account !!')
                return redirect(reverse('login'))
        else:
            messages.error(request, 'Account with this email does not exist !!')
            return redirect(reverse('login'))
    else:
        form = AuthenticationForm()

    return render(request, 'Auth/login-new.html', {'form': form})


# class UserLoginView(LoginView):
#     template_name = 'Auth/login.html'


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
def view_profile(request):
    context = {}
    return render(request, 'Users/view_profile.html', context=context)


@login_required
def update_profile(request, uid=None):
    context = {}

    if uid:
        user = get_object_or_404(User, pk=uid)

        if request.method == "POST":
            form = UpdateUserForm(request.POST, instance=user)

            if form.is_valid():
                form.save()
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                return redirect('view_profile')
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


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = UserPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                current_site = get_current_site(request)
                for user in associated_users:
                    mail_subject = 'GYNERO - Reset your account password.'
                    email_template_name = "Auth/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': current_site.domain,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    message = render_to_string(email_template_name, c)
                    try:
                        send_activation_link.delay(mail_subject, message, user.email)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = UserPasswordResetForm()
    return render(request=request, template_name="Auth/password_reset.html",
                  context={"password_reset_form": password_reset_form})
