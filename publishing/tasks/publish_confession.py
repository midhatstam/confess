from confess.celery import app
from publishing.services.publish_confession_service import PublishConfessionService
from publishing.tasks import BaseTask


class PublishConfessionCallback:

    def __call__(self, *args, **kwargs):
        PublishConfessionService.notify(*args, **kwargs)


class PublishConfessionTask(BaseTask):
    name = "publish_confession_task"
    callback = PublishConfessionCallback

    def execute(self, **kwargs):
        instance_id = kwargs['instance_id']
        return PublishConfessionService.publish(instance_id)


PublishConfessionTask = app.register_task(PublishConfessionTask())
