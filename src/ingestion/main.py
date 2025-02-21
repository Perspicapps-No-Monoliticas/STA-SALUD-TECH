from fastapi import FastAPI


from api import ingestion_router

app = FastAPI()


# if "unittest" not in sys.modules.keys():
#     import db_init


app.include_router(ingestion_router)
