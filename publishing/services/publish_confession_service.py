import logging

from confession.models import Confession

logger = logging.getLogger(__name__)


class PublishConfessionService:

    @classmethod
    def publish(cls, instance_id):
        logger.info(f'Confession with id: {instance_id} will be published')

        instance = Confession.objects.get(id=instance_id)
        logger.info(f'Confession with id: {instance_id} found!')
        instance.user_approved = True
        instance.save()

        return f'Task executed successfully!'
