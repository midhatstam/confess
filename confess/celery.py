import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confess.settings')

app = Celery('confess')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
