from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from uuid import UUID

class InscripcionRequest(BaseModel):
    dni: str
    nombres: str
    apellidos: str
    curso: str
    empresa: Optional[str] = None
    telefono: Optional[str] = None
    fecha_programada: date

class InscripcionResponse(InscripcionRequest):
    id: UUID
    fecha_registro: datetime

    class Config:
        from_attributes = True