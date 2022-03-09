from celery import shared_task
from django.core.mail import EmailMessage

from project.celery import app


@app.task()
def send_activation_link(message, to_email):
    try:
        mail_subject = 'CRYPTO - Activate your account.'

        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        print('#### >>>>>>>>>>>>>>>>>>>>>>>> Email has been sent successfully to %s !!' % to_email)
    except Exception as err:
        print(err)
