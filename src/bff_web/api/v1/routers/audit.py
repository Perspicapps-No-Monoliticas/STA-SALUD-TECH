from fastapi import APIRouter
from config import settings
from api.v1.services.audit_service import fetch_data, send_data

router_audit = APIRouter(prefix="/auditoria")

AUDIT_PATH_URL = f"{settings['AUDIT_PATH']}/auditoria"

@router_audit.get("/health")
def health():
    return fetch_data(f"{AUDIT_PATH_URL}/health")

@router_audit.get("/accion")
def list_actions():
    return fetch_data(f"{AUDIT_PATH_URL}/accion")

@router_audit.post("/accion")
def create_action(payload: dict):
    return send_data(f"{AUDIT_PATH_URL}/accion", payload)

@router_audit.get("/accion/{action_id}")
def get_accion_by_id(action_id: str):
    print(f"AUDIT path {AUDIT_PATH_URL}")
    return fetch_data(f"{AUDIT_PATH_URL}/accion/{action_id}")