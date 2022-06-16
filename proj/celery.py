from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
app = Celery('proj')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# CELERY BEAT schedule
app.conf.beat_schedule = {
    'send-mail-every-15-seconds': {
        'task': 'app_send_mail.tasks.send_mail_periodic',
        'schedule': 15.0, # every 15 second
        # 'schedule': crontab(hour=0, minute=45), # every day at 00:45
        # 'schedule': crontab(hour=12, minute=30), # every day at 12:30
        # 'schedule': crontab(hour=12, minute=00, day_of_week=5), # every friday at 12:00
        # 'schedule': crontab(hour=12, minute=00, day_of_month=1), # every first day of the month at 12:00
    },
}
app.conf.timezone = 'Europe/Berlin'

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))