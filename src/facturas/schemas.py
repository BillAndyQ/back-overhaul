from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal

from decimal import Decimal
from pydantic import BaseModel, Field

class FacturaDetalleSchema(BaseModel):
    descripcion: str
    cantidad: Decimal = Decimal("1")
    precio_unitario: Decimal = Decimal("0")
    subtotal: Decimal = Decimal("0")
    igv: Decimal = Decimal("0")
    total: Decimal = Decimal("0")
    unidad: str | None = None
    id_equipo: int | None = None


class FacturaSchemaCreate(BaseModel):
    n_factura: str | None = None
    fecha_emision: str | None = None

    sin_igv: Decimal = Decimal("0")
    igv: Decimal = Decimal("0")
    total: Decimal = Decimal("0")
    detraccion: Decimal = Decimal("0")

    facturo: bool = False
    pagado: bool = False
    pago_detraccion: bool = False

    en_dolares: str | None = None
    moneda: str = "PEN"

    tipo_ot: str | None = None
    id_ot: int | None = None
    n_ot : str | None = None
    razon_social: str | None = None
    ruc: str | None = None

    detalles: list[FacturaDetalleSchema] = Field(default_factory=list)
    
class FacturaSchema(BaseModel):
    n_factura: Optional[str] = None
    fecha_emision: Optional[str] = None
    sin_igv: Decimal = 0
    igv: Decimal = 0
    total: Decimal = 0
    detraccion: Decimal = 0
    facturo: bool = False
    pagado: bool = False
    pago_detraccion: bool = False
    en_dolares: Optional[str] = None
    moneda: str = 'PEN'
    tipo_ot: Optional[str] = None
    id_ot: Optional[int] = None
    razon_social: Optional[str] = None
    ruc: Optional[str] = None
    total: Decimal = Decimal("0")
    