from dataclasses import dataclass, field
from typing import Dict, Optional
import uuid
from seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class MetadatosImagenDTO(DTO):
    source_filename: str = field(default_factory=str)
    dicom_tags: Optional[Dict] = field(default_factory=dict)
    
@dataclass(frozen=True)
class ImagenMedicaDTO(DTO):
    id_ingestion: uuid.UUID = field(default_factory=uuid.uuid4)
    id_proveedor: uuid.UUID = field(default_factory=uuid.uuid4)
    filename: str = field(default_factory=str)
    metadata: MetadatosImagenDTO = field(default_factory=MetadatosImagenDTO)

@dataclass(frozen=True)
class InformacionMedicaDTO(DTO):
    correlation_id: str = ""
    token: str = ""
    data_ingestion_id: str
    status: str
    provider_id: str = ""
    repository_out_path: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""
    country_iso: str = ""