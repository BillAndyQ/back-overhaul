from sqlalchemy import Boolean, Column, Integer, String, Date, Table, Text, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OTEquipoModel(Base):
    __tablename__ = "ot_equipos"
    id = Column(Integer, primary_key=True, index=True)
    empresa = Column(String(150), nullable=False)
    ruc = Column(String(11), nullable=False)
    estado= Column(String(30), nullable=False)
    fechaServicio = Column("fecha_servicio",DateTime, nullable=False)
    certificadora = Column(String(255), nullable=False)
    n_ot = Column(String(255), nullable=False)
    registered = Column(Boolean, nullable=False)
    deleted = Column(Boolean, nullable=False)
    
class EquipoModel(Base):
    __tablename__ = "equipos"
    
    id = Column(Integer, primary_key=True, index=True)
    
    id_ot_equipo = Column(Integer, ForeignKey("ot_equipos.id"), nullable=False)
    tipo_unidad = Column(String(50), nullable=False)
    placa = Column(String(20), nullable=False)
    ubicacion = Column(String(100), nullable=False)
    tipo_servicio = Column(String(50), nullable=False)
    fecha_servicio = Column(Date, nullable=False)
    inspector = Column(String(100), nullable=False)
    descripcion = Column(Text)
    
    informe_campo_url = Column(String(255))
    informe_final_url = Column(String(255))
    certificado_url = Column(String(255))
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
class OtPersona(Base):
    __tablename__ = 'ot_personas'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, index=True)
    empresa = Column(String(255))
    ruc = Column(String(20))
    modalidad = Column(String(100))
    cursos = Column(Text)
    nombres = Column(String(150))
    apellidos = Column(String(150))
    dni = Column(String(20))
    fecha = Column(Date)
    aprobo = Column(Boolean, default=False)
    certificadora = Column(String(150))
    proyecto = Column(String(150), nullable=True)
    instructor = Column(String(150), nullable=True)
    archivo_foto_pdf = Column(Text, nullable=True)
    certificado = Column(Text, nullable=True)
    comentarios = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    n_ot = Column(String(50), index=True)
    n_veces = Column(Integer, default=1)
    
