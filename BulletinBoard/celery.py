import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletin_board.settings')

app = Celery('bulletin_board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_newsletter': {
        'task': 'board.tasks.newsletter',
        'schedule': crontab(minute='0', hour='6', day_of_week='mon'),
    },
}