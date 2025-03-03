import os
from dotenv import load_dotenv


load_dotenv()

# Environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ingestion")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
BROKER_URL = os.getenv("PULSAR_BROKER_URL", default="pulsar://localhost:6650")

COUNTRY_CODE = os.getenv("COUNTRY_CODE", "US")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
