import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE','wiremit_backend.settings')
app = Celery('wiremit_backend', broker=os.environ.get('REDIS_URL','redis://redis:6379/0'))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
