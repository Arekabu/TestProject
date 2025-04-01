import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestProject.settings')

app = Celery('TestProject')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# запуск задания printer каждые 5 секунд
# app.conf.beat_schedule = {
#     'print_every_5_seconds': {
#         'task': 'mc_donalds.tasks.printer',
#         'schedule': 5,
#         'args': (5,),
#     },
# }

# запуск задания action каждый понедельник в 08:00
# app.conf.beat_schedule = {
#     'action_every_monday_8am': {
#         'task': 'action',
#         'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
#         'args': (agrs),
#     },
# }

app.conf.beat_schedule = {
    'clear_board_every_minute': {
        'task': 'mc_donalds.tasks.clear_old',
        'schedule': crontab(),
    },
}