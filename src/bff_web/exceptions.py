from fastapi import HTTPException

class ServiceUnavailableException(HTTPException):
    def __init__(self, service_name: str):
        super().__init__(
            status_code=503,
            detail=f"El servicio '{service_name}' no está disponible o no existe en el BFF."
        )
