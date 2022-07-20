import os

from django.conf import settings
from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import EmailMessage


@shared_task(bind=True)
def send_mail_func(self, to_emails, current_url):
    #to_email = 'khair.ahammed04@outlook.com'
    for email in to_emails:
        try:
            mail_subject = "Celery Testing"
            message = f"Check Out This Post: {current_url}"
            email = EmailMessage(
                subject=mail_subject,
                body=message,
                from_email=os.environ.get('EMAIL_FROM'),
                to=[email],
            )
            email.send()

        except Exception as e:
            return e

    return "Done"

