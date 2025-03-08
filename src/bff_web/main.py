from fastapi import FastAPI, Request, HTTPException, APIRouter, Depends
from fastapi.responses import JSONResponse
from config import settings
from api.v1.routers import ingestion, canonization, audit, authentication

app = FastAPI()

health_router = APIRouter()
@health_router.get(f"{settings['API_PREFIX']}/health")
def healthcheck():
    return {"status": "ok"}


api_router = APIRouter(prefix=settings['API_PREFIX'], dependencies=[Depends(authentication.validate_token)] )

api_router.include_router(ingestion.router_ingestion)
api_router.include_router(canonization.router_canonization)
api_router.include_router(audit.router_audit)

app.include_router(authentication.router_auth)
app.include_router(api_router)
app.include_router(health_router)


@app.exception_handler(HTTPException)
async def service_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"error": "Servicio no encontrado en el BFF", "path": request.url.path},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )