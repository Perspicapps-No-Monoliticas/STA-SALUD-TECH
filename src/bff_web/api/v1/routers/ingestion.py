from fastapi import APIRouter, Request
from config import settings
from api.v1.services.ingestion_service import fetch_data, send_data

router_ingestion = APIRouter(prefix="/ingestion")

INGESTION_URL = f"{settings['INGESTION_PATH']}/ingestion"
DATA_INTAKE_URL = f"{INGESTION_URL}/data-intakes"
DATA_SOURCE_URL = f"{INGESTION_URL}/data-sources"

@router_ingestion.get("/health")
def health():
     return fetch_data(f"{INGESTION_URL}/health")

@router_ingestion.post("/reset-db")
def reset_db():
    return send_data(f"{INGESTION_URL}/reset-db")

@router_ingestion.get("/data-intakes/{data_intake_id}")
def get_data_intake(data_intake_id: str):
    print(f"DATA_INTAKE_URL {DATA_INTAKE_URL}")
    return fetch_data(f"{DATA_INTAKE_URL}/{data_intake_id}")

@router_ingestion.get("/data-intakes")
def list_data_intakes(request: Request):
    return fetch_data(f"{DATA_INTAKE_URL}",params=dict(request.query_params))

@router_ingestion.post("/data-intakes")
def create_data_intake(payload: dict):
    return send_data(f"{DATA_INTAKE_URL}", payload)

@router_ingestion.get("/data-sources/{data_source_id}")
def get_data_source(data_source_id: str):
    print(f"DATA_SOURCE_URL {DATA_SOURCE_URL}")
    return fetch_data(f"{DATA_SOURCE_URL}/{data_source_id}")

@router_ingestion.get("/data-sources")
def list_data_sources():
    return fetch_data(f"{DATA_SOURCE_URL}")

@router_ingestion.post("/data-sources")
def create_data_source(payload: dict):
    return send_data(f"{DATA_SOURCE_URL}", payload)