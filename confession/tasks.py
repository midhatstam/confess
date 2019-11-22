import datetime
import logging

from celery import shared_task
from confess import celery_app
from django.db.models import Sum, When, Case, IntegerField
from django.db.models.signals import post_save
from django.dispatch import receiver

from confession.models import Confession, AdminApprovedConfession
from confession.utils import slack_notify, get_random_time

logger = logging.getLogger(__name__)


@celery_app.task
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


@celery_app.task
def publish_confession(instance_id):
    logger.info(f'Confession with id: {instance_id} will be published')

    instance = Confession.objects.get(id=instance_id)
    logger.info(f'Confession with id: {instance_id} found!')
    instance.user_approved = True
    instance.save()

    return f'Task executed successfully!'


@receiver(post_save, sender=Confession)
def confession_publish(sender, instance, **kwargs):
    if instance.publish_date is not None:
        publish_confession.apply_async(args=(instance.id,), eta=instance.publish_date)


celery_app.register_task(set_publish_time)
celery_app.register_task(publish_confession)
