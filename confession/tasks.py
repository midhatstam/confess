import json

from celery import task
from django.db.models import Count

from confession.models import Confession


@task
def set_publish_time():
    instances: Confession = Confession.objects.filter()

