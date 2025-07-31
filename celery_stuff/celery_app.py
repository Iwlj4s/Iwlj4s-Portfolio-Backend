from celery import Celery
from celery_stuff.celery_config import CeleryConfig


app = Celery("iwlj4s_portfolio")
app.config_from_object(CeleryConfig)
app.conf.result_extended = True  # Хранить результаты дольше
app.conf.result_expires = 3600  # 1 час
import celery_stuff.celery_tasks

