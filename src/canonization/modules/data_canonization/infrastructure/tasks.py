from seedwork.infrastructure.celery import app
import uuid

from modules.data_canonization.application.services import ProcessCanonizationService


@app.task
def start_canonization_task(canonization_uuid: str, correlation_id: str):
    """
    Starts the canonization task with the given UUID.
    Args:
        canonization_uuid (str): The unique identifier for the canonization task.
        correlation_id (str): The unique identifier for the correlation
    """

    print(f"Starting canonization task {canonization_uuid}")
    # Trug
    ProcessCanonizationService().process_canonization(
        uuid.UUID(canonization_uuid), uuid.UUID(correlation_id)
    )
    print(f"Canonization task {canonization_uuid} completed")
