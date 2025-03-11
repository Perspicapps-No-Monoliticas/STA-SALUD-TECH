from fastapi import FastAPI, APIRouter, HTTPException, Response
from aplicacion.comandos.realizar_anonimizado import AnonimizarInformacionMedica
from aplicacion.dto import ImagenMedicaDTO
from dominio.entidades import ImagenMedica, MetadatosImagen
from seedwork.aplicacion.comandos import ejecutar_commando

app = FastAPI()
prefix_router = APIRouter(prefix="/anonimizacion")

@prefix_router.get("/ping")
def healthcheck():
    return "pong"

@prefix_router.post("/anonymize/")
async def anonymize_image(
    file: ImagenMedicaDTO
):
    """
    Anonymize a medical image by removing personal information.
    """
    try:
        # Create domain entities
        metadata = MetadatosImagen(source_filename= file.metadata.source_filename, dicom_tags=file.metadata.dicom_tags) 
        medical_image = ImagenMedica(id_ingestion=file.id_ingestion, id_proveedor=file.id_proveedor, filename=file.filename, metadata=metadata)
        
        # Process the anonymization
        #comando = AnonimizarInformacionMedica(medical_image)
        #ejecutar_commando(comando)

        return Response('Accepted', status_code=202, media_type='application/json')
    except Exception as e:
        print(f"anonymize_image failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(prefix_router)