from seedwork.presentation.api import create_router

from .data_canonization_router import data_canonization_router

canonization_router = create_router("/canonization")

canonization_router.include_router(data_canonization_router)


# health
@canonization_router.get("/health")
def ping():
    return "pong"


@canonization_router.post("/reset-db")
def rest_db():
    from config.db import Base, db

    db.close()
    Base.metadata.drop_all(bind=db.get_bind())
    Base.metadata.create_all(bind=db.get_bind())
    db.commit()
    db.close()
