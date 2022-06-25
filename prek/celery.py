import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prek.settings.development')

app = Celery('prek')

app.config_from_object('django.conf:settings', namespace='CELERY')
