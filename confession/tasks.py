import datetime
import json

from celery import task
from django.db.models import Count

from confession.models import Confession


@task
def set_publish_time():
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    instances: Confession = Confession.objects.filter(item_meta_data_date__gte=date_from)

