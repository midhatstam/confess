import datetime

from celery import task
from django.db.models import Sum, When, Case, IntegerField

from confession.models import Confession
from confession.utils import slack_notify


@task
def set_publish_time():
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    instances = Confession.objects.filter(item_meta_data_date__gte=date_from).annotate(
        approved_count=Sum(
            Case(
                When(confessionuserapprovement__vote=True, then=1),
                When(confessionuserapprovement__vote=False, then=-1),
                When(confessionuserapprovement=None, then=0),
                output_field=IntegerField()
            )
        )
    ).order_by('-approved_count')

    for i in instances:
        message = f'Confession with id: {i.id} and approved_count: {i.approved_count}'
        slack_notify(message=message)
