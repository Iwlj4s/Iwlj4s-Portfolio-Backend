from celery import Celery
from celery_stuff.celery_config import CeleryConfig


app = Celery("iwlj4s_portfolio")
app.config_from_object(CeleryConfig)
import celery_stuff.celery_tasks

