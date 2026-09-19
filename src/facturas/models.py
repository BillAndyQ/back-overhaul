from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    Numeric,
    Boolean,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from src.models import Base


class Factura(Base):
    __tablename__ = "facturas"
    __table_args__ = {"schema": "public"}

    id_factura = Column(BigInteger, primary_key=True, index=True)
    n_factura = Column(Text, nullable=True)
    fecha_emision = Column(Text, nullable=True)
    sin_igv = Column(Numeric(12, 2), default=0)
    igv = Column(Numeric(12, 2), default=0)
    total = Column(Numeric(12, 2), default=0)
    detraccion = Column(Numeric(12, 2), default=0)
    facturo = Column(Boolean, default=False)
    pagado = Column(Boolean, default=False)
    pago_detraccion = Column(Boolean, default=False)
    en_dolares = Column(Text, nullable=True)
    moneda = Column(String(3), default="PEN")
    tipo_ot = Column(Text, nullable=True)
    n_ot = Column(Text, nullable=True)
    id_ot = Column(BigInteger, nullable=True)
    razon_social = Column(Text, nullable=True)
    ruc = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    detalles = relationship(
        "FacturaDetalle", back_populates="factura", cascade="all, delete-orphan"
    )


class FacturaDetalle(Base):
    __tablename__ = "facturas_detalle"
    __table_args__ = {"schema": "public"}

    id_factura_detalle = Column(BigInteger, primary_key=True, index=True)
    factura_id = Column(
        BigInteger,
        ForeignKey("public.facturas.id_factura", ondelete="CASCADE"),
        nullable=False,
    )
    
    descripcion = Column(Text, nullable=False)
    cantidad = Column(Numeric(12, 2), default=1)
    precio_unitario = Column(Numeric(12, 2), default=0)
    subtotal = Column(Numeric(12, 2), default=0)
    igv = Column(Numeric(12, 2), default=0)
    total = Column(Numeric(12, 2), default=0)
    unidad = Column(Text, nullable=True)
    id_equipo = Column(BigInteger, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    factura = relationship("Factura", back_populates="detalles")
