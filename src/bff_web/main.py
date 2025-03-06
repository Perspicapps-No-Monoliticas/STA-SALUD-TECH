from fastapi import FastAPI, Request, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from api.v1.routers import ingestion, canonization, audit

app = FastAPI()

api_router = APIRouter(prefix="/bff/v1")

api_router.include_router(ingestion.router_ingestion)
api_router.include_router(canonization.router_canonization)
api_router.include_router(audit.router_audit)
app.include_router(api_router)

@api_router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

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