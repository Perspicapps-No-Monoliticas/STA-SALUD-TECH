from celery import Celery

from seedwork.infraestructure.varaibles import CELERY_BROKER_URL

app = Celery(
    "ingestion",
    broker=CELERY_BROKER_URL,
    result_backend=CELERY_BROKER_URL,
    include=[
        "modules.data_intake.infraestructure.tasks",
        "modules.data_intake.infraestructure.event_dispatcher",
    ],
)


if __name__ == "__main__":
    app.start()
