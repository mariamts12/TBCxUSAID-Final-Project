import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magic_loop.settings')

app = Celery('magic_loop')

# namespace='CELERY' means all celery-related configuration
# keys should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
