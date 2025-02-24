from seedwork.presentation.api import create_router

from .data_intake import data_intake_router
from .data_source import data_source_router

ingestion_router = create_router("/ingestion")

ingestion_router.include_router(data_intake_router)
ingestion_router.include_router(data_source_router)


# health
@ingestion_router.get("/health")
def ping():
    return "pong"


@ingestion_router.post("/reset-db")
def rest_db():
    from config.db import Base, db

    Base.metadata.drop_all(bind=db.get_bind())
    Base.metadata.create_all(bind=db.get_bind())
    db.commit()
    db.close()
