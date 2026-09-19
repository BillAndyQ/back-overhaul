from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Empresa(Base):
    __tablename__ = 'empresas'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, index=True)
    ruc = Column(String(20), unique=True, nullable=False)
    razon_social = Column(String(255), nullable=False)
    direccion = Column(String(255), nullable=True)
    telefono = Column(String(50), nullable=True)
    email = Column(String(150), nullable=True)