from celery import Celery

from seedwork.infrastructure.varaibles import CELERY_BROKER_URL

app = Celery(
    "ingestion",
    broker=CELERY_BROKER_URL,
    result_backend=CELERY_BROKER_URL,
    include=[
        "modules.data_intake.infrastructure.tasks",
        "modules.data_intake.infrastructure.event_dispatcher",
    ],
)


if __name__ == "__main__":
    app.start()
