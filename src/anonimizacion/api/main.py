from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from src.aplicacion.pipeline import PipelineAnonimizacion
from src.aplicacion.dto import ImagenMedicaDTO
from src.dominio.entidades import ImagenMedica, MetadatosImagen

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Dependency to get the anonymization pipeline
def get_pipeline():
    return PipelineAnonimizacion()

@app.post("/anonymize/")
async def anonymize_image(
    file: ImagenMedicaDTO,
    pipeline: PipelineAnonimizacion = Depends(get_pipeline)
):
    """
    Anonymize a medical image by removing personal information.
    """
    try:
        # Create domain entities
        metadata = MetadatosImagen(source_filename= file.metadata.source_filename, dicom_tags=file.metadata.dicom_tags) 
        medical_image = ImagenMedica(filename=file.filename, metadata=metadata)
        # Process the anonymization
        result = pipeline.procesar(medical_image)
        
        return {
            "message": "Image anonymized successfully",
            "token": result.token
        }
    except Exception as e:
        print(f"anonymize_image failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))