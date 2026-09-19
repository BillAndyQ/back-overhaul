from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, validator
from fastapi import UploadFile

class RequestEquipo(BaseModel):
    tipo_unidad: str
    placa: str
    ubicacion: str
    tipo_servicio: str
    fecha_servicio: str
    inspector: str
    descripcion: str
    
    # Archivos opcionales
    informeCampo: Optional[UploadFile] = None
    informeFinal: Optional[UploadFile] = None
    certificado: Optional[UploadFile] = None

    class Config:
        # Necesario para que Pydantic acepte clases de FastAPI como UploadFile
        arbitrary_types_allowed = True
        
class RequestOTEquipo(BaseModel):
    empresa: str
    ruc: str = Field(..., min_length=11, max_length=11)
    estado: str
    fechaServicio: date
    certificadora: str
    registered : bool

    @validator('ruc')
    def validate_ruc_digits(cls, v):
        if not v.isdigit():
            raise ValueError('El RUC debe contener solo números')
        return v
    
class PersonaRequest(BaseModel):
    empresa: str
    ruc: str
    modalidad: str
    cursos: str
    nombres: str
    apellidos: str
    dni: str
    fecha: date
    aprobo: bool
    certificadora: str
    proyecto: Optional[str] = None
    instructor: Optional[str] = None
    archivo_foto_pdf: Optional[str] = None
    certificado: Optional[str] = None
    comentarios: Optional[str] = None
    n_veces: int = Field(default=1, ge=0)

    class Config:
        from_attributes = True