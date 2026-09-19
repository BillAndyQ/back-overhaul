from fastapi import APIRouter, Depends, HTTPException

from src.connection_db import get_db
from .repository import FacturaRepository, DetalleRepository
from .schemas import FacturaSchema, FacturaDetalleSchema, FacturaSchemaCreate

route = APIRouter()

# Rutas Facturas

# http://localhost:8000/api/v1/facturas/control/equipos
@route.get("/control/equipos")
def list_facturas(db=Depends(get_db)):
    return FacturaRepository(db).get_control_facturacion()

@route.get("/")
def list_facturas(db=Depends(get_db)):
    return FacturaRepository(db).get_facturas_con_detalles()

@route.post("/")
def create_factura(data: FacturaSchemaCreate, db=Depends(get_db)):
    return FacturaRepository(db).crear(data)

# Rutas Detalle
@route.post("/detalle")
def create_detalle(data: FacturaDetalleSchema, db=Depends(get_db)):
    return DetalleRepository(db).crear(data)

@route.delete("/detalle/{id}")
def delete_detalle(id: int, db=Depends(get_db)):
    if not DetalleRepository(db).eliminar(id):
        raise HTTPException(404)
    return {"ok": True}

@route.get("/{n_factura}")
def get_factura(n_factura : str,db=Depends(get_db)):
    return FacturaRepository(db).get_factura(n_factura)

@route.delete("/{n_factura}")
def delete_factura(n_factura: str, db=Depends(get_db)):
    if not FacturaRepository(db).eliminar_por_factura(n_factura):
        raise HTTPException(404)
    return {"ok": True}

@route.put("/{n_factura}")
def update_factura(
    n_factura: str,
    data: dict,
    db=Depends(get_db)
):
    return FacturaRepository(db).actualizar_factura_completa(
        n_factura,
        data
    )