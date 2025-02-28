from dataclasses import dataclass, field
from typing import Dict, Optional
from src.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class MetadatosImagenDTO(DTO):
    source_filename: str = field(default_factory=str)
    dicom_tags: Optional[Dict] = field(default_factory=dict)
    
@dataclass(frozen=True)
class ImagenMedicaDTO(DTO):
    filename: str = field(default_factory=str)
    metadata: MetadatosImagenDTO = field(default_factory=MetadatosImagenDTO)
