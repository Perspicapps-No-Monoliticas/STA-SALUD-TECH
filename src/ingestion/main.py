import sys

from fastapi import FastAPI


from api import ingestion_router

app = FastAPI()


if "unittest" not in sys.modules.keys():
    from db_init import init_db

    init_db()


app.include_router(ingestion_router)
