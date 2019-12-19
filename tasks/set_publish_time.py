from confess.celery import app
from services.set_publish_time import SetPublishTime
from tasks import BaseTask


class PublishTimeUpdateCallback:

    def __call__(self, result, *args, **kwargs):
        SetPublishTime.update(result, *args, **kwargs)


class SetPublishTimeTask(BaseTask):
    name = 'set_publish_task'
    callback = PublishTimeUpdateCallback

    def execute(self, *args, **kwargs):
        return SetPublishTime.get_instances()


SetPublishTimeTask = app.register_task(SetPublishTimeTask())
