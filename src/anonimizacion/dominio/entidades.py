from dataclasses import dataclass
from typing import Dict, Optional, List
from src.seedwork.dominio.entidades import Entidad

@dataclass
class MetadatosImagen(Entidad):
    source_filename: str = ""
    dicom_tags: Optional[Dict] = None
    
    def __str__(self) -> str:
        return self.source_filename.upper()
    
@dataclass
class ImagenMedica(Entidad):
    #content: bytes
    filename: str = ""
    metadata: MetadatosImagen = None
    
    def __str__(self) -> str:
        return self.filename.upper()
    
    def obtener_metadatos(self) -> MetadatosImagen:
        return self.metadata
