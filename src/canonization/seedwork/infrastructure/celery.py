# celery.py
from celery import Celery
from .varaibles import CELERY_BROKER_URL

app = Celery("ingestion_project", broker=CELERY_BROKER_URL)

app.conf.update(
    result_backend=CELERY_BROKER_URL,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
