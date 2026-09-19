from sqlalchemy.orm import Session

from src.facturas.schemas import FacturaSchemaCreate
from src.models import EquipoModel, OTEquipoModel
from .models import Factura, FacturaDetalle
from sqlalchemy import and_
from sqlalchemy import case

class FacturaRepository:
    def __init__(self, db: Session): self.db = db

    def get_all(self): return self.db.query(Factura).all()
    
    def get_factura(self, n_factura: str):
        factura = (
            self.db.query(Factura)
            .filter(Factura.n_factura == n_factura)
            .first()
        )

        if not factura:
            return None

        detalles = (
            self.db.query(FacturaDetalle)
            .filter(FacturaDetalle.factura_id == factura.id_factura)
            .all()
        )

        return {
            "factura": factura,
            "detalles": detalles
        }
        
    def get_factura_model(self, n_factura: str):
        return (
            self.db.query(Factura)
            .filter(Factura.n_factura == n_factura)
            .first()
        )
        
    def actualizar_factura_completa(self, n_factura: str, data: dict):

        factura = self.get_factura_model(n_factura)

        if not factura:
            return None


        detalles = data.get("detalles", [])


        # quitar detalles para actualizar cabecera
        factura_data = {
            key: value
            for key, value in data.items()
            if key != "detalles"
        }
        
        print(detalles)


        campos_factura = {
            "sin_igv",
            "igv",
            "total",
            "detraccion",
            "facturo",
            "pagado",
            "pago_detraccion",
            "en_dolares",
            "moneda",
            "tipo_ot",
            "n_ot",
            "razon_social",
            "ruc",
            "fecha_emision"
        }


        for key, value in factura_data.items():

            if key in campos_factura:
                setattr(factura, key, value)


        for detalle_data in detalles:

            id_detalle = detalle_data.get("id_factura_detalle")

            detalle = None

            if id_detalle:

                detalle = (
                    self.db.query(FacturaDetalle)
                    .filter(
                        FacturaDetalle.id_factura_detalle == id_detalle,
                        FacturaDetalle.factura_id == factura.id_factura
                    )
                    .first()
                )


            # Existe -> actualizar
            if detalle:

                for key, value in detalle_data.items():

                    if key not in {
                        "id_factura_detalle",
                        "factura_id"
                    }:
                        setattr(detalle, key, value)


            # No existe -> crear
            else:

                nuevo_detalle_data = {
                    key: value
                    for key, value in detalle_data.items()
                    if key not in {
                        "id_factura_detalle",
                        "factura_id"
                    }
                }


                nuevo_detalle = FacturaDetalle(
                    factura_id=factura.id_factura,
                    **nuevo_detalle_data
                )

                self.db.add(nuevo_detalle)


        self.db.commit()
        self.db.refresh(factura)

        return factura
    
    def actualizar(self, n_factura: str, data: FacturaSchemaCreate):
        factura = self.get_factura(n_factura)

        if not factura:
            return None

        factura_data = data.model_dump(exclude={"detalles"})

        for key, value in factura_data.items():
            setattr(factura, key, value)

        self.db.commit()
        self.db.refresh(factura)

        return factura
    
    def eliminar_por_factura(self, n_factura: str):
        factura = self.get_factura_model(n_factura)

        if not factura:
            return False

        self.db.delete(factura)
        self.db.commit()

        return True
    
    def get_by_id(self, id: int): return self.db.query(Factura).filter(Factura.id_factura == id).first()
    
    def crear(self, data: FacturaSchemaCreate):
        factura_data = data.model_dump(exclude={"detalles"})
        factura = Factura(**factura_data)
        self.db.add(factura)
        self.db.flush()
        print(data.detalles)
        for detalle in data.detalles:
            nuevo_detalle = FacturaDetalle(
                factura_id=factura.id_factura,
                **detalle.model_dump()
            )
            self.db.add(nuevo_detalle)

        self.db.commit()
        self.db.refresh(factura)

        return factura

    def eliminar(self, id: int):
        f = self.get_by_id(id)
        if f:
            self.db.delete(f)
            self.db.commit()
            return True
        return False
    
    def get_facturas_con_detalles(self):
        """
        Realiza un LEFT JOIN entre Factura y FacturaDetalle.
        Retorna todas las facturas y sus detalles asociados.
        """
        return self.db.query(Factura).outerjoin(FacturaDetalle).all()
    
    def get_control_facturacion(self):

        factura_exist = case(
            (
                Factura.id_factura.is_(None),
                False
            ),
            else_=True
        ).label("factura_exist")

        rows = (
            self.db.query(

                # OT
                OTEquipoModel.id.label("id_ot"),
                OTEquipoModel.n_ot,
                OTEquipoModel.empresa,
                OTEquipoModel.ruc,
                OTEquipoModel.estado.label("estado_ot"),

                # Equipo
                EquipoModel.id.label("id_equipo"),
                EquipoModel.placa,
                EquipoModel.tipo_unidad,
                EquipoModel.tipo_servicio,
                EquipoModel.fecha_servicio,

                # Detalle
                FacturaDetalle.id_factura_detalle,
                FacturaDetalle.descripcion,
                FacturaDetalle.cantidad,
                FacturaDetalle.precio_unitario,
                FacturaDetalle.subtotal,
                FacturaDetalle.igv,
                FacturaDetalle.total.label("total_detalle"),

                # Factura
                Factura.id_factura,
                Factura.n_factura,
                Factura.fecha_emision,
                Factura.moneda,
                Factura.facturo,
                Factura.pagado,
                Factura.pago_detraccion,
                Factura.total,

                factura_exist,
            )
            .join(
                OTEquipoModel,
                EquipoModel.id_ot_equipo == OTEquipoModel.id
            )
            .outerjoin(
                FacturaDetalle,
                FacturaDetalle.id_equipo == EquipoModel.id
            )
            .outerjoin(
                Factura,
                Factura.id_factura == FacturaDetalle.factura_id
            )
            .order_by(
                OTEquipoModel.n_ot,
                EquipoModel.placa
            )
            .all()
        )

        return [dict(row._mapping) for row in rows]
    
class DetalleRepository:
    def __init__(self, db: Session): self.db = db
    
    def crear(self, data):
        d = FacturaDetalle(**data.model_dump())
        self.db.add(d)
        self.db.commit()
        self.db.refresh(d)
        return d

    def eliminar(self, id: int):
        d = self.db.query(FacturaDetalle).filter(FacturaDetalle.id_factura_detalle == id).first()
        if d:
            self.db.delete(d)
            self.db.commit()
            return True
        return False