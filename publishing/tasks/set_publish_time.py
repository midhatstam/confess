from confess.celery import app
from publishing.services.set_publish_time_service import SetPublishTimeService
from publishing.tasks import BaseTask


class PublishTimeUpdateCallback:

    def __call__(self, result, *args, **kwargs):
        SetPublishTimeService.update(result, *args, **kwargs)


class SetPublishTimeTask(BaseTask):
    name = "set_publish_time_task"
    callback = PublishTimeUpdateCallback

    def execute(self, **kwargs):
        return SetPublishTimeService.check_instance()


SetPublishTimeTask = app.register_task(SetPublishTimeTask())
