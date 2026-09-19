from sqlalchemy import Column, Integer, String, Text, Date
from src.models import Base

class Curso(Base):
    __tablename__ = 'cursos'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, index=True)
    nombre_curso = Column(Text, nullable=False)
    src_portada = Column(Text, nullable=True)
    titulo = Column(Text, nullable=True)
    descripcion = Column(Text, nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    fecha_final = Column(Date, nullable=True)