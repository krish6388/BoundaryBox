from django.apps import AppConfig
from jobs import scheduler

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        # print("In ready")
        scheduler.schedule_job()
