from celery import shared_task
from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from users.models import User
from project.celery import app
from subscription.utils import calculate_diff_in_days


@app.task()
def send_activation_link(mail_subject, message, to_email):
    try:
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        print('#### >>>>>>>>>>>>>>>>>>>>>>>> Email has been sent successfully to %s !!' % to_email)
    except Exception as err:
        print('#### >>>>>>>>>>>>>>>>>>>>>>>> Error in sending email to %s.' % to_email)
        print(err)


def get_date_N_days_ago(days):
    date_N_days_ago = datetime.now() - timedelta(days=days)
    date = date_N_days_ago.date()
    return date.strftime('%Y-%m-%d')


trial_end_date = get_date_N_days_ago(14)


@shared_task
def end_user_free_trial_period():
    free_trial_users = User.objects.filter(
        is_active=True,
        free_trial=True,
        is_staff=False,
        is_superuser=False,
        date_joined__contains=trial_end_date
    )

    for user in free_trial_users:
        try:
            user_joined_date = str(user.date_joined).split(" ")[0]
            if user_joined_date == trial_end_date:
                user.free_trial = False
                user.save()
        except Exception as err:
            print('#### >>>>>>>>>>>>>>>>>>>>>>>> Error in updating user with id %s.' % user.id)
            print(err)
            continue


@app.task()
def send_subscription_reminder():
    user_queryset = User.objects.filter(
        is_active=True,
        free_trial=True,
        is_staff=False,
        is_superuser=False,
        date_joined__contains=trial_end_date
    )

    for user in user_queryset:
        days_joined_before = calculate_diff_in_days(user.email)
        if days_joined_before == 12:
            mail_subject = 'GYNERO Portal - Your account free trial will expire in 48 hours.'
            message = render_to_string('Users/free_trial_reminder.html', {
                'protocol': settings.SITE_PROTOCOL,
                'user': user,
                'hour': 48,
                'domain': "gynero.com"
            })
            send_activation_link.delay(mail_subject, message, user.email)
        elif days_joined_before == 13:
            mail_subject = 'GYNERO Portal - Your account free trial will expire in 24 hours.'
            message = render_to_string('Users/free_trial_reminder.html', {
                'protocol': settings.SITE_PROTOCOL,
                'user': user,
                'hour': 24,
                'domain': "gynero.com"
            })
            send_activation_link.delay(mail_subject, message, user.email)
        else:
            continue
