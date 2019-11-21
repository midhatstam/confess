import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confess.settings')

app = Celery('confess', include=['confession.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'set-publish-time': {
        'task': 'confession.tasks.set_publish_time',
        'schedule': crontab(hour=15, minute=45),
    },
}

if __name__ == 'main':
    app.start()
