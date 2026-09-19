import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from src.connection_db_async import engine
from src.dashboard.repository import EquiposDashboardRepository # Importa solo el motor

async def ejecutar_consulta(date_start : str, data_end : str):
    # Creamos la sesión asíncrona manualmente usando el motor existente
    async with AsyncSession(engine) as db:
        repo = EquiposDashboardRepository(db)
        ot_equipos_totales = await repo.get_count_ot_equipos()
        ot_equipos_pending = await repo.get_count_ot_equipos_pending()
        ot_equipos_procesing = await repo.get_count_ot_equipos_procesing()
        ot_equipos_cerrada = await repo.get_count_ot_equipos_cerrada()
        
        data_dashboard = {
            "ot_equipos_totales" : ot_equipos_totales,
            "ot_equipos_pending" : ot_equipos_pending,
            "ot_equipos_procesing" : ot_equipos_procesing,
            "ot_equipos_cerrada" : ot_equipos_cerrada,
        }
        print(data_dashboard)

if __name__ == "__main__":
    asyncio.run(ejecutar_consulta())