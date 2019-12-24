import datetime
import logging

from django.db import Error
from django_celery_beat.models import PeriodicTask

logger = logging.getLogger(__name__)


class DeleteTaskService:
    @classmethod
    def delete(cls):
        before_one_hour = datetime.datetime.now() - datetime.timedelta(hours=1)
        old_tasks = PeriodicTask.objects.filter(enabled=False, clocked__clocked_time_lte=before_one_hour)
        logger.info('')
        if old_tasks.exists():
            for task in old_tasks:
                try:
                    task.delete()
                except Error as err:
                    logger.debug('')
                    logger.exception(err)
                    continue
        return {'status': True}
