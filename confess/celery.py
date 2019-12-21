import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confess.settings')

app = Celery('konfess-tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.Task.resultrepr_maxsize = 2048

app.conf.update(
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    result_backend='django-db',
    task_ignore_result=True,
    task_store_errors_even_if_ignored=False,
    broker_connection_max_retries=0,
    broker_pool_limit=50,
    task_inherit_parent_priority=True,
    worker_hijack_root_logger=False,
)

app.conf.task_default_queue = 'celery'

app.autodiscover_tasks()

if __name__ == 'main':
    app.start()
