import os
from dotenv import load_dotenv


load_dotenv()

BFF_HOST = os.getenv("BFF_HOST", "http://localhost:8006/bff/v1")
INGESTION_HOST = os.getenv("INGESTION_HOST", "http://localhost:8000/ingestion/reset-db")
