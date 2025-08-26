from __future__ import absolute_import, unicode_literals
import os
import os
from celery import Celery
from django.conf import settings

# اگر متغیر محیطی تعریف نشده بود، پیش‌فرض dev استفاده میشه
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('config')

# اینجا سلری خودش تمام متغیرهای CELERY_* رو از ستینگ میگیره
app.config_from_object('django.conf:settings', namespace='CELERY')

# کشف خودکار تسک‌ها از اپ‌ها
app.autodiscover_tasks()
app.conf.update(
    task_default_queue='celery',
)
# تست ساده
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')