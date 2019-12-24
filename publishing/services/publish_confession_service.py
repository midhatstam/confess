import logging

from django.db import IntegrityError

from confession.models import Confession
from confession.utils import slack_notify

logger = logging.getLogger(__name__)


class PublishConfessionService:

    @classmethod
    def publish(cls, instance_id):
        logger.info(f'Confession with id: {instance_id} will be published')
        try:
            instance = Confession.objects.get(id=instance_id)
        except Confession.DoesNotExist:
            logger.debug(f'Confession with id: {instance_id} does not exist!')
            return {"status": False}
        logger.info(f'Confession with id: {instance_id} found!')
        try:
            instance.user_approved = True
            instance.save()
        except IntegrityError as err:
            logger.debug(f'Could not save instance status to db!')
            logger.exception(err)
            return {"status": False}

        return {"status": True, "instance_id": instance_id}

    @classmethod
    def notify(cls, *args, **kwargs):
        instance_id = kwargs['instance_id']
        message = f'Confession with id: {instance_id} has been published successfully'
        slack_notify(message)
