from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


class EquiposDashboardRepository:
    # Cambia el tipo de pista a AsyncSession para mayor claridad
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_count_ot_equipos(self) -> int | None:
        try:
            query = text("SELECT count(*) FROM ot_equipos where deleted=false")

            # 1. Esperamos la ejecución de la consulta
            result = await self.db.execute(query)

            # 2. scalar() no es una corutina, se llama directo sobre el 'result'
            # que ya contiene los datos obtenidos de la DB.
            return result.scalar()

        except Exception as e:
            # Es útil imprimir el error para saber qué falló
            print(f"Error en consulta: {e}")
            return None

    async def get_count_ot_equipos_pending(self) -> int | None:
        try:
            query = text("SELECT count(*) FROM ot_equipos where estado='pendiente'")

            # 1. Esperamos la ejecución de la consulta
            result = await self.db.execute(query)

            # 2. scalar() no es una corutina, se llama directo sobre el 'result'
            # que ya contiene los datos obtenidos de la DB.
            return result.scalar()

        except Exception as e:
            # Es útil imprimir el error para saber qué falló
            print(f"Error en consulta: {e}")
            return None

    async def get_count_ot_equipos_procesing(self) -> int | None:
        try:
            query = text("SELECT count(*) FROM ot_equipos where estado='En Proceso'")

            # 1. Esperamos la ejecución de la consulta
            result = await self.db.execute(query)

            # 2. scalar() no es una corutina, se llama directo sobre el 'result'
            # que ya contiene los datos obtenidos de la DB.
            return result.scalar()

        except Exception as e:
            # Es útil imprimir el error para saber qué falló
            print(f"Error en consulta: {e}")
            return None

    async def get_count_ot_equipos_cerrada(self) -> int | None:
        try:
            query = text("SELECT count(*) FROM ot_equipos where estado='cerrada'")

            # 1. Esperamos la ejecución de la consulta
            result = await self.db.execute(query)

            # 2. scalar() no es una corutina, se llama directo sobre el 'result'
            # que ya contiene los datos obtenidos de la DB.
            return result.scalar()

        except Exception as e:
            # Es útil imprimir el error para saber qué falló
            print(f"Error en consulta: {e}")
            return None

    async def get_count_ot_equipos_abierta(self) -> int | None:
        try:
            query = text("SELECT count(*) FROM ot_equipos where estado='abierta'")

            # 1. Esperamos la ejecución de la consulta
            result = await self.db.execute(query)

            # 2. scalar() no es una corutina, se llama directo sobre el 'result'
            # que ya contiene los datos obtenidos de la DB.
            return result.scalar()

        except Exception as e:
            # Es útil imprimir el error para saber qué falló
            print(f"Error en consulta: {e}")
            return None

    async def get_count_ot_equipos_x_cliente(self) -> list | None:
        try:
            query = text("""
                            SELECT 
                                empresa, 
                                COUNT(*) AS cantidad
                            FROM public.ot_equipos
                            where deleted=false
                            and empresa IS NOT NULL
                            GROUP BY empresa
                            ORDER BY empresa ASC;
                         
                         """)

            # 1. Esperamos la ejecución de la consulta
            result = await self.db.execute(query)

            # que ya contiene los datos obtenidos de la DB.
            return [dict(row) for row in result.mappings().all()]

        except Exception as e:
            # Es útil imprimir el error para saber qué falló
            print(f"Error en consulta: {e}")
            return None

    async def get_count_ot_equipos_x_fecha(self) -> list | None:
        try:
            query = text("""
                            SELECT 
                                DATE(created_at) AS fecha, 
                                COUNT(*) AS cantidad
                            FROM public.ot_equipos
                            where deleted=false
                            GROUP BY DATE(created_at)
                            ORDER BY fecha ASC;
                         """)

            # 1. Esperamos la ejecución de la consulta
            result = await self.db.execute(query)

            # que ya contiene los datos obtenidos de la DB.
            return [dict(row) for row in result.mappings().all()]

        except Exception as e:
            # Es útil imprimir el error para saber qué falló
            print(f"Error en consulta: {e}")
            return None

    async def get_count_clients_actives(self) -> int | None:
        try:
            query = text("""
                            SELECT COUNT(DISTINCT empresa) AS total_empresas
                            FROM public.ot_equipos
                            WHERE deleted = false;
                         """)

            # 1. Esperamos la ejecución de la consulta
            result = await self.db.execute(query)
            
            # 2. scalar() no es una corutina, se llama directo sobre el 'result'
            # que ya contiene los datos obtenidos de la DB.
            return result.scalar()

        except Exception as e:
            # Es útil imprimir el error para saber qué falló
            print(f"Error en consulta: {e}")
            return None
