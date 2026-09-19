from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.connection_db_async import get_db
from src.dashboard.repository import EquiposDashboardRepository

router = APIRouter()

@router.get("/equipos")
async def dashboard_equipos( db: Session = Depends(get_db)):
    repo = EquiposDashboardRepository(db)
    ot_equipos_totales = await repo.get_count_ot_equipos()
    ot_equipos_pending = await repo.get_count_ot_equipos_pending()
    ot_equipos_procesing = await repo.get_count_ot_equipos_procesing()
    ot_equipos_cerrada = await repo.get_count_ot_equipos_cerrada()
    ot_equipos_x_cliente = await repo.get_count_ot_equipos_x_cliente()
    ot_equipos_x_fecha = await repo.get_count_ot_equipos_x_fecha()
    ot_equipos_abierta = await repo.get_count_ot_equipos_abierta()
    ot_equipos_clients_actives = await repo.get_count_clients_actives()
    
    # get_count_clients_actives
    # get_count_ot_equipos_abierta
    # get_count_ot_equipos_x_fecha
    # get_count_ot_equipos_x_cliente
    
    data_dashboard = {
        "ot_equipos_totales" : ot_equipos_totales,
        "ot_equipos_pending" : ot_equipos_pending,
        "ot_equipos_procesing" : ot_equipos_procesing,
        "ot_equipos_cerrada" : ot_equipos_cerrada,
        "ot_equipos_x_cliente" : ot_equipos_x_cliente,
        "ot_equipos_x_fecha" : ot_equipos_x_fecha,
        "ot_equipos_abierta": ot_equipos_abierta,
        "ot_equipos_clients_actives": ot_equipos_clients_actives
    }
    return data_dashboard