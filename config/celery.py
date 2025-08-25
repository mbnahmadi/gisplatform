from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# استفاده از تنظیمات بر اساس محیط
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('config')
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()