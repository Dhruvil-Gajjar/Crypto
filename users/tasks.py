from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import EmailMessage

from users.models import User
from project.celery import app


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


@shared_task
def end_user_free_trial_period():
    trial_end_date = get_date_N_days_ago(14)

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
