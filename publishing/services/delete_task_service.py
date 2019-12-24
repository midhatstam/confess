import datetime
import logging

from django.db import Error
from django_celery_beat.models import PeriodicTask

logger = logging.getLogger(__name__)


class DeleteTaskService:
    @classmethod
    def delete(cls):
        before_one_hour = datetime.datetime.now() - datetime.timedelta(hours=1)
        old_tasks = PeriodicTask.objects.filter(enabled=False, clocked__clocked_time__lte=before_one_hour)
        logger.info(f'Tasks preparing for delete: {old_tasks}')
        if old_tasks.exists():
            for task in old_tasks:
                task_id = task.id
                task_name = task.name
                try:
                    task.delete()
                    logger.info(f'Task with id: {task_id} - {task_name} deleted')
                except Error as err:
                    logger.debug(f'Error occurred while deleting task: {task_id} - {task_name}')
                    logger.exception(err)
                    continue
        return {'status': True}
