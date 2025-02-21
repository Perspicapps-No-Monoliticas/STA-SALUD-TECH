from seedwork.presentation.api import create_router

from .data_intake import data_intake_router
from .data_source import data_source_router

ingestion_router = create_router("/ingestion")

ingestion_router.include_router(data_intake_router)
ingestion_router.include_router(data_source_router)


# health
@ingestion_router.get("/ping")
def ping():
    return "pong"
