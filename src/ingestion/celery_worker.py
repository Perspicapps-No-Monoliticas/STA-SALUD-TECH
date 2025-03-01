from celery import Celery

from seedwork.infraestructure.varaibles import CELERY_BROKER_URL

app = Celery(
    "ingestion",
    broker=CELERY_BROKER_URL,
    result_backend=CELERY_BROKER_URL,
    include=[
        "modules.data_intake.infraestructure.tasks",
        "modules.data_source.infraestrucuture.event_dispatcher",
    ],
)


# Ensure dispatch_events are registered
import modules.data_source.infraestrucuture.event_dispatcher  # type: ignore

if __name__ == "__main__":
    app.start()
