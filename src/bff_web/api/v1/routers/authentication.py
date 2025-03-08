from fastapi import APIRouter, Request, HTTPException, status
from config import settings
import uuid

router_auth = APIRouter(prefix=f"{settings['API_PREFIX']}/auth")

valid_tokens = set()

@router_auth.get("/generate_token")
async def generate_token():
    token = str(uuid.uuid4())
    valid_tokens.add(token)
    return {"token": token}

async def validate_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o no proporcionado")

    token = auth_header.split("Bearer ")[1]
    
    if token not in valid_tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o no proporcionado")
    
    return token
