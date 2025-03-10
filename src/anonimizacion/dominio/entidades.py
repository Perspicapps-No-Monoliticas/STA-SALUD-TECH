from dataclasses import dataclass
from typing import Dict, Optional, List
import uuid
from seedwork.dominio.entidades import Entidad

@dataclass
class MetadatosImagen(Entidad):
    source_filename: str = ""
    dicom_tags: Optional[Dict] = None
    
    def __str__(self) -> str:
        return self.source_filename.upper()
    
@dataclass
class ImagenMedica(Entidad):
    #content: bytes
    id_ingestion: uuid.UUID = None
    id_proveedor: uuid.UUID = None
    filename: str = ""
    metadata: MetadatosImagen = None
    
    def __str__(self) -> str:
        return self.filename.upper()

    def obtener_metadatos(self) -> MetadatosImagen:
        return self.metadata

@dataclass
class InformacionMedica(Entidad):
    token: str = ""
    data_ingestion_id: str = ""
    status: str = ""
    provider_id: str = ""
    repository_out_path: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""
    country_iso: str = ""