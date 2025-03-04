from seedwork.infrastructure.celery import app
import uuid

from modules.data_intake.application.services import ProcessIngestionService


@app.task
def start_ingestion_task(ingestion_uuid: str, correlation_id: str):
    """
    Starts the ingestion task with the given UUID.
    Args:
        ingestion_uuid (str): The unique identifier for the ingestion task.
    """

    print(f"Starting ingestion task {ingestion_uuid}")
    # Trug
    ProcessIngestionService().process_ingestion(
        uuid.UUID(ingestion_uuid), uuid.UUID(correlation_id)
    )
    print(f"Ingestion task {ingestion_uuid} completed")
