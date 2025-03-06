from fastapi import APIRouter
from config import settings
from api.v1.services.canonization_service import fetch_data, send_data

router_canonization = APIRouter(prefix="/canonization")

CANONIZATION_PATH_URL = f"{settings['CANONIZATION_PATH']}/canonization"

@router_canonization.get("/health")
def health():
    return fetch_data(f"{CANONIZATION_PATH_URL}/health")    

@router_canonization.post("/reset-db")
def reset_db():
    return send_data(f"{CANONIZATION_PATH_URL}/reset-db")

@router_canonization.get("/data-canonizations")
def list_canonizations():
    return fetch_data(f"{CANONIZATION_PATH_URL}/data-canonizations")

@router_canonization.post("/data-canonizations")
def create_canonization(payload: dict):
    return send_data(f"{CANONIZATION_PATH_URL}/data-canonizations", payload)

@router_canonization.get("/data-canonizations/{canonization_id}")
def get_canonization_by_id(canonization_id: str):
    print(f"CANONIZATION_PATH_URL {CANONIZATION_PATH_URL}")
    return fetch_data(f"{CANONIZATION_PATH_URL}/data-canonizations/{canonization_id}")