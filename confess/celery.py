import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confess.settings')

app = Celery('confess', include=['confession.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if __name__ == 'main':
    app.start()
