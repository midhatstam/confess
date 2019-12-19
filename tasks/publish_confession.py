from confess.celery import app
from services.publish_confession import PublishConfession
from tasks import BaseTask


class PublishConfessionTask(BaseTask):
    name = 'publish_confession_task'
    callback = None

    def execute(self, *args, **kwargs):
        instance_id = kwargs['instance_id']
        return PublishConfession.publish(instance_id)


PublishConfessionTask = app.register_task(PublishConfessionTask)
