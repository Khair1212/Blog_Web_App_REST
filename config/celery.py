
from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Dhaka')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Celery Beat Settings
# app.conf.beat_schedule = {
#     'send-mail-everyday-at-8':{
#         'task': 'send_mail.tasks.send_mail_func',
#         'schedule': crontab(hour=5, minute=8)
#         #'args': (2,)
#     }
# }

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')