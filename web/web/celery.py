# django_celery/celery.py

import os
from celery import Celery
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

app = Celery("web")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    time.sleep(5)