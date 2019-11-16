import datetime
import logging

from celery import task
from django.db.models import Sum, When, Case, IntegerField

from confession.models import AdminApprovedConfession
from confession.utils import slack_notify, get_random_time

logger = logging.getLogger(__name__)


@task
def set_publish_time():
    # date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    instances = AdminApprovedConfession.objects.filter(publish_date__isnull=True).annotate(
        approved_count=Sum(
            Case(
                When(confessionuserapprovement__vote=True, then=1),
                When(confessionuserapprovement__vote=False, then=-1),
                When(confessionuserapprovement=None, then=0),
                output_field=IntegerField()
            )
        )
    ).order_by('-approved_count')

    logger.debug(f'Filtered confession queryset is: {instances}')
    if instances.exists():
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
        return f'Task executed with confessions: {instances}'
    else:
        message = 'There is no confession to publish'
        slack_notify(message=message)

        return f'Task executed with message: {message}'
