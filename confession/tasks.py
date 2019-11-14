import datetime

from celery import task
from django.db.models import Sum, When, Case, IntegerField

from confession.models import Confession
from confession.utils import slack_notify, get_random_time


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

    for confession in instances:
        publish_time = get_random_time()
        try:
            confession.publish_date = publish_time
            confession.save()
            message = f'Confession with id: {confession.id} and approved votes: {confession.approved_count} updated with publish_time of {publish_time}'
            slack_notify(message=message)
        except Exception as e:
            message = f'Confession with id: {confession.id} could not be updated with publish_time of {publish_time} with error: {e}'
            slack_notify(message=message)
            continue
