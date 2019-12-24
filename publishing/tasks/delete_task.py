from confess.celery import app
from publishing.services.delete_task_service import DeleteTaskService
from publishing.tasks import BaseTask


class DeleteTask(BaseTask):
    name = 'delete_task'
    callback = None

    def execute(self, *args, **kwargs):
        return DeleteTaskService.delete()


DeleteTask = app.register_task(DeleteTask())
