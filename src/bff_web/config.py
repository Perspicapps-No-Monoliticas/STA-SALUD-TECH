import os
from dotenv import load_dotenv

load_dotenv()

settings = {
    "INGESTION_PATH": os.getenv("INGESTION_PATH", "http://users:8000"),
    "CANONIZATION_PATH": os.getenv("CANONIZATION_PATH", "http://canonization:8005"),
    "AUDIT_PATH": os.getenv("AUDIT_PATH", "http://auditoria:8002"),
}
