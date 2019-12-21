import logging
from celery import Task


logger = logging.getLogger(__name__)

__all__ = ['BaseTask', 'SetPublishTimeTask', 'PublishConfessionTask']


class BaseTask(Task):
    abstract = True
    # ----------
    name = None
    callback = None
    history_enabled = True

    def execute(self, *args, **kwargs):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        local_params = locals()
        logger.info(f"'{self.name}' with params '{local_params}' is started")

        result = self.execute(*args, **kwargs)

        if self.callback:
            self.callback()(result, *args, **kwargs)

        logger.info(f"{self.name} with params '{local_params}' is finished")

        clz = result.__class__
        result = result.as_dict()
        logger.debug(f"task result class converted to the dict {clz}")

        logger.debug(f'Task: {self.name}, Context: {local_params}, Result: {result}')

        return result

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.exception(exc)
        # raise exc  # NOTE: django-celery-results is not working properly in case of 'raise'


from .set_publish_time import SetPublishTimeTask
from .publish_confession import PublishConfessionTask
