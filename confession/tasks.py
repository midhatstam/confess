from celery import task
from django.core.mail import send_mail

from django.conf import settings


@task
def send_email():
    send_mail(
        'Celery task test',
        'It is working',
        settings.EMAIL_HOST_USER,
        ['midhat@gmail.com'],
        fail_silently=False,
    )
