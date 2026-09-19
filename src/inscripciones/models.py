from sqlalchemy import Column, String, Text, Date, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.models import Base

class Inscripcion(Base):
    __tablename__ = 'inscripciones'
    __table_args__ = {'schema': 'public'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dni = Column(String(15), nullable=False)
    nombres = Column(Text, nullable=False)
    apellidos = Column(Text, nullable=False)
    curso = Column(Text, nullable=False)
    empresa = Column(Text, nullable=True)
    telefono = Column(String(20), nullable=True)
    fecha_programada = Column(Date, nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())